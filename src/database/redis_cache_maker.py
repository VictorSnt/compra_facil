from os import getenv

import redis
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

class RedisConnection:
    def __init__(self, host=None, port=None, password=None, db=0):
        self.host = host or getenv('REDIS_HOST')
        self.port = port or int(getenv('REDIS_PORT'))
        self.db = db
        self.password = password or getenv('REDIS_PASSWD')
        self.redis_client = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        try:
            self.redis_client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password
            )
            self.redis_client.ping()  
            print(f"Conectado ao Redis em {self.host}:{self.port}, DB {self.db}")
        except redis.ConnectionError as e:
            print(f"Erro ao conectar ao Redis: {e}")

    def set(self, key, value, expiry=86400):
        try:
            self.redis_client.set(key, value, ex=expiry)
            print(f"Chave '{key}' definida com valor '{value}'")
        except redis.RedisError as e:
            print(f"Erro ao definir chave '{key}': {e}")

    def get(self, key):
        try:
            value = self.redis_client.get(key)
            if value:
                return value.decode('utf-8')
            print(f"Chave '{key}' não encontrada no Redis")
            return None
        except redis.RedisError as e:
            print(f"Erro ao obter chave '{key}': {e}")
            return None

    def get_all(self, keys):
        try:
            values = self.redis_client.mget(keys)
            if values:
                return [value.decode('utf-8') for value in values if value]
            print(f"Chave '{keys}' não encontrada no Redis")
            return None
        except redis.RedisError as e:
            print(f"Erro ao obter chave '{keys}': {e}")
            return None

    def delete(self, key: str):
        try:
            # Verifique se a chave existe antes de deletar
            if not self.redis_client.exists(key):
                return HTTPException(404, f'Chave {key} não encontrada')

            # Tente deletar a chave
            result = self.redis_client.delete(key)
            if result == 0:
                return HTTPException(400, f'Falha ao deletar a chave: {key}')

            print(f'Chave {key} deletada com sucesso')
            return None
        except redis.RedisError as e:
            print(e)
            return HTTPException(
                400, f'Ocorreu uma falha ao inativar a chave: {key}'
            )

    def close(self):
        if self.redis_client:
            self.redis_client.close()
            print("Conexão com Redis fechada")
