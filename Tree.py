class Node(object):
    def __init__(self, value, leftNode, rightNode, prev):
        self.value = value
        self.leftNode = leftNode
        self.rightNode = rightNode
        self.prev = prev

    def addChild(self, node, dir):
        if dir == 0:
            self.leftNode = node
        else:
            self.rightNode = node

    def getLeft(self):
        return self.leftNode

    def getRight(self):
        return self.rightNode

    def getPrev(self):
        return self.prev

    def getValue(self):
        return self.value


class Tree(object):
    def __init__(self, currNode):
        self.currNode = currNode

    def traverse(self, i):
        self.currNode = self.currNode.children[i]

    def reverse(self):
        self.currNode = self.currNode.prev

    def showStructure(self):
        self.findNodes(self.currNode)

    def findNodes(self, node):
        if self.leftNode is None and self.rightNode is None:
            print("Hello")
            


