from dotenv import load_dotenv
from concurrent import futures
import time
from publisher import Publisher
from compiled.encrypter_pb2_grpc import (
    EncrypterServicer,
    add_EncrypterServicer_to_server,
)
from compiled.encrypter_pb2 import Response

from utils import encrypt, decrypt
import grpc

load_dotenv()

class EncrypterService(EncrypterServicer):
    def __init__(self, publisher) -> None:
        self._publisher = publisher

    def Encrypt(self, request, context):
        encrypted = encrypt(request.key, request.message)
        self._publisher.publish("encrypted", request.message)
        return Response(result=encrypted)

    def Decrypt(self, request, context):
        decrypted = decrypt(request.key, request.message)
        self._publisher.publish("decrypted", request.message)
        return Response(result=decrypted)


def serve():
    publisher = Publisher()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_EncrypterServicer_to_server(EncrypterService(publisher=publisher), server)

    server.add_insecure_port("[::]:50051")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
        publisher.close_connection()


if __name__ == "__main__":
    serve()
