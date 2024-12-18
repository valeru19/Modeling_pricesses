import math
import random

# Параметры модели
arrival_rate = 25  # Плотность потока заявок (клиентов в час)
num_cashiers = 10   # Кол-во касс
service_time = 0.055  # Среднее время обслуживания одного покупателя на кассе (в часах)
store_hours = 1200  # Время работы магазина в минутах
num_simulations = 10000  # Кол-во симуляций для усреднения результатов

# Массивы для хранения статистики
served_customers = [0] * (num_cashiers + 1)  # Массив обслуженных клиентов на каждой кассе и потерянных клиентов
cashier_status = [0] * num_cashiers  # Время, когда каждая касса станет свободной
customer_counter = [0] * (num_cashiers + 1)  # Счетчики обслуженных клиентов на каждой кассе и потерянных клиентов
service_shares = [0.0] * (num_cashiers + 1)  # Средние доли обслуживания клиентов и потерь


#Генерация веремени с экспоненциальным распределением
def generate_exponential_random(value):
    return -1 / arrival_rate * math.log(value)


# Основной алгоритм
for _ in range(num_simulations):
    current_time = 0  # Начальное время симуляции

    # Моделируем поступление клиентов
    while current_time <= store_hours:
        # Генерация времени прихода следующего клиента
        current_time += generate_exponential_random(random.random())

        # Находим свободную кассу
        free_cashier = -1
        for cashier_index in range(len(cashier_status)):
            if cashier_status[cashier_index] < current_time:
                free_cashier = cashier_index  # Если касса свободна, записываем её индекс
                break

        # Если касс нет свободных, увеличиваем счетчик потерянных клиентов
        if free_cashier == -1:
            served_customers[num_cashiers] += 1
        else:
            served_customers[free_cashier] += 1     # Если касса свободна, увеличиваем счетчик обслуженных клиентов

            cashier_status[free_cashier] = current_time + service_time      # Устанавливаем время, когда касса освободится

    # Накопление результатов по всем симуляциям
    for i in range(len(served_customers)):
        customer_counter[i] += served_customers[i]

    # Сброс для следующей симуляции
    served_customers = [0] * (num_cashiers + 1)
    cashier_status = [0] * num_cashiers

# Расчет долей обслуживания и потерь
for i in range(len(customer_counter)):
    service_shares[i] = customer_counter[i] / num_simulations

# Вывод результатов
total_served = sum(service_shares)  # Общая доля всех обслуженных и потерянных клиентов
print("Нагруженность касс:")
for i in range(len(service_shares) - 1):
    print(f"{i + 1}.\t{service_shares[i]:.2f}\t( {service_shares[i] / total_served * 100:.2f}% )")

# Доля потерянных клиентов
print(f"Потерянные покупатели:\n1.\t{service_shares[-1]:.2f}\t( {service_shares[-1] / total_served * 100:.2f}% )")
