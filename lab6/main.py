import time
from functools import wraps

# Простой декоратор для замера времени выполнения
def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[ДЕКОРАТОР] Время выполнения: {end - start:.4f} сек.")
        return result
    return wrapper

# Замыкание для построчного чтения файла с ограничением длины строки
def file_reader(filename, max_length, encoding='utf-8'):
    """
    Создаёт замыкание для чтения файла с ограничением длины строки.
    
    Args:
        filename: путь к файлу
        max_length: максимальная длина строки (количество символов)
        encoding: кодировка файла (по умолчанию utf-8)
    
    Returns:
        функцию, которая при каждом вызове возвращает следующую часть текста
    """
    if max_length <= 0:
        raise ValueError("Максимальная длина строки должна быть положительным числом")
    
    # Пытаемся открыть файл
    try:
        file = open(filename, 'r', encoding=encoding)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден")
        return None
    except PermissionError:
        print(f"Ошибка: Нет прав для чтения файла '{filename}'")
        return None
    except UnicodeDecodeError:
        # Пробуем другую кодировку
        try:
            file = open(filename, 'r', encoding='cp1251')
            print(f"[ПРЕДУПРЕЖДЕНИЕ] Использована кодировка cp1251 вместо {encoding}")
        except Exception as e:
            print(f"Ошибка: Не удалось прочитать файл - {e}")
            return None
    
    # Переменные замыкания
    remainder = ""      # остаток от предыдущей длинной строки
    is_exhausted = False  # флаг окончания файла
    
    # Внутренняя функция - замыкание
    def read_next():
        nonlocal remainder, is_exhausted
        
        # Если файл уже закончился и нет остатка
        if is_exhausted and not remainder:
            return None
        
        # Если есть остаток от предыдущей длинной строки
        if remainder:
            if len(remainder) <= max_length:
                result = remainder
                remainder = ""
                return result
            else:
                result = remainder[:max_length]
                remainder = remainder[max_length:]
                return result
        
        # Читаем следующую строку из файла
        line = file.readline()
        
        # Если файл закончился
        if not line:
            is_exhausted = True
            file.close()
            return None
        
        # Удаляем символ перевода строки
        line = line.rstrip('\n\r')
        
        # Если строка целиком помещается в лимит
        if len(line) <= max_length:
            return line
        
        # Если строка длиннее лимита - разбиваем
        result = line[:max_length]
        remainder = line[max_length:]
        return result
    
    return read_next

# Демонстрация работы
if __name__ == "__main__":
    print("=" * 70)
    print("ЛАБОРАТОРНАЯ РАБОТА №6: Генераторы")
    print("=" * 70)
    
    # Создаём тестовый файл для демонстрации
    test_filename = "test_file.txt"
    test_content = """Это короткая строка.
А это очень-очень-очень-очень-очень-очень-очень-очень-очень-очень длинная строка, которая явно превышает лимит в 30 символов.
Третья строка с нормальной длиной.
Последняя строка файла."""
    
    with open(test_filename, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print(f"\n[ИНФО] Создан тестовый файл: {test_filename}")
    print(f"[ИНФО] Содержимое файла:")
    print("-" * 70)
    print(test_content)
    print("-" * 70)
    
    # Применяем декоратор к замыканию
    @timer_decorator
    def get_reader():
        return file_reader(test_filename, max_length=30)
    
    # Создаём замыкание (обёрнутое декоратором)
    print("\n[ЛОГ] Инициализация генератора...")
    reader = get_reader()
    
    if reader is None:
        print("Ошибка: Не удалось создать читатель файла")
        exit(1)
    
    print("\n[РЕЗУЛЬТАТ] Построчное чтение с ограничением 30 символов:")
    print("-" * 70)
    
    # Читаем все блоки
    block_num = 1
    while True:
        text = reader()
        if text is None:  # конец файла
            break
        print(f"Блок {block_num}: \"{text}\" (длина: {len(text)})")
        block_num += 1
    
    print("-" * 70)
    print(f"\n[ИТОГО] Прочитано блоков: {block_num - 1}")
    print("[ИНФО] Работа программы завершена")
    
    # Дополнительная демонстрация с разными лимитами (без декоратора)
    print("\n" + "=" * 70)
    print("ДОПОЛНИТЕЛЬНАЯ ДЕМОНСТРАЦИЯ С РАЗНЫМИ ЛИМИТАМИ")
    print("=" * 70)
    
    for limit in [10, 20, 50]:
        print(f"\nЛимит: {limit} символов")
        print("-" * 50)
        
        # Создаём замыкание без декоратора
        reader_func = file_reader(test_filename, limit)
        if reader_func:
            block_num = 1
            while True:
                text = reader_func()
                if text is None:
                    break
                print(f"  {block_num}: \"{text}\"")
                block_num += 1
    
    # Очистка: удаляем тестовый файл
    import os
    os.remove(test_filename)
    print("\n[ИНФО] Тестовый файл удалён")
