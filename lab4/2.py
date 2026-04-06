import math

# Рекурсивная версия
def sequence_recursive(k):
    if k == 1:
        return 1.0, 1.0
    a_prev, b_prev = sequence_recursive(k - 1)
    a_k = 0.5 * (math.sqrt(b_prev) + 0.5 * math.sqrt(a_prev))
    return a_k, b_prev

# Итеративная версия
def sequence_iterative(k):
    if k == 1:
        return 1.0
    a = 1.0
    b = 1.0
    for _ in range(2, k + 1):
        a_new = 0.5 * (math.sqrt(b) + 0.5 * math.sqrt(a))
        a, b = a_new, a
    return a

# Пример использования
a_rec, b_rec = sequence_recursive(5)
print(a_rec)

a_iter = sequence_iterative(5)
print(a_iter)