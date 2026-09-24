import sys

def main():
    # Читаем все данные из стандартного ввода (неважно, одной строкой или несколькими)
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    # Парсим данные
    n = int(input_data[0])
    q = list(map(int, input_data[1:n+1]))
    k = int(input_data[n+1])

    # Вычисляем сумму первого окна
    current_sum = sum(q[:k])
    
    # Формируем результат
    result = []
    result.append(f"{current_sum / k:.1f}")

    # Двигаем окно
    for i in range(1, n - k + 1):
        current_sum = current_sum - q[i - 1] + q[i + k - 1]
        result.append(f"{current_sum / k:.1f}")

    # Выводим через пробел
    print(" ".join(result))

if __name__ == "__main__":
    main()