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

    === Representation Invariants ===
    num_floors >= 2
    num_elevators >= 1
    elevator_capacity >= 1
    """
    arrival_generator: algorithms.ArrivalGenerator
    elevators: List[Elevator]
    moving_algorithm: algorithms.MovingAlgorithm
    num_floors: int
    visualizer: Visualizer
    waiting: Dict[int, List[Person]]

    def __init__(self,
                 config: Dict[str, Any]) -> None:
        """Initialize a new simulation using the given configuration."""

        self.arrival_generator = config['arrival_generator']
        self.elevators = []
        self.moving_algorithm = config['moving_algorithm']
        self.num_floors = config['num_floors']
        self.waiting = {}

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

            # Pause for 1 second
            self.visualizer.wait(1)

        return self._calculate_stats()

    def _generate_arrivals(self, round_num: int) -> None:
        """Gets dictionary with {start_floor : Person(start, target) and
        adds each element to waiting dict at start"""

        arrivals = self.arrival_generator.generate(round_num)[round_num]
        for i in range(len(arrivals)):
            self.waiting[arrivals[i].start].append(arrivals[i])

        self.visualizer.show_arrivals(self.waiting)

    # TODO are the sprites supposed to disappear after leaving?
    def _handle_leaving(self) -> None:
        """Handle people leaving elevators."""
        for elevator in self.elevators:
            for person in elevator.passengers:

                if elevator.floor == person.target:
                    elevator.passengers.remove(person)
                    self.visualizer.show_disembarking(person, elevator)

    def _handle_boarding(self) -> None:
        """Handle boarding of people and visualize."""
        for floor in self.waiting:
            arrivals_at_floor = self.waiting[floor]
            self._load_elevators(floor, arrivals_at_floor)

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
            'num_iterations': 0,
            'total_people': 0,
            'people_completed': 0,
            'max_time': 0,
            'min_time': 0,
            'avg_time': 0
        }


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
        'max-nested-blocks': 4
    })"""
