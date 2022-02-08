from pydantic import BaseModel


class Message(BaseModel):
    key: str
    message: str
