import json

from os import getenv
from dotenv import load_dotenv

from redis import Redis, ConnectionPool
from redis.exceptions import RedisError



class DotEnv:
    
    def __init__(self):
        """ # Загружаем переменные из .env файла """
        load_dotenv()
        self.host = getenv("REDIS_HOST")  # Получаем хост
        self.port = int(getenv("REDIS_PORT"))  # Получаем порт и преобразуем в int
        self.username = getenv(key="REDIS_USER")
        self.password = getenv(key="REDIS_USER_PASSWORD")



class RedisManager:
    
    def __init__(self, client: Redis):
        self.redis = client
        
    def save_if_not_exists(self, key: str, data) -> None:
        """ Сохраняет данные в Redis, если их нет, с временем кеширования 30 секунд. """
        if not self.redis.exists(key):
            # Преобразуем данные в JSON, если это словарь
            if isinstance(data, dict):
                data = json.dumps(data)
            # Сохраняем данные в Redis
            self.redis.set(key, data, ex=30)  # ex=30 устанавливает время жизни в 30 секунд
            print(f"Данные сохранены под ключом '{key}'.")
        else:
            print(f"Данные с ключом '{key}' уже существуют в Redis.")
    
    def get_data(self, key: str) -> None:
        """ Получает данные по ключу из Redis и выводит их в консоли. """
        try:
            data = self.redis.get(key)
            if data is not None:
                # Проверяем, является ли данные строкой JSON
                try:
                    data = json.loads(data)  # Преобразуем обратно в словарь, если это JSON
                except json.JSONDecodeError:
                    pass  # Если не JSON, оставляем как есть
                print(f"Данные по ключу '{key}': {data}")
            else:
                print(f"Данные с ключом '{key}' не найдены в Redis.")
        except RedisError as e:
            print(f"Ошибка при получении данных: {e}")

    def test(self) -> None:
        """ Метод теста подключения """        
        try:
            info = redis.info()
            print(info['redis_version'])
            response = redis.ping()
            if response:
                print("Подключение успешно!")
                
                # Пример использования метода save_if_not_exists
                sample_dict = {"name": "Alice", "age": 30, "city": "Wonderland"}
                self.save_if_not_exists("user:1", sample_dict)  # Сохраняем словарь с ключом "user:1"
                
                sample_string = "Hello, Redis!"
                self.save_if_not_exists("greeting", sample_string)  # Сохраняем строку с ключом "greeting"
                
                # Пример использования метода get_data
                self.get_data("user:1")  # Получаем данные по ключу "user:1"
                self.get_data("greeting")  # Получаем данные по ключу "greeting"
                self.get_data("non_existing_key")  # Пробуем получить несуществующий ключ
                
            else:
                print("Не удалось подключиться к Redis.")
        except (RedisError, Exception) as e:
            print(f"Ошибка: {e}")
    
    
        
if __name__ == "__main__":
    de = DotEnv()

    redis = Redis(connection_pool=ConnectionPool(  # Создаем пул соединений
        host=de.host,
        port=de.port,
        db=0,
        username=de.username,
        password=de.password,
        max_connections=10  # Укажите максимальное количество соединений в пуле
    ))
    
    redis_manager = RedisManager(client=redis)
    redis_manager.test()