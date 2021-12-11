from pydantic.main import BaseModel


class LegacyBody(BaseModel):
    taskId: str = None
    pdfUrl: str = None
    referenceUrl: str = None
    callback: str = None


class ConvertRequest(BaseModel):
    legacy: LegacyBody = None

