from typing import List, Tuple
from __future__ import annotations


class Car:
    def __init__(self, model):
        self.model = model

    def say_hi(self, name: str) -> None:
        '''
        This function returns a phrase that states the user by given name and
        then states what model of car this object is

        :param name: Name of the user asking the car to say hi
        :return: None
        '''

        print(f'Hello {name}! I am a {self.model}!')


def neg_pos(numbers: List[int]) -> Tuple[List[int], List[int]]:
    pos = []
    neg = []

    for n in numbers:
        if n < 0:
            neg.append(n)

        else:
            pos.append(n)

    return pos, neg


car = Car("Lambo")
car.say_hi("Arun")
print(neg_pos([-1, 1, -2, 2, -3, 3, -4, 4]))
