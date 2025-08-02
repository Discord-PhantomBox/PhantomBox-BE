import pymysql

class MySQLDAO:
    def __init__(self, host, user, password, db, port=3306, charset='utf8mb4'):
        self.conn_params = {
            'host': host,
            'user': user,
            'password': password,
            'db': db,
            'port': port,
            'charset': charset,
            'cursorclass': pymysql.cursors.DictCursor,  # 결과를 dict 형태로
        }

    def _get_connection(self):
        return pymysql.connect(**self.conn_params)

    def execute_query(self, query, params=None):
        """
        SELECT 등 조회 쿼리 실행 후 결과 반환
        """
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
            return result
        finally:
            conn.close()

    def execute_update(self, query, params=None):
        """
        INSERT, UPDATE, DELETE 쿼리 실행 후 영향받은 row 수 반환
        """
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                affected = cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()

mysql_dao = MySQLDAO('localhost', 'root', 'kdoornega0128', 'hiton', 3306)