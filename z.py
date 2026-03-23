import numpy as np
import matplotlib.pyplot as plt

# Определение функции
def f(x):
    return np.exp(np.sin(x))

# Точка касания (выбираем x0 = 0.2)
x0 = 0.2
y0 = f(x0)

# Производная функции f'(x) = e^(sin x) * cos x
def f_derivative(x):
    return np.exp(np.sin(x)) * np.cos(x)

# Уравнение касательной: y = f(x0) + f'(x0)(x - x0)
def tangent_line(x):
    return y0 + f_derivative(x0) * (x - x0)

# Создание массива точек для графика
x = np.linspace(0, 0.25, 100)
y = f(x)
y_tangent = tangent_line(x)

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='f(x) = e^(sin x)', linewidth=2)
plt.plot(x, y_tangent, '--', label='Касательная в точке x = 0.2', linewidth=2)
plt.plot(x0, y0, 'ro', markersize=8)

# Добавление аннотации к точке касания
plt.annotate(f'Точка касания\n({x0:.2f}, {y0:.4f})', 
             xy=(x0, y0), 
             xytext=(x0+0.03, y0-0.1),
             arrowprops=dict(arrowstyle='->', color='red'),
             fontsize=10,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

# Настройка графика
plt.title('График функции f(x) = e^(sin x) и касательной к ней', fontsize=14)
plt.xlabel('x', fontsize=12)
plt.ylabel('y', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)

# Добавление вертикальной линии в точке разрыва
plt.axvline(x=0.25, color='gray', linestyle=':', alpha=0.7, label='Точка разрыва (x = 0.25)')

plt.tight_layout()
plt.savefig('function_plot.png', dpi=300, bbox_inches='tight')
plt.show()