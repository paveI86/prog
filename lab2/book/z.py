import numpy as np
import matplotlib.pyplot as plt

# Определение функций
def f1(x):
    return np.exp(np.sin(x))

def f2(x):
    return np.exp(x) - 1 / np.sqrt(x)

# Создание массива x (область определения: x > 0 из-за корня)
x = np.linspace(0.1, 2, 500)  # от 0.1 до 2, чтобы избежать деления на ноль

# Вычисление значений функций
y1 = f1(x)
y2 = f2(x)

# Построение графиков
plt.figure(figsize=(12, 7))

plt.plot(x, y1, 'b-', label='$f_1(x) = e^{\\sin x}$', linewidth=2)
plt.plot(x, y2, 'r-', label='$f_2(x) = e^x - \\frac{1}{\\sqrt{x}}$', linewidth=2)

# Настройка графика
plt.title('Графики функций $f_1(x) = e^{\\sin x}$ и $f_2(x) = e^x - \\frac{1}{\\sqrt{x}}$', fontsize=14)
plt.xlabel('$x$', fontsize=12)
plt.ylabel('$y$', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12, loc='best')

# Добавление горизонтальной линии y = 0 для наглядности
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.5)

# Ограничение по y для лучшей наглядности (можно убрать или изменить)
plt.ylim(-5, 8)

plt.tight_layout()
plt.savefig('two_functions_plot.png', dpi=300, bbox_inches='tight')
plt.show()

# Вывод информации о точках пересечения с осью x (корни)
print("Поиск корней f2(x) = 0:")
print("Приблизительные корни можно найти визуально на графике")