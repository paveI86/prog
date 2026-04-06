# ========== ЗАДАЧА 1. Сумма вложенных списков ==========

# Рекурсивная версия
def sum_nested_recursive(lst):
    total = 0
    for item in lst:
        if isinstance(item, list):
            total += sum_nested_recursive(item)
        elif isinstance(item, (int, float)):
            total += item
    return total

# Итеративная версия (без рекурсии)
def sum_nested_iterative(lst):
    stack = list(lst)
    total = 0
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(item)
        elif isinstance(item, (int, float)):
            total += item
    return total

# Пример использования
print(sum_nested_recursive([1, [2, [3, 4, [5]]]]))
print(sum_nested_iterative([1, [2, [3, 4, [5]]]]))