from pydantic import BaseModel


class ErrorState(BaseModel):
    code: int
    errorStateCode: str
    message: str


