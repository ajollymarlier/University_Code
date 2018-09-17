from typing import List

def insert_value(lst: List[int], n1: int, n2: int) -> List[int]:
    '''
    This function inserts n2 after every instance of n1 in the list

    >>> insert_value([1, 2, 3], 2, 3)
    [1, 2, 3, 3]

    >>> insert_value([1, 1, 1, 1], 1, 2)
    [1, 2, 1, 2, 1, 2, 1, 2]

    :param lst: lst containing ints
    :param n1: any int
    :param n2: any int
    :return: New list containing n2 inserted after every instance of n1
    '''


    i = 0
    while i < len(lst):
        if lst[i] == n1:
            lst.insert(i + 1, n2)
            i += 1
        i += 1

    return lst


print(insert_value([1, 1, 1, 1], 1, 1))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
