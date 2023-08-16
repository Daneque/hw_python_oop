
# Константа для перевода метров в километры.
KMH_IN_MS = 0.06
SM_IN_M = 0.01


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float, distance: float,
                 speed: float, calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

# Длина одного шага в метрах.
    LEN_STEP = 0.65
    M_IN_KM = 1000
    HOURS_IN_MINUTES = 60

    def __init__(self, action: int, duration: float, weight: float):
        self.action = action
        self.duration = duration
        self.weight = weight

# Возвращает дистанцию (в километрах), которую преодолел пользователь
    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * self.HOURS_IN_MINUTES)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    FIRST_PARAMETER = 0.035
    SECOND_PARAMETER = 0.029

    def __init__(self, action: int, duration: float,
                 weight: float, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (((self.FIRST_PARAMETER * self.weight)
                + ((self.get_mean_speed() * KMH_IN_MS)**2 / self.height
                * SM_IN_M) * self.SECOND_PARAMETER * self.weight)
                * self.duration * self.HOURS_IN_MINUTES)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    FIRST_PARAMETER = 1.1
    SECOND_PARAMETER = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM) / self.duration

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.FIRST_PARAMETER)
                * self.SECOND_PARAMETER
                * self.weight * self.duration)


training_codes: dict[str: Training] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type in training_codes:
        return training_codes[workout_type](*data)
    raise Exception('Workout type not in list')


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

    test = Running(1206, 12, 6)
    print(test.get_spent_calories())