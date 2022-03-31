import random
import numpy as np

from elevator import Elevator
from passenger import Building, Passenger

result_5 = []

random.seed(1)
np.random.seed(1)

counter = 0
sims_10 = []

"""
Создание Здания, которое называется Дома (название нашей резиденции в Хайдарабаде).
distribution_of_people говорит нам, что вероятность того, что человек поедет на 0-й этаж или с него, 
будет в 6 раз выше, чем на любой другой этаж. Кроме того, существует одинаковая вероятность того, 
что человек поедет на/с i-го этажа по сравнению с j-м этажом, когда i и j положительны.
"""
while counter < 10:
    At_Home = Building(
        distribution_of_people=[220, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                                10], total_num_passengers=20)

    num_floors = At_Home.get_floors()
    distribution = At_Home.get_distribution()
    num_passengers = At_Home.get_total_num_passengers()

    distribution = [float(distribution[i]) / sum(distribution) for i in range(len(distribution))]
    pickup_locations = np.random.choice(range(num_floors), num_passengers, p=distribution)

    destinations = []

    for index_passenger in range(num_passengers):
        distribution_without_passenger = [a for a in distribution]
        range_without_passenger = list(range(num_floors))

        del range_without_passenger[pickup_locations[index_passenger]]

        del distribution_without_passenger[pickup_locations[index_passenger]]

        distribution_without_passenger = [float(distribution_without_passenger[i]) / sum(distribution_without_passenger)
                                          for i in range(len(distribution_without_passenger))]

        destinations.append(np.random.choice(range_without_passenger, 1, p=distribution_without_passenger)[0])

    average_delay = 40.0

    delays = np.random.poisson(lam=10 * average_delay, size=num_passengers - 1)
    delays = [(i - 9 * average_delay) * ((i - 9 * average_delay) > 0) for i in delays]

    times_of_arrival = [3.]

    for i in range(num_passengers - 1):
        times_of_arrival.append(times_of_arrival[i] + delays[i])

    passenger_list = []
    for i in range(num_passengers):
        passenger_list.append(
            Passenger(time_appeared=times_of_arrival[i], destination=destinations[i], pickup_floor=pickup_locations[i],
                      identity=i))

    cur_time = 0.

    elevator = Elevator()
    elevator.set_all_passenger_list(passenger_list)
    elevator.set_passengers_in_elevator_list()
    elevator.set_top_floor(num_floors - 1)

    print(
        "Время появления:", [i.time_appeared for i in passenger_list])
    print(
        "Подобран с этажа:", [i.pickup_floor for i in passenger_list])
    print(
        "Направления:", [i.destination for i in passenger_list])
    print(
        "IDs:", [i.identity for i in passenger_list])

    while num_passengers != elevator.happy_people:
        elevator.set_cur_time(cur_time)
        elevator.simulation_2()
        cur_time += elevator.update_time()
        cur_time += 0.5
        print(
            "Текущее время:", cur_time)

    counter += 1
    sims_10.append(passenger_list)

results_5 = sims_10


def results(lis, name):
    """
    Это можно запустить, чтобы получить сводку результатов запуска симуляции
    """
    print(
        "Среднее время от", name, sum(lis) / float(len(lis)))
    print(
        "Максимальное время от»", name, max(lis))
    print(
        "медиану времени от", name, np.median(np.array(lis)))
    print(
        "__________\n")


def print_results(simulation_10_list, label):
    """
    Это основная функция результатов, она принимает список длиной 100 и выводит соответствующие результаты
    Мы запускаем эту функцию для 8 списков из 100, содержащихся в списке результатов.
    """
    pushing_to_arrival = []
    wait_for_elevator = []
    wait_in_elevator = []

    for j in range(0, len(simulation_10_list)):
        for i in simulation_10_list[j]:
            wait_for_elevator.append(i.get_pickup_time() - i.get_time_appeared())
            wait_in_elevator.append(i.get_time_exited() - i.get_pickup_time())
            pushing_to_arrival.append(i.get_time_exited() - i.get_time_appeared())

    print(
        label)
    print(
        "Показатели эффективности:")
    print(
        "__________\n")

    results(wait_for_elevator, "начали подниматься в лифте:")
    results(wait_in_elevator, "вход в лифт до места назначения:")
    results(pushing_to_arrival, "нажатие кнопки, чтобы добраться до пункта назначения:")