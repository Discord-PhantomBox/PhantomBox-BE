from http.client import HTTPException
from typing import List

from model.post_model import PostRequest, PostResponse
from dao.mysql_dao import mysql_dao
from model.user_model import User

async def post(post_request : PostRequest, user : User):
    sql = "insert into post(label_id, context, user_id) values(%s, %s, %s)"
    mysql_dao.execute_update(sql, [post_request.label_id, post_request.context, user.user_id])
    return {"message": "post success"}


async def get_posts() -> List[PostResponse]:
    sql = "select * from post"
    posts = mysql_dao.execute_query(sql)
    return [PostResponse(post_id=post['post_id'], context=post['context'], label_id=post['label_id'], user_id=post['user_id']) for post in posts]


async def get_post(post_id) -> PostResponse:
    sql = "select * from post where post_id = %s"
    post = mysql_dao.execute_query(sql, [post_id])
    return PostResponse(post_id=post[0]['post_id'], label_id=post[0]['label_id'], context=post[0]['context'], user_id=post[0]['user_id'])


async def get_my_posts(user : User):
    sql = "select * from post where user_id = %s"
    posts = mysql_dao.execute_query(sql, [user.user_id])
    return [PostResponse(post_id=post['post_id'], context=post['context'], label_id=post['label_id'], user_id=post['user_id']) for post in posts]


async def delete_post(post_id : int):
    sql = "delete from post where post_id = %s"
    mysql_dao.execute_update(sql, [post_id])
    return {"message": "post delete success"}


async def update(post_id, post_request):
    sql = "update post set label_id = %s, context = %s where post_id = %s"
    mysql_dao.execute_update(sql, [post_request.label_id, post_request.context, post_id])
    return {"message": "post update success"}