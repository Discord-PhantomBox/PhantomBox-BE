from pydantic import BaseModel


class GoogleUrlResponse(BaseModel):
    url : str