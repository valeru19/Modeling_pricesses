import numpy as np
import time

# Начальные параметры
seed_value = 0  # Начальное значение генератора
mod = 2**31 - 1 # Модуль (максимальное значение)
factor = 1122348271 # Множитель
offset = 7  # Приращение
num_values = int(1e6)   # Количество генерируемых значений
primary_array = np.zeros(num_values)    # Массив для хранения значений из генератора
secondary_array = np.zeros(num_values)  # Массив для стандартного ГСЧ
epsilon = 1e-31

# Функция генерации следующего числа
def generate_number(seed):
    return (factor * seed + offset) % mod


# Проверка уникальности значений массива
def test_uniqueness(values):
    start_time = time.time()
    is_unique = True
    sorted_values = np.sort(values)   # Сортировка массива по возрастанию
    for i in range(len(sorted_values) - 1):
        if abs(sorted_values[i] - sorted_values[i + 1]) < epsilon:
            print("1.\tОшибка: Найдены неуникальные значения.")
            is_unique = False
            break
    if is_unique:
        print("1.\tТест на уникальность пройден.")
    print("\tВремя прохождения теста:", time.time() - start_time)


# Вычисление математического ожидания
def calculate_mean(values):
    start_time = time.time()
    mean_value = np.mean(values)
    print(f"2.\tМатематическое ожидание: {mean_value}")
    print("\tВремя прохождения теста:", time.time() - start_time)
    return mean_value


# Вычисление дисперсии и среднеквадратичного отклонения
def calculate_variance_and_std(values, mean_value):
    start_time = time.time()
    variance = np.mean((values - mean_value) ** 2)
    std_deviation = np.sqrt(variance)
    print(f"3.\tДисперсия: {variance}\n  \tСреднеквадратичное отклонение: {std_deviation}")
    print("\tВремя прохождения теста:", time.time() - start_time)
    return variance, std_deviation


# Частотный тест
def frequency_test(values, std_deviation):
    start_time = time.time()
    upper_limit = 0.5 + std_deviation
    lower_limit = 0.5 - std_deviation
    expected_freq = upper_limit - lower_limit  # Ожидаемая частота
    actual_freq = np.sum((values > lower_limit) & (values < upper_limit)) / len(values)
    print(f"4.\tОжидаемый результат частотного теста: {expected_freq}")
    print(f"  \tФактический результат частотного теста: {actual_freq}")
    print("\tВремя прохождения теста:", time.time() - start_time)


# Проверка вероятности попадания в интервалы
def interval_probability(values):
    start_time = time.time()
    left_interval = np.sum(values <= 0.5)
    right_interval = len(values) - left_interval
    print(f"5.\tВероятность попадания в [0;0.5]: {left_interval / len(values)}")
    print(f"  \tВероятность попадания в (0.5;1]: {right_interval / len(values)}")
    print("\tВремя прохождения теста:", time.time() - start_time)

# Генерация случайных чисел с помощью ЛКМ
start_time = time.time()
for i in range(num_values):
    seed_value = generate_number(seed_value)
    primary_array[i] = seed_value / mod  # Преобразование значений в диапазон [0, 1]
print(f"\tВремя генерации {num_values} чисел: {time.time() - start_time}")

# Тесты для ЛКМ
test_uniqueness(primary_array)
mean_value = calculate_mean(primary_array)
variance, std_deviation = calculate_variance_and_std(primary_array, mean_value)
frequency_test(primary_array, std_deviation)
interval_probability(primary_array)



# Определение периода генератора
seed_value = 0
slow_pointer = seed_value
fast_pointer = seed_value
while True:
    slow_pointer = generate_number(slow_pointer)                # "Черепаха" движется на один шаг
    fast_pointer = generate_number(generate_number(fast_pointer))  # "Кролик" движется на два шага
    if slow_pointer == fast_pointer:
        break

cycle_start = slow_pointer
period_count = 0
while True:
    slow_pointer = generate_number(slow_pointer)
    period_count += 1
    if slow_pointer == cycle_start:
        break

print("Период генератора:", period_count)


# Генерация случайных чисел с помощью стандартного генератора NumPy
start_time = time.time()
secondary_array = np.random.rand(num_values)
print(f"\tВремя генерации {num_values} чисел: {time.time() - start_time}")

# Тесты для стандартного генератора
test_uniqueness(secondary_array)
comp_mean_value = calculate_mean(secondary_array)
comp_variance, comp_std_deviation = calculate_variance_and_std(secondary_array, comp_mean_value)
frequency_test(secondary_array, comp_std_deviation)
interval_probability(secondary_array)
