import datetime

from pydantic import BaseModel
from .error_state import ErrorState


class Status(BaseModel):
    ok: bool = None
    errorState: ErrorState = None
    # respTime: datetime.datetime = None

