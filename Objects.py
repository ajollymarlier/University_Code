import os

class Car:
    def __init__(self, speed, color):
        self.speed = speed
        self.color = color

    def sayState(self):
        print("My color is {} and I'm going {}km/h".format(self.color, self.speed))

    def setSpeed(self, speed):
        self.speed = speed

    def setColor(self, color):
        self.color = color;

    def getSpeed(self):
        return self.speed

    def getColor(self):
        return self.color

    def accelerate(self):
        self.speed += 2

    def deccelerate(self):
        self.speed -= 2;

class Lambo(Car):
    __rapper = " "

    def __init__(self, speed, color, rapper):
        Car.__init__(self, speed, color)
        self.__rapper = rapper



def doStuff():
    myCar = Car(int(input("Enter a starting speed: ")), input("Enter a color: "))

    myCar.deccelerate()
    myCar.sayState()

    for i in range(11):
        myCar.accelerate()

    myCar.sayState()

    clearAnswer = input("Clear Console? (Y/N)")

    if clearAnswer.upper() == "Y":
        os.system('cls')

    huracan = Lambo(4, "Purple", "KSI")
    huracan.deccelerate()

    print(huracan.getColor())
    print(huracan.getSpeed())

doStuff()











