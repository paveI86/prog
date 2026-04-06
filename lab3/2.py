# task2_count_digit_2_in_base3.py
"""
Задача: вычислить 9^8 + 3^5 - 9, перевести в троичную систему,
подсчитать количество цифр 2.
"""

def to_base3(n: int) -> str:
    """Перевод числа в троичную систему счисления"""
    if n == 0:
        return "0"
    digits = []
    while n > 0:
        digits.append(str(n % 3))
        n //= 3
    return ''.join(reversed(digits))

def solve_task2():
    # Вычисляем выражение
    result = 9**8 + 3**5 - 9
    print(f"Значение выражения: {result}")
    
    # Переводим в троичную систему
    base3_repr = to_base3(result)
    print(f"В троичной системе: {base3_repr}")
    
    # Считаем количество цифр '2'
    count_2 = base3_repr.count('2')
    print(f"Количество цифр 2: {count_2}")
    
    # Дополнительная проверка: анализ разрядов
    print("\nПроверка через степени:")
    print(f"9^8 = 3^16 → в троичной: 1 и 16 нулей")
    print(f"3^5 → в троичной: 1 и 5 нулей")
    print(f"Вычитаем 9 = 3^2")
    
    return count_2

if __name__ == "__main__":
    solve_task2()