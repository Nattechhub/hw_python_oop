from dataclasses import dataclass, asdict
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    text = (
        'Тип тренировки: {}; '
        'Длительность: {:.3f} ч.; '
        'Дистанция: {:.3f} км; '
        'Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.')

    def get_message(self) -> None:
        text_1 = asdict(self)
        return self.text.format(*text_1.values())


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60
    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20
    K_1 = 0.035
    K_2 = 0.029
    K_3 = 2
    K_4 = 1.1

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self):
        return ((
                self.COEFF_CALORIE_1
                * self.get_mean_speed()
                - self.COEFF_CALORIE_2)
                * self.weight
                / self.M_IN_KM
                * (self.duration
                * self.MIN_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int, duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        min_duration = self.duration * self.MIN_IN_HOUR
        weigh = self.weight
        heigh = self.height
        return ((self.K_1
                * weigh
                + (self.get_mean_speed()**self.K_3 // heigh)
                * self.K_2
                * weigh)
                * min_duration)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + self.K_4) * self.K_3 * self.weight


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    train_class = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking}
    if workout_type in train_class:
        return train_class[workout_type](*data)
    else:
        raise ValueError('Некорректные данные')


def main(my_training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = my_training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
