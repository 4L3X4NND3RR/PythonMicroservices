from base64 import b64decode, b64encode
from Crypto.Cipher import AES

init_vector = [35, 46, 57, 24, 85, 35, 24, 74, 87, 35, 88, 98, 66, 32, 14, 5]


def encrypt(key, message):
    cipher = AES.new(key.encode("utf-8"), AES.MODE_CFB, iv=bytearray(init_vector))
    ct_bytes = cipher.encrypt(message.encode("utf-8"))
    ct = b64encode(ct_bytes).decode("utf-8")
    return ct


def decrypt(key, message):
    cipher = AES.new(key.encode("utf-8"), AES.MODE_CFB, iv=bytearray(init_vector))
    pt = cipher.decrypt(b64decode(message))
    return pt
