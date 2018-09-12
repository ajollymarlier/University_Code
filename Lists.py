goodList = list()

goodList.append(31)

goodList.insert(0, 'Hello')
print(goodList)

goodList[1] = "Goodbye"
print(goodList)

goodList.remove("Goodbye")

for x in goodList:
    print(x)

goodList.pop()
print(goodList)

goodList.clear()

del goodList

