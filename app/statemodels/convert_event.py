from pydantic import BaseModel


class ConvertEvent(BaseModel):
    code: int
    errorStateCode: str
    message: str

