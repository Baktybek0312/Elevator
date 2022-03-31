class Elevator(object):

    def __init__(self, max_capacity=5):
        self.cur_floor = 0
        self.DOT = "Up"
        self.passengers_in_elevator_list = []
        self.cur_time = 0
        self.max_capacity = max_capacity
        self.happy_people = 0
        self.all_passenger_list = []
        self.queue_list = []
        self.action_time = 0
        self.last_check = 0
        self.top_floor = 0

    def set_cur_time(self, cur_time):
        """
        Это выполняется один раз перед началом моделирования, чтобы установить время
        """
        self.cur_time = cur_time

    def set_all_passenger_list(self, all_passenger_list):
        """
        Это выполняется один раз перед тем, как симуляция начнет создавать «список всех пассажиров»
        """
        self.all_passenger_list = all_passenger_list

    def set_passengers_in_elevator_list(self):
        """
        Это выполняется один раз перед тем, как симуляция начнет создавать пустой "список пассажиров в лифте"
        """
        self.passengers_in_elevator_list = [None for i in range(len(self.all_passenger_list))]

    def set_top_floor(self, top_floor):
        """
        Это выполняется один раз, прежде чем симуляция начнет устанавливать верхний_этаж, взятый из класса здания.
        """
        self.top_floor = top_floor

    def update_time(self):
        """
        Это используется для совершения действия, например, когда кто-то заходит в лифт, требуется больше времени
        """
        return self.action_time

    def move(self, direction):
        """
        Это перемещает лифт на 1 этажа вверх в указанном направлении (подъем на один этаж занимает 2 секунды)
        """
        if direction == "Up":
            self.cur_floor += 1
        else:
            self.cur_floor += -1

    def change_direction(self):
        """
        Метод, меняющий направление лифта
        """
        if self.DOT == "Up":
            self.DOT = "Down"
        else:
            self.DOT = "Up"

    def new_passenger(self, new_passengers_list):
        """
        Метод добавления пассажиров в лифт. Он принимает список пассажиров в качестве входных данных, и пассажиры,
        которые ждали больше всего, входят первыми, либо до тех пор, пока на этом этаже не останется людей, либо пока не будет достигнута максимальная вместимость лифта.
        """
        identities_list_still_waiting = [i.identity for i in new_passengers_list]
        identities_list_all_passengers = [i.identity for i in new_passengers_list]

        num_passengers_got_on = 0
        identities_list_people_who_got_on = []

        while len(new_passengers_list) > num_passengers_got_on and len(
                [x for x in self.passengers_in_elevator_list if x is not None]) < self.max_capacity:
            num_passengers_got_on += 1  # one more person gets in the elevator
            id_passenger_gets_on = min(identities_list_still_waiting)
            index_of_passenger_in_identities_list_all_passengers = identities_list_all_passengers.index(
                id_passenger_gets_on)
            index_of_passenger_in_identities_list_still_waiting = identities_list_still_waiting.index(
                id_passenger_gets_on)
            self.passengers_in_elevator_list[id_passenger_gets_on] = new_passengers_list[
                index_of_passenger_in_identities_list_all_passengers]
            self.passengers_in_elevator_list[id_passenger_gets_on].set_pickup_time(self.cur_time)
            identities_list_people_who_got_on.append(id_passenger_gets_on)

            del identities_list_still_waiting[index_of_passenger_in_identities_list_still_waiting]

        indeces_to_delete_from_queue_list = []  # the indeces within the queue_list with the people who got on
        for element_in_queue_list in self.queue_list:
            if element_in_queue_list[2] in identities_list_people_who_got_on:
                indeces_to_delete_from_queue_list.append(self.queue_list.index(element_in_queue_list))

        for index_to_delete_from_queue_list in range(len(indeces_to_delete_from_queue_list) - 1, -1, -1):
            del self.queue_list[indeces_to_delete_from_queue_list[index_to_delete_from_queue_list]]

        if len(new_passengers_list) > num_passengers_got_on:
            print(
                "Лифт ПОЛНЫЙ!!! Некоторые пассажиры не смогли войти!")

    def passenger_exit(self, exit_passengers_list):
        """
        Места назначения всех пассажиров, которые должны выйти на этом этаже, должны быть на этом же этаже
        """
        exit_destinations = [i.destination for i in exit_passengers_list]
        if exit_destinations != [self.cur_floor for i in range(len(exit_passengers_list))]:
            print(
                "Внимание!!! Некоторые пассажиры не хотят выходить на этом этаже!!!")
        else:
            for exit_passenger in exit_passengers_list:
                self.passengers_in_elevator_list[exit_passenger.identity].set_time_exited(
                    self.cur_time)  # set the time of drop off
            for exit_passenger in exit_passengers_list:
                self.passengers_in_elevator_list[
                    exit_passenger.identity] = None  # remove them from passengers_in_elevator_list
            self.happy_people += len(exit_passengers_list)

    def update_last_check(self):
        """
        Этот метод используется для обновления «last_check», который используется для проверки того,
        нажимали ли люди кнопку лифта с момента последней проверки.
        Это важно, потому что некоторые действия (люди заходят в лифт) требуют времени,
        и если лифт проверяет только нажатия кнопок в текущий момент времени, он пропустит те действия,
        которые произошли между последней проверкой и текущим временем.
        """
        self.last_check = self.cur_time

    def simulation(self):
        # Каждый раз происходит небольшая логистика
        # Во-первых, он восстанавливает время действия по умолчанию
        global goal
        self.action_time = 0

        # Затем он обновляет список кнопок из списка действий, добавляя все действия с момента последней проверки
        for passenger in self.all_passenger_list:
            if passenger.time_appeared > self.last_check and passenger.time_appeared <= self.cur_time:
                self.queue_list.append([passenger.pickup_floor, passenger.direction, passenger.identity])
        self.update_last_check()

        # Тогда есть пара сценариев, в которых лифт может оказаться

        # Первый сценарий: в лифте нет людей и никто не ждет лифт,
        # и лифт ждет
        if len(self.queue_list) == 0 and self.passengers_in_elevator_list == [None for i in range(len(
                self.passengers_in_elevator_list))]:
            return "The elevator is waiting"

        # Следующее, если в лифте нет людей, но есть люди, ожидающие лифта.
        # В этом случае лифт движется к самому крайнему ожидающему его по ходу движения человеку.

        elif self.passengers_in_elevator_list == [None for i in range(len(self.passengers_in_elevator_list))]:
            if self.DOT == "Up":
                temp_goal = max(item[0] for item in self.queue_list)
                if temp_goal > self.cur_floor:
                    goal = temp_goal
                elif temp_goal < self.cur_floor:
                    self.change_direction()
                    goal = min(item[0] for item in self.queue_list)
                else:
                    goal = self.cur_floor
            elif self.DOT == "Down":
                temp_goal = min(item[0] for item in self.queue_list)
                if temp_goal < self.cur_floor:
                    goal = temp_goal
                elif temp_goal > self.cur_floor:
                    self.change_direction()
                    goal = max(item[0] for item in self.queue_list)
                else:
                    goal = self.cur_floor

        # Третий случай - в лифте люди. Лифт ставит своей целью максимально
        # экстремальное направление от людей в лифте.
        else:
            if self.DOT == "Up":
                goal = max(
                    passenger.destination for passenger in [i for i in self.passengers_in_elevator_list if i != None])
            else:  # self.DOT == "Down"
                goal = min(
                    passenger.destination for passenger in [i for i in self.passengers_in_elevator_list if i != None])

        # Это определяет, как лифт движется к своей цели
        print(
            "цель =", goal)
        if goal > self.cur_floor and self.DOT == "Up":
            self.move("Up")
        elif goal > self.cur_floor and self.DOT == "Down":
            self.DOT = "Up"
            self.move("Up")
        elif goal < self.cur_floor and self.DOT == "Down":
            self.move("Down")
        elif goal < self.cur_floor and self.DOT == "Up":
            self.DOT = "Down"
            self.move("Down")
        elif goal == self.cur_floor:
            self.change_direction()

        # Если человек находится в лифте на своем этаже, он должен выйти
        getting_off = []
        for i in range(0, len(self.passengers_in_elevator_list)):
            if self.passengers_in_elevator_list[i] != None:
                if self.cur_floor == self.passengers_in_elevator_list[i].destination:
                    getting_off.append(self.passengers_in_elevator_list[i])
                    # self.passengers_in_elevator_list[i] = Нет
                    # Двери лифта открываются и закрываются за 4 секунды. В это время люди входят и выходят, поэтому, если один пассажир входит или выходит, действие займет 4 секунды.
                    self.action_time = 4
        print(
            "выходят", [i.identity for i in getting_off])
        self.passenger_exit(getting_off)

        getting_on = []
        for i in range(0, len(self.queue_list)):
            if self.cur_floor == self.queue_list[i][0] and self.DOT == self.queue_list[i][1]:
                getting_on.append(self.all_passenger_list[self.queue_list[i][2]])
                self.action_time = 4
        self.new_passenger(getting_on)

        print(
            "Список очереди", self.queue_list)
        print(
            "Текущий этаж =", self.cur_floor)
        print(
            "Пассажир в лифте=", [i.identity for i in self.passengers_in_elevator_list if i != None])
        print(
            "Счастливые люди) =", self.happy_people)

    def simulation_2(self):
        self.action_time = 0
        """ Пример стратегии. Начинается снизу, движется вверх, движется вниз, подбирая людей, когда идет их ТОЧКА """
        for passenger in self.all_passenger_list:
            if passenger.time_appeared > self.last_check and passenger.time_appeared <= self.cur_time:
                self.queue_list.append([passenger.pickup_floor, passenger.direction, passenger.identity])
        self.update_last_check()

        # Двигайтесь в правильном направлении, сначала вверх, затем вниз

        if self.DOT == "Up" and self.cur_floor != self.top_floor:
            self.move("Up")
        elif self.DOT == "Down" and self.cur_floor != 0:
            self.move("Down")
        elif self.DOT == "Up" and self.cur_floor == self.top_floor:
            self.change_direction()
        elif self.DOT == "Down" and self.cur_floor == 0:
            self.change_direction()

        getting_off = []
        for i in range(0, len(self.passengers_in_elevator_list)):
            if self.passengers_in_elevator_list[i] != None:
                if self.cur_floor == self.passengers_in_elevator_list[i].destination:
                    getting_off.append(self.passengers_in_elevator_list[i])
                    # self.passengers_in_elevator_list[i] = None
                    self.action_time = 4
        self.passenger_exit(getting_off)

        getting_on = []
        for i in range(0, len(self.queue_list)):
            if (self.cur_floor == self.queue_list[i][0] and self.DOT == self.queue_list[i][1]):
                getting_on.append(self.all_passenger_list[self.queue_list[i][2]])
                self.action_time = 4
        self.new_passenger(getting_on)

        print(
            "выходят", [i.identity for i in getting_off])
        print(
            "Список очереди", self.queue_list)
        print(
            "Текущий этаж=", self.cur_floor)
        print(
            "Пассажиры в лифте =", [i.identity for i in self.passengers_in_elevator_list if i != None])
        print(
            "Счастливые люди=", self.happy_people)
