"""CSC148 Assignment 1 - Simulation

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This contains the main Simulation class that is actually responsible for
creating and running the simulation. You'll also find the function `sample_run`
here at the bottom of the file, which you can use as a starting point to run
your simulation on a small configuration.

Note that we have provided a fairly comprehensive list of attributes for
Simulation already. You may add your own *private* attributes, but should not
remove any of the existing attributes.
"""
# You may import more things from these modules (e.g., additional types from
# typing), but you may not import from any other modules.
from typing import Dict, List, Any

import algorithms
from algorithms import Direction
from entities import Person, Elevator
from visualizer import Visualizer


class Simulation:
    """The main simulation class.

    === Attributes ===
    arrival_generator: the algorithm used to generate new arrivals.
    elevators: a list of the elevators in the simulation
    moving_algorithm: the algorithm used to decide how to move elevators
    num_floors: the number of floors
    visualizer: the Pygame visualizer used to visualize this simulation
    waiting: a dictionary of people waiting for an elevator
             (keys are floor numbers, values are the list of waiting people)

    _num_iterations: number of rounds processed in simulation
    _total_people: total amount of people arriving in simulation
    _people_completed: total amount of people picked up and dropped
                        off at target floor
    _max_time: maximum time spent waiting
    _min_time: minimum time spent waiting
    _wait_times: list of all people's wait times.
                    Will be used to calculate avg_time

    === Representation Invariants ===
    num_floors >= 2
    num_elevators >= 1
    elevator_capacity >= 1

    _max_time >= 0 and <= 15
    _min_time >= 0 and <= 15
    """
    # Running Attributes
    arrival_generator: algorithms.ArrivalGenerator
    elevators: List[Elevator]
    moving_algorithm: algorithms.MovingAlgorithm
    num_floors: int
    visualizer: Visualizer
    waiting: Dict[int, List[Person]]

    # Stat Attributes
    _num_iterations: int
    _total_people: int
    _people_completed: int
    _max_time: int
    _min_time: int
    _wait_times: List[int]

    def __init__(self,
                 config: Dict[str, Any]) -> None:
        """Initialize a new simulation using the given configuration."""

        # Running Attributes
        self.arrival_generator = config['arrival_generator']
        self.elevators = []
        self.moving_algorithm = config['moving_algorithm']
        self.num_floors = config['num_floors']
        self.waiting = {}

        # Stat Attributes
        self._num_iterations = 0  # updated in self.run
        self._total_people = 0  # changed in self._generate_arrivals()
        self._people_completed = 0  # changed in self._handle_leaving()
        self._max_time = 0  # This and below update in self.handle_leaving()
        self._min_time = 16  # 1 + num_rounds so first occurrence is always min
        self._wait_times = list()  # updates in self._handle_leaving()

        # Populates waiting with empty lists for every floor_num
        # i + 1 b/c first floor is 1
        for i in range(self.num_floors):
            self.waiting[i + 1] = []

        # Populates self.elevators with number if elevators needed
        i = 0
        while i < config['num_elevators']:
            self.elevators.append(Elevator(config['elevator_capacity']))
            i += 1

        # Initialize the visualizer.
        # Note that this should be called *after* the other attributes
        # have been initialized.
        self.visualizer = Visualizer(self.elevators,
                                     self.num_floors,
                                     config['visualize'])

    ############################################################################
    # Handle rounds of simulation.
    ############################################################################
    def run(self, num_rounds: int) -> Dict[str, Any]:
        """Run the simulation for the given number of rounds.

        Return a set of statistics for this simulation run, as specified in the
        assignment handout.

        Precondition: num_rounds >= 1.

        Note: each run of the simulation starts from the same initial state
        (no people, all elevators are empty and start at floor 1).
        """
        for i in range(num_rounds):
            self.visualizer.render_header(i)

            # Stage 1: generate new arrivals
            self._generate_arrivals(i)

            # Stage 2: leave elevators
            self._handle_leaving()

            # Stage 3: board elevators
            self._handle_boarding()

            # Stage 4: move the elevators using the moving algorithm
            self._move_elevators()

            # Pause for 1 second and increment _num_iterations
            self.visualizer.wait(1)
            self._num_iterations += 1

        self._add_times_in_elevator()
        return self._calculate_stats()

    def _add_times_in_elevator(self) -> None:
        """Adds wait times for people in elevator at end of sim and
        adjusts _max_time and _min_time accordingly"""
        for elevator in self.elevators:
            for person in elevator.passengers:
                self._wait_times.append(person.wait_time)

                if person.wait_time > self._max_time:
                    self._max_time = person.wait_time

                if person.wait_time < self._min_time:
                    self._min_time = person.wait_time

    def _generate_arrivals(self, round_num: int) -> None:
        """Gets dictionary with {start_floor : Person(start, target) and
        adds each element to waiting dict at start"""

        arrivals = self.arrival_generator.generate(round_num)[round_num]
        for i in range(len(arrivals)):
            self.waiting[arrivals[i].start].append(arrivals[i])

        self._total_people += len(arrivals)  # adds to _total_people
        self.visualizer.show_arrivals(self.waiting)

    def _handle_leaving(self) -> None:
        """Handle people leaving elevators."""
        for elevator in self.elevators:
            for person in elevator.passengers:

                if elevator.floor == person.target:
                    elevator.passengers.remove(person)
                    self._people_completed += 1  # Increments _people_completed

                    # Updates _min_time
                    if person.wait_time < self._min_time:
                        self._min_time = person.wait_time

                    # Updates max_time
                    if person.wait_time > self._max_time:
                        self._max_time = person.wait_time

                    # Updates wait_times and calls visualizer
                    self._wait_times.append(person.wait_time)
                    self.visualizer.show_disembarking(person, elevator)

    def _handle_boarding(self) -> None:
        """Handle boarding of people and visualize."""
        for floor in self.waiting:
            arrivals_at_floor = self.waiting[floor]
            self._load_elevators(floor, arrivals_at_floor)

            # Updates wait_time for all people waiting
            for person in arrivals_at_floor:
                person.wait_time += 1

        # Updates wait_time for all people in elevators
        for elevator in self.elevators:
            for person in elevator.passengers:
                person.wait_time += 1

    # Self-created Helper Method
    def _load_elevators(self, curr_floor: int,
                        arrivals_at_floor: List[Person]) -> None:
        """Helper method to handle loading of elevators"""
        for i in range(len(arrivals_at_floor)):

            for j in range(len(self.elevators)):
                try:
                    while self.elevators[j].fullness() < 1.0 \
                            and self.elevators[j].floor == curr_floor:

                        person_boarding = arrivals_at_floor.pop(i)
                        self.elevators[j].passengers.append(person_boarding)

                        self.visualizer.show_boarding(person_boarding,
                                                      self.elevators[j])
                except IndexError:
                    pass

    def _move_elevators(self) -> None:
        """Move the elevators in this simulation.

        Use this simulation's moving algorithm to move the elevators.
        """
        directions = self.moving_algorithm.move_elevators(
            self.elevators, self.waiting, self.num_floors)

        self.visualizer.show_elevator_moves(self.elevators, directions)

    ############################################################################
    # Statistics calculations
    ############################################################################
    def _calculate_stats(self) -> Dict[str, int]:
        """Report the statistics for the current run of this simulation.
        """
        return {
            'num_iterations': self._num_iterations,
            'total_people': self._total_people,
            'people_completed': self._people_completed,
            'max_time': self._max_time,
            'min_time': self._min_time,
            'avg_time': self._get_avg_time()
        }

    def _get_avg_time(self) -> int:
        """Helper method to calculate the avg
        wait time of all people in simulation"""
        total_time = 0
        for time in self._wait_times:
            total_time += time

        if len(self._wait_times) > 0:
            return total_time // len(self._wait_times)

        else:
            return 0


def sample_run() -> Dict[str, int]:
    """Run a sample simulation, and return the simulation statistics."""
    config = {
        'num_floors': 6,
        'num_elevators': 6,
        'elevator_capacity': 3,
        'num_people_per_round': 2,
        # File arrival from "sample_arrivals.csv"
        'arrival_generator': algorithms.FileArrivals(6, "sample_arrivals.csv"),
        'moving_algorithm': algorithms.RandomAlgorithm(),
        'visualize': True
    }

    sim = Simulation(config)
    stats = sim.run(15)
    return stats


if __name__ == '__main__':
    # Uncomment this line to run our sample simulation (and print the
    # statistics generated by the simulation).
    print(sample_run())

    """import python_ta
    python_ta.check_all(config={
        'extra-imports': ['entities', 'visualizer', 'algorithms', 'time'],
        'max-nested-blocks': 4,
        'max-attributes': 12,
        'disable': ['R0201']
    })"""
