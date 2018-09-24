'''
Module for race registry lab2 project
Last Edited: 9/21/2018
'''

from typing import List


class Runner:
    """
    A runner participating in the race

    === Attributes ===

    name: the name of the race contestant
    email: email address of race contestant
    speed_category: speed bracket in which runner falls based on running time

    === Representation Invariants ===
    speed_category must be one of four ints,

    0 = < 20 minutes
    1 = < 30 minutes
    2 = < 40 minutes
    3 = > 40 minutes

    === Sample Usage ===

    >>> r = Runner('Mike', 'mike_mike.com', 0)
    >>> r.name
    'Mike'
    >>> r.email
    'mike_mike.com'
    >>> r.speed_category
    0

    """

    #Attribute Types
    name: str
    email: str
    speed_category: int

    def __init__(self, name: str, email: str, speed_category: int) -> None:
        """
        Initialize a new runner object.

        >>> r = Runner( 'Mike', 'mike_mike.com', 0)
        >>> r.name
        'Mike'
        >>> r.email
        'mike_mike.com'
        >>> r.speed_category
        0
        """

        self.name = name
        self.email = email
        self.speed_category = speed_category

    def change_email(self, new_email: str) -> None:
        """
        Changes the Runner's email

        >>> r = Runner('Mike', 'mike_mike.com', 0)
        >>> r.email
        'mike_mike.com'
        >>> r.change_email("arun_arun.com")
        >>> r.email
        'arun_arun.com'
        """

        self.email = new_email

    def change_speed_category(self, new_category: int) -> None:
        """
        change the Runner's speed category

        >>> r = Runner('Mike', 'mike_mike.com', 0)
        >>> r.speed_category
        0
        >>> r.change_speed_category(2)
        >>> r.speed_category
        2
        """
        self.speed_category = new_category


class Race:
    """
    A race that is being held

    === Attributes ===
    runners: A dictionary of runners competing in the race

    === Sample Usage ===
    >>> race = Race()
    >>> race.runners
    {}

    """

    #Attribute Types
    runners: List[Runner]

    def __init__(self) -> None:
        """

        Creates a new race with an empty dictionary of Runners

        """
        self.runners = {}

    def register(self, runner: Runner) -> None:
        """

        Adds given Runner to runners dictionary with the key
        being the runner's name

        >>> race = Race()
        >>> race.register(Runner("Arun", "arun_arun.com", 0))
        >>> race.runners["Arun"].name
        'Arun'
        >>> race.runners["Arun"].email
        'arun_arun.com'
        >>> race.runners["Arun"].speed_category
        0

        """
        self.runners[runner.name] = runner

    def withdraw(self, runner_name: str) -> None:
        """
        Deletes a Runner with key runner_name from runners dictionary

        >>> race = Race()
        >>> race.register(Runner("Arun", "arun_arun.com", 0))
        >>> race.withdraw("Arun")
        >>> race.runners
        {}

        """
        del self.runners[runner_name]

    def get_runners_in_category(self, speed_category: int) -> List[Runner]:
        """

        Returns a list of all runners in a given speed_category

        >>> race = Race()
        >>> race.runners["Arun"] = Runner("Arun", "arun_arun.com", 0)
        >>> race.runners["Mike"] = Runner("Mike", "mike_mike.com", 0)
        >>> race.get_runners_in_category(0)[0].name
        'Arun'
        >>> race.get_runners_in_category(0)[1].name
        'Mike'

        """

        same_speed_runners = []
        for x, y in self.runners.items():
            if y.speed_category == speed_category:
                same_speed_runners.append(self.runners[x])

        return same_speed_runners


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Optionally, check your work with python_ta!
    import python_ta
    python_ta.check_all(config={'extra-imports': ['datetime']})
