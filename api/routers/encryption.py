import os
from dotenv import load_dotenv
from fastapi import APIRouter, status
import grpc
from compiled.encrypter_pb2_grpc import EncrypterStub
from compiled.encrypter_pb2 import Request

from models import Message

load_dotenv()
encryption_channel = grpc.insecure_channel(f"{os.getenv('GRPC_HOST')}:50051")
encryption_client = EncrypterStub(encryption_channel)
router = APIRouter(prefix="/encryption", tags=["Encryption"])


@router.post("/encrypt", status_code=status.HTTP_200_OK)
def encrypt(message: Message):
    request = Request(key=message.key, message=message.message)
    response = encryption_client.Encrypt(request)
    return {"encrypted": response.result}


@router.post("/decrypt", status_code=status.HTTP_200_OK)
def decrypt(message: Message):
    request = Request(key=message.key, message=message.message)
    response = encryption_client.Decrypt(request)
    return {"decrypted": response.result}
