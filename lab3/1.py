# task1_count_code_words.py
"""
Задача: сколько 4-буквенных слов из букв A,B,C,D,X,Y,Z,
если первая буква X,Y,Z, а далее X,Y,Z не встречаются.
"""

def solve_task1():
    # Аналитическое решение
    first_letter_options = 3  # X, Y, Z
    other_letter_options = 4  # A, B, C, D
    positions_after_first = 3  # 2-я, 3-я, 4-я позиции
    
    total = first_letter_options * (other_letter_options ** positions_after_first)
    print(f"Аналитически: {first_letter_options} × {other_letter_options}^{positions_after_first} = {total}")
    
    # Проверка перебором (для демонстрации)
    alphabet = ['A', 'B', 'C', 'D', 'X', 'Y', 'Z']
    first_letters = ['X', 'Y', 'Z']
    rest_letters = ['A', 'B', 'C', 'D']
    
    count = 0
    for first in first_letters:
        for second in rest_letters:
            for third in rest_letters:
                for fourth in rest_letters:
                    count += 1
                    # Можно раскомментировать для вывода всех слов (будет много)
                    # print(first + second + third + fourth)
    
    print(f"Перебором: {count}")
    print(f"Ответ: {count} различных кодовых слов")

if __name__ == "__main__":
    solve_task1()