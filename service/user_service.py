from dao.mysql_dao import mysql_dao
from model.user_model import User


async def get_user_by_id(user_id : int) -> User:
    query = "select * from user where user_id = %s"
    user = mysql_dao.execute_query(query, [user_id])
    print(user)
    return User(user_id=user[0]['user_id'], name=user[0]['name'], email=user[0]['email'])