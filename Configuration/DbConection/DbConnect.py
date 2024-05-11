import psycopg2

class DbConnection:
    def __init__(self, host: str, port: str, dbname: str, user: str, password: str):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.conn = None
        self.error = None

    def connect(self) -> bool:
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            return True
        except psycopg2.Error as e:
            self.error = f"Falha na conexão: {e}"
            raise psycopg2.Error

    def execute_query(self, query, args=None) -> list:
        if not self.conn:
            self.error = "Você não está conectado a nenhum banco de dados."
            return []
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, args)
                return self._fetch_results(cursor)
        except psycopg2.Error as e:
            self.error = f"Falha na execução da consulta: {e}"
            return []

    def _fetch_results(self, cursor) -> list:
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return [{column: value for column, value in zip(columns, row)} for row in rows]

    def close_connection(self) -> bool:
        try:
            self.conn.close()
            return True
        except psycopg2.Error as e:
            self.error = f"Falha ao fechar a conexão: {e}"
            return False

    def commit(self) -> bool:
        try:
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            self.error = f"Falha ao confirmar transação: {e}"
            return False

    def rollback(self) -> bool:
        try:
            self.conn.rollback()
            return True
        except psycopg2.Error as e:
            self.error = f"Falha ao fazer rollback: {e}"
            return False
    
    def execute_update(self, query) -> int:
        if not self.conn:
            self.error = "Você não está conectado a nenhum banco de dados."
            return 0

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.rowcount
        except psycopg2.Error as e:
            self.error = f"Falha na execução da consulta: {e}"
            return 0
    
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()
