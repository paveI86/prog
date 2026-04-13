import requests
import time
from functools import wraps

# Декоратор для замера времени выполнения
def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[ДЕКОРАТОР] Время выполнения: {end - start:.4f} сек.")
        return result
    return wrapper

# Замыкание: запоминает URL и возвращает функцию получения факта
def api_requester(url):
    @timer_decorator   # применяем декоратор к внутренней функции
    def get_fact():
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            # Извлекаем текст факта (структура зависит от API)
            fact = data["data"][0]["attributes"]["body"]
            return fact
        except requests.exceptions.RequestException as e:
            return f"Ошибка запроса: {e}"
        except (KeyError, IndexError, ValueError) as e:
            return f"Ошибка парсинга ответа: {e}"
    return get_fact

# Использование
if __name__ == "__main__":
    api_url = "https://dogapi.dog/api/v2/facts"
    
    # Создаём замыкание
    dog_fact_clousure = api_requester(api_url)
    
    # Вызываем замыкание (срабатывает декоратор)
    fact_text = dog_fact_clousure()
    
    print("Факт о собаках:", fact_text)