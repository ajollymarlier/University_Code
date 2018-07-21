#Tuples are lists that cannot be modified unless converted back to list
newTuple = (5, 4, 3, 2, 1)

print(newTuple)

listTuple = list(newTuple)
listTuple[2] = 100
print(listTuple)

newTuple = tuple(listTuple)
print(newTuple)

def printValues(object):
    for i in range(len(object)):
        print(object[i])
