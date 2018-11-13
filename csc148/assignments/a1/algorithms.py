"""CSC148 Assignment 1 - Algorithms

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===

This file contains two sets of algorithms: ones for generating new arrivals to
the simulation, and ones for making decisions about how elevators should move.

As with other files, you may not change any of the public behaviour (attributes,
methods) given in the starter code, but you can definitely add new attributes
and methods to complete your work here.

See the 'Arrival generation algorithms' and 'Elevator moving algorithsm'
sections of the assignment handout for a complete description of each algorithm
you are expected to implement in this file.
"""
import csv
from enum import Enum
import random
from typing import Dict, List, Optional

from entities import Person, Elevator


###############################################################################
# Arrival generation algorithms
###############################################################################
class ArrivalGenerator:
    """An algorithm for specifying arrivals at each round of the simulation.

    === Attributes ===
    max_floor: The maximum floor number for the building.
               Generated people should not have a starting or target floor
               beyond this floor.
    num_people: The number of people to generate, or None if this is left
                up to the algorithm itself.

    === Representation Invariants ===
    max_floor >= 2
    num_people is None or num_people >= 0
    """
    max_floor: int
    num_people: Optional[int]

    def __init__(self, max_floor: int, num_people: Optional[int]) -> None:
        """Initialize a new ArrivalGenerator.

        Preconditions:
            max_floor >= 2
            num_people is None or num_people >= 0
        """
        self.max_floor = max_floor
        self.num_people = num_people

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Return the new arrivals for the simulation at the given round.

        The returned dictionary maps floor number to the people who
        arrived starting at that floor.

        You can choose whether to include floors where no people arrived.
        """
        raise NotImplementedError


class RandomArrivals(ArrivalGenerator):
    """Generate a fixed number of random people each round.

    Generate 0 people if self.num_people is None.

    For our testing purposes, this class *must* have the same initializer header
    as ArrivalGenerator. So if you choose to to override the initializer, make
    sure to keep the header the same!

    Hint: look up the 'sample' function from random.
    """

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Return the new arrivals for the simulation at the given round.

        The returned dictionary maps floor number to the people who
        arrived starting at that floor.

        You can choose whether to include floors where no people arrived.
        """
        arriving_people = dict()
        arriving_people[round_num] = []

        # Creates a list 2 * the length of generations with each pair
        # representing a person with start and end values
        if self.num_people is not None:
            people_info = random.sample(range(1, self.max_floor),
                                        self.num_people * 2)

            i = 0
            while i < len(people_info):
                arriving_people[round_num].append(Person(people_info[i],
                                                         people_info[i + 1]))
                i += 2

            return arriving_people

        else:
            return arriving_people


class FileArrivals(ArrivalGenerator):
    """Generate arrivals from a CSV file.
    === Attributes ===
        file_lines: List of lines from file
    """

    file_lines: List[List[str]]

    def __init__(self, max_floor: int, filename: str) -> None:
        """Initialize a new FileArrivals algorithm from the given file.

        The num_people attribute of every FileArrivals instance is set to None,
        since the number of arrivals depends on the given file.

        Precondition:
            <filename> refers to a valid CSV file, following the specified
            format and restrictions from the assignment handout.

        """

        ArrivalGenerator.__init__(self, max_floor, None)
        self.file_lines = list()

        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                # <line> is a list of strings corresponding
                # to one line of the original file.
                # You'll need to convert the strings to ints and then process
                # and store them.
                self.file_lines.append(line)

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        # Instantiates and populates dict with empty list for each round num
        # i + 1 b/c first floor is at 1
        arriving_people = dict()
        arriving_people[round_num] = []

        for line in self.file_lines:
            if len(line) > 0 and int(line[0]) == round_num:
                i = 1
                while i < len(line):
                    arriving_people[round_num].append(
                        Person(int(line[i]), int(line[i + 1])))
                    i += 2

        return arriving_people


###############################################################################
# Elevator moving algorithms
###############################################################################
class Direction(Enum):
    """
    The following defines the possible directions an elevator can move.
    This is output by the simulation's algorithms.

    The possible values you'll use in your Python code are:
        Direction.UP, Direction.DOWN, Direction.STAY
    """
    UP = 1
    STAY = 0
    DOWN = -1


