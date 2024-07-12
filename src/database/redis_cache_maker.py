import redis
from dotenv import load_dotenv
from os import getenv

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
            else:
                print(f"Chave '{key}' não encontrada no Redis")
                return None
        except redis.RedisError as e:
            print(f"Erro ao obter chave '{key}': {e}")

    
    def get_all(self, keys):
        try:
            values = self.redis_client.mget(keys)
            if values:
                return [value.decode('utf-8') for value in values if value]
            else:
                print(f"Chave '{keys}' não encontrada no Redis")
                return None
        except redis.RedisError as e:
            print(f"Erro ao obter chave '{keys}': {e}")
    
    def close(self):
        if self.redis_client:
            self.redis_client.close()
            print("Conexão com Redis fechada")
