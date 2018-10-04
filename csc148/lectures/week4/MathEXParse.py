from typing import Any

class Stack:
    def __init__(self):
        self._items = []

    def push(self, thing: Any) -> None:
        self._items.append(thing)

    def pop(self) -> Any:
        item = self._items[len(self._items) - 1]
        del self._items[len(self._items) - 1]
        return item

    def is_empty(self) -> bool:
        if len(self._items) == 0:
            return True
        else:
            False


def check_expression(user_in: str) -> bool:
    '''Return true or false based on if
    mathematical expression has balanced parentheses

    '''
    stack = Stack()

    expression = user_in
    for x in expression:
        if x == ")":
            popped_el = stack.pop()

            while not popped_el == "(":
                if stack.is_empty():
                    return False
                else:
                    popped_el = stack.pop()

        else:
            stack.push(x)

    if stack.is_empty():
        return True
    else:
        return False


if __name__ == "__main__":
    print(check_expression(input("Write Expression: ")))