class MovingAlgorithm:
    """An algorithm to make decisions for moving an elevator at each round.
    """
    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.

        As input, this method receives the list of elevators in the simulation,
        a dictionary mapping floor number to a list of people waiting on
        that floor, and the maximum floor number in the simulation.

        Note that each returned direction should be valid:
            - An elevator at Floor 1 cannot move down.
            - An elevator at the top floor cannot move up.
        """
        raise NotImplementedError


class RandomAlgorithm(MovingAlgorithm):
    """A moving algorithm that picks a random direction for each elevator.
    """
    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        directions = list()
        for elevator in elevators:
            chosen_dir = None

            if elevator.floor == max_floor:
                chosen_dir = random.choice([Direction.DOWN, Direction.STAY])

            elif elevator.floor == 1:
                chosen_dir = random.choice([Direction.STAY, Direction.UP])

            else:
                chosen_dir = random.choice([Direction.DOWN,
                                            Direction.STAY, Direction.UP])

            directions.append(chosen_dir)
            elevator.floor += chosen_dir.value

        return directions


class PushyPassenger(MovingAlgorithm):
    """A moving algorithm that preferences the first passenger on each elevator.

    If the elevator is empty, it moves towards the *lowest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the target floor of the
    *first* passenger who boarded the elevator.
    """
    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        directions = list()
        for elevator in elevators:

            if len(elevator.passengers) == 0:
                elevator_target_floor = None

                for i in range(1, max_floor + 1):

                    if len(waiting[i]) != 0:
                        elevator_target_floor = i
                        break

                # Don't have to worry about same
                # floor case because everyone would leave
                # Also don't have to worry about out of bounds case
                # because floors are limited by person target RI
                if elevator_target_floor is None:
                    directions.append(Direction.STAY)

                elif elevator.floor < elevator_target_floor:
                    directions.append(Direction.UP)
                    elevator.floor += 1

                elif elevator.floor > elevator_target_floor:
                    directions.append(Direction.DOWN)
                    elevator.floor -= 1

            else:
                # Same as above comment in if/elif/else block
                if elevator.floor < elevator.passengers[0].target:
                    directions.append(Direction.UP)
                    elevator.floor += 1

                elif elevator.floor > elevator.passengers[0].target:
                    directions.append(Direction.DOWN)
                    elevator.floor -= 1

                else:
                    directions.append(Direction.STAY)

        return directions


class ShortSighted(MovingAlgorithm):
    """A moving algorithm that preferences the closest possible choice.

    If the elevator is empty, it moves towards the *closest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the closest target floor of
    all passengers who are on the elevator.

    In this case, the order in which people boarded does *not* matter.
    """
    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        directions = list()
        for elevator in elevators:

            if len(elevator.passengers) == 0:
                closest_floor = max_floor * elevator.floor + 1

                # Checks floors below elevator floor
                i = elevator.floor - 1
                while i >= 1:
                    if len(waiting[i]) != 0:
                        closest_floor = i
                        break

                    i -= 1

                # Checks floors above elevator floor
                i = elevator.floor + 1
                while i <= max_floor:
                    if len(waiting[i]) != 0 and abs(elevator.floor - i) <\
                                abs(elevator.floor - closest_floor):
                        closest_floor = i
                        break

                    i += 1

                # Adds directions to list
                if closest_floor == max_floor * elevator.floor + 1 \
                        or elevator.floor == max_floor:
                    directions.append(Direction.STAY)

                elif elevator.floor < closest_floor:
                    directions.append(Direction.UP)
                    elevator.floor += 1

                elif elevator.floor > closest_floor:
                    directions.append(Direction.DOWN)
                    elevator.floor -= 1

            else:
                closest_floor = elevator.floor * max_floor
                for person in elevator.passengers:

                    if abs(person.target - elevator.floor) < \
                            abs(closest_floor - elevator.floor):
                        closest_floor = person.target

                    elif abs(person.target - elevator.floor) == \
                            abs(closest_floor - elevator.floor):
                        closest_floor = min(closest_floor, person.target)


                # Adds directions to list
                if closest_floor > max_floor:
                    directions.append(Direction.STAY)

                elif elevator.floor < closest_floor:
                    directions.append(Direction.UP)
                    elevator.floor += 1

                elif elevator.floor > closest_floor:
                    directions.append(Direction.DOWN)
                    elevator.floor -= 1

        return directions


if __name__ == '__main__':
    # Don't forget to check your work regularly with python_ta!
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['__init__'],
        'extra-imports': ['entities', 'random', 'csv', 'enum'],
        'max-nested-blocks': 4,
        'max-attributes': 12,
        'disable': ['R0201']
    })
