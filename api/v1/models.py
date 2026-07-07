from pydantic import BaseModel

class CompileRequest(BaseModel):
    code: str

class BrainOSRequest(BaseModel):
    intent: str
