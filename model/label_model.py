from pydantic import BaseModel


class TextRequest(BaseModel):
    text: str

class LabelTextResponse(BaseModel):
    label : str
