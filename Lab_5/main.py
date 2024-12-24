import matplotlib.pyplot as plt
import numpy as np

S_range = 1500  # Дальность до середины мишени
G = 9.81    # Усорение свободного падения
Delta = 25   # Размер мишени в метрах
Alfa = np.radians(39.5)   # Угол выстрела пушки

V_0 = np.sqrt(S_range * G / np.sin(Alfa * 2))    # Начальная скорость
print(V_0)
V_math = 122    # Мат. ожид. для скорости
V_sigma = 2     # Среднеквадратическое для скорости
Alfa_math = Alfa    # Мат. ожид. для alfa
Alfa_sigma = np.radians(2)  # Среднеквадратическое для альфа в радианах

# Кол-во генераций
N_simulation = 100000

# Генерация значений скорости и угла по НЗР
V_valus = np.random.normal(V_math, V_sigma, N_simulation)
Alfa_values = np.random.normal(Alfa_math, Alfa_sigma, N_simulation)

# Дальность выстрела для каждой пары V и Alfa
S_values = (V_valus**2 * np.sin(Alfa_values * 2)) / G

S_mean = M = np.mean(S_values)  # Средняя дальность
D = np.var(S_values)    # Дисперсия дальности

# Вероятность попадания в мишень
Hits_count = 0  # Счетчик попаданий
for i in range(N_simulation):
    if abs(S_values[i] - S_range) <= (Delta / 2):
        Hits_count += 1

Hits_prob = Hits_count / N_simulation

# Графики зависимости M и D от числа испытаний

Trial_numbers = np.arange(100, N_simulation + 1, 100)
M_values = []   # np.mean(current_values) вычисляет среднее значение для текущей выборки, которое добавляется в список M_values"""
D_values = []   #np.var(current_values) вычисляет дисперсию для текущей выборки, добавляя ее в список D_values

for N in Trial_numbers:
    current_values = S_values[:N]   # current_values = S_values[:N] берет первые N значений из массива S_values
    M_values.append(np.mean(current_values))
    D_values.append(np.var(current_values))

# Вычисление трех сигм
three_sigma_low = S_mean - 3 * np.sqrt(D)
three_sigma_high = S_mean + 3 * np.sqrt(D)

# Доля значений в пределах трех сигм
within_three_sigma = np.sum((S_values >= three_sigma_low) & (S_values <= three_sigma_high))
three_sigma_prob = within_three_sigma / N_simulation

# Создание интервалов для гистограммы
bin_width = 20  # Ширина интервала в метрах
bins = np.arange(0, max(S_values) + bin_width, bin_width)

# Графики M, D и гистограмма
plt.figure(figsize=(15, 10))

# График для M
plt.subplot(2, 2, 1)  # Создаем первый подграфик (верхний левый угол)
plt.plot(Trial_numbers, M_values, label='M (Мат. ожидание)', color='blue')  # График зависимости M от числа испытаний
plt.xlabel('Число испытаний')
plt.ylabel('M')
plt.title('Зависимость M от числа испытаний')
plt.grid()  # Включаем сетку для удобства чтения
plt.legend()

# График для D
plt.subplot(2, 2, 2)  # Создаем второй подграфик (верхний правый угол)
plt.plot(Trial_numbers, D_values, label='D (Дисперсия)', color='orange')  # График зависимости D от числа испытаний
plt.xlabel('Число испытаний')
plt.ylabel('D')
plt.title('Зависимость D от числа испытаний')
plt.grid()
plt.legend()

# Гистограмма распределения дальности выстрела
plt.subplot(2, 1, 2)  # Создаем третий подграфик (вся нижняя часть)
counts, bin_edges, _ = plt.hist(S_values, bins=bins, color='skyblue', edgecolor='black', alpha=0.7)  # Построение гистограммы
plt.xlabel('Дальность выстрела (м)')
plt.ylabel('Частота')
plt.title('Гистограмма распределения дальности выстрела')
plt.grid()  # Включаем сетку для удобства чтения

# Добавление текста на гистограмму
for i in range(len(counts)):
    plt.text(bin_edges[i] + bin_width / 2, counts[i] + 0.5, str(int(counts[i])),  # Добавляем текст над каждым столбцом
             ha='center', va='bottom', fontsize=9, color='black')

# Добавление информации о попаданиях в мишень
plt.axvline(x=S_range - Delta / 2, color='green', linestyle='--', label='Граница мишени')  # Левая граница мишени
plt.axvline(x=S_range + Delta / 2, color='green', linestyle='--')  # Правая граница мишени
plt.axvline(x=three_sigma_low, color='red', linestyle='--', label=f'3σ граница: {three_sigma_low:.2f} м')  # Левая граница трех сигм
plt.axvline(x=three_sigma_high, color='red', linestyle='--')  # Правая граница трех сигм
plt.legend(loc='upper right')  # Добавляем легенду

plt.tight_layout()  # Оптимизируем размещение графиков
plt.show()  # Отображаем графики

# Вывод результатов
print(f"Правило трех сигм: от {three_sigma_low:.2f} до {three_sigma_high:.2f} м")
print(f"Доля значений в пределах трех сигм: {three_sigma_prob * 100:.2f}%")
print(f"Средняя дальность выстрела: {S_mean:.2f} м")
print(f"Вероятность попадания в мишень: {Hits_prob * 100:.2f}%")
print(f"Математическое ожидание дальности: {M:.2f} м")
print(f"Дисперсия дальности: {D:.2f} м^2")
