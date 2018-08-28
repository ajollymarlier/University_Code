class Vehicle():
    def __init__(self, name):
        self.name = name

    def beep(self):
        print(self.name + " goes beep!")

class Car(Vehicle):
    def __init__(self, name):
        self.name = name

meep = Car("Bugel")
meep.beep()