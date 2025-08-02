from pydantic import BaseModel


class PostRequest(BaseModel):
    label_id : int
    context : str


class PostResponse(BaseModel):
    post_id : int
    label_id : int
    context : str
    user_id : int
