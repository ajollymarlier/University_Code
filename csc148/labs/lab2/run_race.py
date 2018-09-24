from labs.lab2.registry import Race, Runner

if __name__ == '__main__':
    race = Race()

    arun = Runner('Arun', 'arun@arun.com', 0)
    race.register(arun)
    print(f'{race.get_runners_in_category(0)[0].name}, '
          f'{race.get_runners_in_category(0)[0].email}, '
          f'{race.get_runners_in_category(0)[0].speed_category}')

    race.register(Runner('David', 'david@david.com', 2))
    race.register(Runner("Mike", 'mike@mike.com', 2))

    for x in race.get_runners_in_category(2):
        print(f'{x.name}, {x.email}, {x.speed_category}')

    race.withdraw('Mike')
    arun.change_email("arun@gmail.com")
    arun.change_speed_category(3)

    for x in race.get_runners_in_category(2):
        print(f'{x.name}, {x.email}, {x.speed_category}')

        print(f'{race.get_runners_in_category(3)[0].name}, '
              f'{race.get_runners_in_category(3)[0].email}, '
              f'{race.get_runners_in_category(3)[0].speed_category}')
