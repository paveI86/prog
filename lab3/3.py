# task3_numbers_with_5_odd_divisors.py
"""
Найти числа из [45_000_000; 50_000_000], у которых ровно 5 различных нечётных делителей.
Число имеет вид 2^k * p^4, где p — нечётное простое.
"""

import math

def is_prime(n: int) -> bool:
    """Проверка на простоту"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def solve_task3():
    LOW = 45_000_000
    HIGH = 50_000_000
    result = []
    
    # p^4 должно быть <= HIGH, т.е. p <= HIGH^(1/4)
    max_p = int(round(HIGH ** 0.25)) + 2
    
    for p in range(3, max_p + 1, 2):  # только нечётные простые
        if not is_prime(p):
            continue
        
        p4 = p ** 4
        if p4 > HIGH:
            break
        
        # Перебираем степень двойки k
        k = 0
        while True:
            num = (2 ** k) * p4
            if num > HIGH:
                break
            if num >= LOW:
                result.append(num)
            k += 1
    
    result.sort()
    
    print(f"Найдено чисел: {len(result)}")
    print("Числа в порядке возрастания:")
    for num in result:
        print(num)
    
    # Проверка для первого числа
    if result:
        print("\nПроверка первого числа:")
        test_num = result[0]
        # Находим нечётную часть
        odd_part = test_num
        while odd_part % 2 == 0:
            odd_part //= 2
        print(f"Число: {test_num}")
        print(f"Нечётная часть: {odd_part}")
        # Находим делители нечётной части
        divisors = [d for d in range(1, odd_part + 1) if odd_part % d == 0]
        odd_divisors = [d for d in divisors if d % 2 == 1]
        print(f"Нечётные делители: {odd_divisors}")
        print(f"Их количество: {len(odd_divisors)}")

if __name__ == "__main__":
    solve_task3()