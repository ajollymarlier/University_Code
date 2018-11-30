"""CSC148 Assignment 2: Autocompleter classes

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This file contains the design of a public interface (Autocompleter) and two
implementation of this interface, SimplePrefixTree and CompressedPrefixTree.
You'll complete both of these subclasses over the course of this assignment.

As usual, be sure not to change any parts of the given *public interface* in the
starter code---and this includes the instance attributes, which we will be
testing directly! You may, however, add new private attributes, methods, and
top-level functions to this file.
"""
from __future__ import annotations
from typing import Any, List, Optional, Tuple


################################################################################
# The Autocompleter ADT
################################################################################
class Autocompleter:
    """An abstract class representing the Autocompleter Abstract Data Type.
    """
    def __len__(self) -> int:
        """Return the number of values stored in this Autocompleter."""
        raise NotImplementedError

    def insert(self, value: Any, weight: float, prefix: List) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this prefix tree
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
            weight > 0
            The given value is either:
                1) not in this Autocompleter
                2) was previously inserted with the SAME prefix sequence
        """
        raise NotImplementedError

    def autocomplete(self, prefix: List,
                     limit: Optional[int] = None) -> List[Tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix.

        The return value is a list of tuples (value, weight), and must be
        ordered in non-increasing weight. (You can decide how to break ties.)

        If limit is None, return *every* match for the given prefix.

        Precondition: limit is None or limit > 0.
        """
        raise NotImplementedError

    def remove(self, prefix: List) -> None:
        """Remove all values that match the given prefix.
        """
        raise NotImplementedError


################################################################################
# SimplePrefixTree (Tasks 1-3)
################################################################################
class SimplePrefixTree(Autocompleter):
    """A simple prefix tree.

    This class follows the implementation described on the assignment handout.
    Note that we've made the attributes public because we will be accessing them
    directly for testing purposes.

    === Attributes ===
    value:
        The value stored at the root of this prefix tree, or [] if this
        prefix tree is empty.
    weight:
        The weight of this prefix tree. If this tree is a leaf, this attribute
        stores the weight of the value stored in the leaf. If this tree is
        not a leaf and non-empty, this attribute stores the *aggregate weight*
        of the leaf weights in this tree.
    subtrees:
        A list of subtrees of this prefix tree.
    weight_type:
        The method of calculating weight

    === Representation invariants ===
    - self.weight >= 0

    - (EMPTY TREE):
        If self.weight == 0, then self.value == [] and self.subtrees == [].
        This represents an empty simple prefix tree.
    - (LEAF):
        If self.subtrees == [] and self.weight > 0, this tree is a leaf.
        (self.value is a value that was inserted into this tree.)
    - (NON-EMPTY, NON-LEAF):
        If len(self.subtrees) > 0, then self.value is a list (*common prefix*),
        and self.weight > 0 (*aggregate weight*).

    - ("prefixes grow by 1")
      If len(self.subtrees) > 0, and subtree in self.subtrees, and subtree
      is non-empty and not a leaf, then

          subtree.value == self.value + [x], for some element x

    - self.subtrees does not contain any empty prefix trees.
    - self.subtrees is *sorted* in non-increasing order of their weights.
      (You can break ties any way you like.)
      Note that this applies to both leaves and non-leaf subtrees:
      both can appear in the same self.subtrees list, and both have a `weight`
      attribute.
    """
    value: Any
    weight: float
    subtrees: List[SimplePrefixTree]
    weight_type: str
    num_leaves: int

    def __init__(self, weight_type: str) -> None:
        """Initialize an empty simple prefix tree.

        Precondition: weight_type == 'sum' or weight_type == 'average'.

        The given <weight_type> value specifies how the aggregate weight
        of non-leaf trees should be calculated (see the assignment handout
        for details).
        """
        self.value = []
        self.subtrees = []
        self.weight_type = weight_type
        self.weight = 0.0
        self.num_leaves = 0

    def _get_sum_weights(self) -> float:
        """Helper method to traverse tree and return sum of all leaf weights
        """
        sum_weight = 0.0
        for subtree in self.subtrees:
            sum_weight += subtree.weight

        return sum_weight

    def _get_ave_weights(self) -> float:
        """Helper method to traverse tree and return sum of all leaf weights
            Returns a tuple containing sum and num_leaves
        """
        sum_sub_leaves = 0
        sum_sub_weights = 0.0
        for subtree in self.subtrees:
            sum_sub_leaves += subtree.num_leaves
            sum_sub_weights += subtree.weight * subtree.num_leaves

        if sum_sub_leaves == 0:
            return 0.0
        else:
            self.num_leaves = sum_sub_leaves
            return sum_sub_weights / sum_sub_leaves

    # Adds leaves only
    def __len__(self) -> int:
        """=== Inherited from superclass ===

        >>> t = SimplePrefixTree('sum')
        >>> t.insert("C", 4, ['C'])
        >>> t.__len__()
        1
        """
        if self.value == [] and len(self.subtrees) == 0:
            return 0

        elif len(self.subtrees) == 0:
            return 1

        else:
            sum_weights = 0
            for subtree in self.subtrees:
                sum_weights += subtree.__len__()

            return sum_weights

    def insert(self, value: Any, weight: float, prefix: List) -> None:
        """
        === Inherited from superclass ===
        Insert the given value into this Autocompleter.
        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this prefix tree
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
            weight > 0
            The given value is either:
                1) not in this Autocompleter
                2) was previously inserted with the SAME prefix sequence

            len(value) and len(prefix) > 0

        >>> t = SimplePrefixTree('average')
        >>> t.__len__()
        0
        >>> t.weight
        0.0
        >>> t.insert("art", 3.0, ['a', 'r', 't'])
        >>> t.insert("carol", 3.0, ['c', 'a', 'r', 'o', 'l'])
        >>> t.insert("car", 3.0, ['c', 'a', 'r'])
        >>> t.insert("carol", 3.0, ['c', 'a', 'r', 'o', 'l'])
        >>> t.insert("carol", 3.0, ['c', 'a', 'r', 'o', 'l'])
        >>> t.__len__()
        3
        >>> t.insert("car", 3.0, ['c', 'a', 'r'])
        >>> t.subtrees[0].subtrees[0].subtrees[0].subtrees[0].subtrees[0].subtrees[0].value
        'carol'
        >>> t.__len__()
        3
        >>> t.weight
        6.0
        >>> t._str_indented() # This is supposed to fail to show tree
        3
        """
        # Sanitizes value and prefix to make all chars lowercase
        prefix_cut = prefix[:len(self.value)]

        if len(self.value) == len(prefix):
            found_value = False
            for subtree in self.subtrees:
                if subtree.value == value:
                    subtree.weight += weight
                    found_value = True
                    break

            if not found_value:
                self.subtrees.append(SimplePrefixTree(self.weight_type))
                self.subtrees[len(self.subtrees) - 1].value = value
                self.subtrees[len(self.subtrees) - 1].weight += weight
                self.subtrees[len(self.subtrees) - 1].num_leaves += 1

        else:
            if len(self.subtrees) == 0:
                self.subtrees.append(SimplePrefixTree(self.weight_type))
                self.subtrees[len(self.subtrees) - 1].value = \
                    prefix[:len(self.value) + 1]
                self.subtrees[len(self.subtrees) - 1] \
                    .insert(value, weight, prefix)

            elif self.value == prefix_cut:
                found_fragment = False
                for subtree in self.subtrees:
                    if subtree.value == prefix[0: len(subtree.value)]:
                        subtree.insert(value, weight, prefix)
                        found_fragment = True
                        break

                if not found_fragment:
                    self.subtrees.append(SimplePrefixTree(self.weight_type))
                    self.subtrees[len(self.subtrees) - 1].value = \
                        prefix[:len(self.value) + 1]
                    self.subtrees[len(self.subtrees) - 1] \
                        .insert(value, weight, prefix)

        # Recalculates Weight after inserting
        if self.weight_type == 'sum':
            self.weight = self._get_sum_weights()
            self.subtrees.sort(key=self._take_weight_list, reverse=True)

        elif self.weight_type == 'average':
            self.weight = self._get_ave_weights()
            self.subtrees.sort(key=self._take_weight_list, reverse=True)

    def _take_weight_list(self, elem: Any) -> float:
        """Helper method for sort key"""
        return elem.weight

    def autocomplete(self, prefix: List,
                     limit: Optional[int] = None) -> List[Tuple[Any, float]]:
        """ Return up to <limit> matches for the given prefix.

            The return value is a list of tuples (value, weight), and must be
            ordered in non-increasing weight. (You can decide how to break ties.)

            If limit is None, return *every* match for the given prefix.

            Precondition: limit is None or limit > 0.

            >>> t = SimplePrefixTree('average')
            >>> t.autocomplete(['c'])
            'Triple meme'
            >>> t.insert("art", 3.0, ['a', 'r', 't'])
            >>> t.insert("car", 3.0, ['c', 'a', 'r'])
            >>> t.insert("caroL", 3.0, ['c', 'a', 'r', 'o', 'L'])
            >>> t.insert("carol", 3.0, ['c', 'a', 'r', 'o', 'l'])
            >>> t.insert("carol", 3.0, ['c', 'a', 'r', 'o', 'L'])
            >>> t.insert("cards", 4.0, ['c', 'a', 'r', 'd', 's'])
            >>> t.autocomplete(['a'])
            'Quad Meme'
            >>> t.autocomplete(['c', 'a', 'r'], 2)
            'Double meme'
            >>> t.insert("car", 3.0, ['c', 'a', 'r'])
            >>> t.autocomplete(['c'], 2)
            'Penta meme'
            >>> t._str_indented()
            'Meme'
        """

        # Outer level is just for finding prefix match
        # This is run when matching prefix is found
        if self.value == prefix:
            # Adds all values in self.subtrees
            return self._return_values(limit)

        # If self.value is contained within prefix
        elif self.value == prefix[0: len(self.value)]:
            for subtree in self.subtrees:
                if subtree.value == prefix[0: len(subtree.value)]:
                    return subtree.autocomplete(prefix, limit)

            # If self.value is part of prefix but there is no other parts
            # IE. 'Car' exists but wanting to find 'Carol'
            return []

        # If prefix is not found at all in tree
        else:
            return []

    def _return_values(self, limit: Optional[int]) -> List[Tuple[Any, float]]:
        """ Helper method to return a list of all values and
            weights within self.subtrees
        """
        auto_values = list()
        for subtree in self.subtrees:
            # If subtree.value is a value
            if type(subtree.value) != list:
                # If there is no limit
                if limit is None:
                    auto_values.append((subtree.value, subtree.weight))

                # If there is a limit and len(auto_values) < limit
                elif limit is not None and len(auto_values) < limit:
                    auto_values.append((subtree.value, subtree.weight))

            # If subtree.value is a prefix
            else:
                lst = subtree._return_values(limit)

                # If limit is not stated or adding lst to
                # auto_values won't go over limit
                if limit is None or len(auto_values) + len(lst) <= limit:
                    auto_values.extend(lst)

                # If adding all of lst to auto_values will go over limit
                else:
                    for i in range(limit - len(auto_values)):
                        auto_values.append(lst[i])

        auto_values.sort(key=self._sort_autos, reverse=True)
        return auto_values

    def _sort_autos(self, elem: Any) -> float:
        return elem[1]

    def remove(self, prefix: List) -> None:
        """Remove all values that match the given prefix.
         >>> t = SimplePrefixTree('average')
         >>> t.insert('a', 7.0, ['a'])
         >>> t.insert('art', 4.0, ['a', 'r', 't'])
         >>> t.insert('arts', 4.0, ['a', 'r', 't', 's'])
         >>> t.insert('cat', 4.0, ['c', 'a', 't'])
         >>> t.insert('cut', 4.0, ['c', 'u', 't'])
         >>> t.subtrees[0].subtrees[1].value
         'a'
         >>> t._str_indented()
         'Double Meme'
         >>> t.weight
         4.6
         >>> t.remove(['a', 'r', 't'])
         >>> t._str_indented()
         'Meme'
         >>> t.weight
         5.0
        """
        if self.value == prefix:
            self.subtrees = list()

        elif self.value == prefix[0: len(self.value)]:
            for subtree in self.subtrees:
                if subtree.value == prefix[0: len(subtree.value)]:
                    subtree.remove(prefix)

                    # This is after the level below has been removed
                    # Thus if there exists an element,
                    # then it connects to some other branch
                    if len(subtree.subtrees) == 0:
                        self.subtrees.remove(subtree)
                        self.num_leaves -= 1

            # Recalculates Weight after inserting
            if self.weight_type == 'sum':
                self.weight = self._get_sum_weights()
                self.subtrees.sort(key=self._take_weight_list, reverse=True)

            elif self.weight_type == 'average':
                self.weight = self._get_ave_weights()
                self.subtrees.sort(key=self._take_weight_list, reverse=True)

        else:
            return

    def is_empty(self) -> bool:
        """Return whether this simple prefix tree is empty."""
        return self.weight == 0.0

    def is_leaf(self) -> bool:
        """Return whether this simple prefix tree is a leaf."""
        return self.weight > 0 and self.subtrees == []

    def __str__(self) -> str:
        """Return a string representation of this tree.

        You may find this method helpful for debugging.
        """
        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = '  ' * depth + f'{self.value} ({self.weight})\n'
            for subtree in self.subtrees:
                s += subtree._str_indented(depth + 1)
            return s


################################################################################
# CompressedPrefixTree (Task 6)
################################################################################
class CompressedPrefixTree(SimplePrefixTree):
    """A compressed prefix tree implementation.

    While this class has the same public interface as SimplePrefixTree,
    (including the initializer!) this version follows the implementation
    described on Task 6 of the assignment handout, which reduces the number of
    tree objects used to store values in the tree.

    === Attributes ===
    value:
        The value stored at the root of this prefix tree, or [] if this
        prefix tree is empty.
    weight:
        The weight of this prefix tree. If this tree is a leaf, this attribute
        stores the weight of the value stored in the leaf. If this tree is
        not a leaf and non-empty, this attribute stores the *aggregate weight*
        of the leaf weights in this tree.
    subtrees:
        A list of subtrees of this prefix tree.

    === Representation invariants ===
    - self.weight >= 0

    - (EMPTY TREE):
        If self.weight == 0, then self.value == [] and self.subtrees == [].
        This represents an empty simple prefix tree.
    - (LEAF):
        If self.subtrees == [] and self.weight > 0, this tree is a leaf.
        (self.value is a value that was inserted into this tree.)
    - (NON-EMPTY, NON-LEAF):
        If len(self.subtrees) > 0, then self.value is a list (*common prefix*),
        and self.weight > 0 (*aggregate weight*).

    - **NEW**
      This tree does not contain any compressible internal values.
      (See the assignment handout for a definition of "compressible".)

    - self.subtrees does not contain any empty prefix trees.
    - self.subtrees is *sorted* in non-increasing order of their weights.
      (You can break ties any way you like.)
      Note that this applies to both leaves and non-leaf subtrees:
      both can appear in the same self.subtrees list, and both have a `weight`
      attribute.
    """
    value: Optional[Any]
    weight: float
    subtrees: List[CompressedPrefixTree]

    # TODO Think this is working
    def insert(self, value: Any, weight: float, prefix: List) -> None:
        """
        === Inherited from superclass ===
        Insert the given value into this Autocompleter.
        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this prefix tree
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
            weight > 0
            The given value is either:
                1) not in this Autocompleter
                2) was previously inserted with the SAME prefix sequence

            len(value) and len(prefix) > 0

        >>> t = CompressedPrefixTree('average')
        >>> t.__len__()
        0
        >>> t.weight
        0.0
        #>>> t.insert("art", 3.0, ['a', 'r', 't'])
        >>> t._str_indented()
        >>> t.insert("carol", 3.0, ['c', 'a', 'r', 'o', 'l'])
        >>> t._str_indented()
        >>> t.insert("cat", 3.0, ['c', 'a', 't'])
        >>> t.insert("cut", 4.0, ['c', 'u', 't'])
        >>> t._str_indented()
        >>> t.insert("carol", 3.0, ['c', 'a', 'r', 'o', 'l'])
        >>> t.insert("caro", 3.0, ['c', 'a', 'r', 'o'])
        >>> t.insert("carol", 3.0, ['c', 'a', 'r', 'o', 'l'])
        >>> t.__len__()
        4
        >>> t.insert("car", 3.0, ['c', 'a', 'r'])
        >>> t._str_indented() # This is supposed to fail to show tree
        3
        >>> t.remove(['c', 'a', 'r'])
        >>> t._str_indented()
        'Meme'
        """
        # Sanitizes value and prefix to make all chars lowercase
        # prefix_cut = prefix[:len(self.value)]

        # This only runs when value is already present
        # Every prefix must have a subtree that is a value

        if self.is_empty():
            self.value = prefix
            self.weight = weight
            self.subtrees.append(CompressedPrefixTree(self.weight_type))
            self.subtrees[len(self.subtrees) - 1].value = value
            self.subtrees[len(self.subtrees) - 1].weight = weight
            self.subtrees[len(self.subtrees) - 1].num_leaves = 1

        elif self.value == prefix:
            found_value = False
            for subtree in self.subtrees:
                if subtree.value == value:
                    subtree.weight += weight
                    found_value = True
                    break

            if not found_value:
                self.subtrees.append(CompressedPrefixTree(self.weight_type))
                self.subtrees[len(self.subtrees) - 1].value = value
                self.subtrees[len(self.subtrees) - 1].weight = weight
                self.subtrees[len(self.subtrees) - 1].num_leaves = 1

        elif len(prefix) > len(self.value) and self.value == prefix[:len(self.value)]:
            found_fragment = False
            for subtree in self.subtrees:
                if len(subtree.value) < len(prefix):
                    if subtree.value == prefix[:len(subtree.value)]:
                        subtree.insert(value, weight, prefix)
                        found_fragment = True

                else:
                    if prefix == subtree.value[:len(prefix)]:
                        subtree.insert(value, weight, prefix)
                        found_fragment = True

            if not found_fragment:
                found_common_prefix = False
                for subtree in self.subtrees:
                    common_prefix = subtree._get_common_prefix(prefix)
                    if len(common_prefix) != 0 and common_prefix != self.value:
                        subtree.insert(value, weight, prefix)
                        found_common_prefix = True
                        break

                if not found_common_prefix:
                    self.subtrees.append(CompressedPrefixTree(self.weight_type))
                    self.subtrees[len(self.subtrees) - 1].value = prefix
                    self.subtrees[len(self.subtrees) - 1].weight = weight
                    self.subtrees[len(self.subtrees) - 1].insert(value, weight, prefix)

        elif len(prefix) < len(self.value) and prefix == self.value[:len(prefix)]:
            # Uproots self tree and saves all temp variables
            temp_value = self.value
            temp_subtrees = self.subtrees
            temp_weight = self.weight
            temp_num_leaves = self.num_leaves

            # Makes self == to smaller prefix
            self.subtrees = []
            self.value = prefix
            # Plus one for new leaf
            self.num_leaves = temp_num_leaves

            # Appending uprooted tree
            self.subtrees.append(CompressedPrefixTree(self.weight_type))
            self.subtrees[len(self.subtrees) - 1].value = temp_value
            self.subtrees[len(self.subtrees) - 1].subtrees = temp_subtrees
            self.subtrees[len(self.subtrees) - 1].weight = temp_weight
            self.subtrees[len(self.subtrees) - 1].num_leaves = temp_num_leaves

            # Recursing on self b/c self.value has changed to our prefix
            self.insert(value, weight, prefix)

        else:
            common_prefix = self._get_common_prefix(prefix)
            if len(common_prefix) != 0:
                # Uproots self tree and saves all temp variables
                temp_value = self.value
                temp_subtrees = self.subtrees
                temp_weight = self.weight
                temp_num_leaves = self.num_leaves

                self.value = common_prefix
                self.subtrees = []

                # Appending uprooted tree
                self.subtrees.append(CompressedPrefixTree(self.weight_type))
                self.subtrees[len(self.subtrees) - 1].value = temp_value
                self.subtrees[len(self.subtrees) - 1].subtrees = temp_subtrees
                self.subtrees[len(self.subtrees) - 1].weight = temp_weight
                self.subtrees[
                    len(self.subtrees) - 1].num_leaves = temp_num_leaves

                # Appending new prefix and recurses into matching prefix
                self.subtrees.append(CompressedPrefixTree(self.weight_type))
                self.subtrees[len(self.subtrees) - 1].value = prefix
                self.subtrees[len(self.subtrees) - 1].weight = weight
                self.subtrees[len(self.subtrees) - 1].insert(value, weight,
                                                             prefix)

            else:
                # Uproots self tree and saves all temp variables
                temp_value = self.value
                temp_subtrees = self.subtrees
                temp_weight = self.weight
                temp_num_leaves = self.num_leaves

                self.value = []
                self.subtrees = []

                # Appending uprooted tree
                self.subtrees.append(CompressedPrefixTree(self.weight_type))
                self.subtrees[len(self.subtrees) - 1].value = temp_value
                self.subtrees[len(self.subtrees) - 1].subtrees = temp_subtrees
                self.subtrees[len(self.subtrees) - 1].weight = temp_weight
                self.subtrees[len(self.subtrees) - 1].num_leaves = temp_num_leaves

                # Appending new prefix and recurses into matching prefix
                self.subtrees.append(CompressedPrefixTree(self.weight_type))
                self.subtrees[len(self.subtrees) - 1].value = prefix
                self.subtrees[len(self.subtrees) - 1].weight = weight
                self.subtrees[len(self.subtrees) - 1].insert(value, weight, prefix)

        # Recalculates Weight after inserting
        if self.weight_type == 'sum':
            self.weight = self._get_sum_weights()
            self.subtrees.sort(key=self._take_weight_list, reverse=True)

        elif self.weight_type == 'average':
            self.weight = self._get_ave_weights()
            self.subtrees.sort(key=self._take_weight_list, reverse=True)

    def _get_common_prefix(self, prefix: List) -> List:
        """Helper method for finding common prefix in self.value and prefix"""
        common_prefix = []

        if not isinstance(self.value, list):
            return common_prefix

        for i in range(min(len(prefix), len(self.value))):
            if prefix[i] == self.value[i]:
                common_prefix.append(prefix[i])
            else:
                break

        return common_prefix

    # Works
    def autocomplete(self, prefix: List,
                     limit: Optional[int] = None) -> List[Tuple[Any, float]]:
        """
        >>> t = CompressedPrefixTree('average')
        >>> t.autocomplete(['c'])
        'Triple meme'
        >>> t.insert("art", 3.0, ['a', 'r', 't'])
        >>> t.insert("car", 3.0, ['c', 'a', 'r'])
        >>> t.insert("carol", 3.0, ['c', 'a', 'r', 'o', 'l'])
        >>> t.insert("carol", 3.0, ['c', 'a', 'r', 'o', 'l'])
        >>> t.insert("carol", 3.0, ['c', 'a', 'r', 'o', 'l'])
        >>> t.insert("cards", 4.0, ['c', 'a', 'r', 'd', 's'])
        >>> t.insert("cut", 4.0, ['c', 'u', 't'])
        >>> t.autocomplete(['a'])
        'Quad Meme'
        >>> t.autocomplete(['c', 'a', 'r'], 20)
        'Double meme'
        >>> t.insert("car", 3.0, ['c', 'a', 'r'])
        >>> t.autocomplete(['c'], 20)
        'Penta meme'
        >>> t._str_indented()
        'Meme'
        """
        # Outer level is just for finding prefix match
        # This is run when matching prefix is found
        if self.value == prefix:
            # Adds all values in self.subtrees
            return self._return_values(limit)

        # If self.value is contained within prefix
        elif self.value == prefix[0: len(self.value)]:
            for subtree in self.subtrees:
                if len(subtree.value) >= len(prefix) and prefix == subtree.value[:len(prefix)]:
                    return subtree._return_values(limit)

                elif len(subtree.value) < len(prefix) and prefix[:len(subtree.value)] == subtree.value:
                    return subtree.autocomplete(prefix, limit)

            # If self.value is part of prefix but there is no other parts
            # IE. 'Car' exists but wanting to find 'Carol'
            return []

        # If prefix is not found at all in tree
        else:
            return []

    # Works
    def remove(self, prefix: List) -> None:
        """Remove all values that match the given prefix.
         >>> t = CompressedPrefixTree('average')
         >>> t.insert('a', 7.0, ['a'])
         >>> t.insert('art', 4.0, ['a', 'r', 't'])
         >>> t.insert('arts', 4.0, ['a', 'r', 't', 's'])
         >>> t.insert('cat', 4.0, ['c', 'a', 't'])
         >>> t.insert('cut', 4.0, ['c', 'u', 't'])
         >>> t._str_indented()
         'Double Meme'
         >>> t.weight
         4.6
         >>> t.remove(['a', 'r', 't'])
         >>> t._str_indented()
         'Meme'
         >>> t.weight
         5.0
        """
        if self.value == prefix:
            self.subtrees = list()

        elif self.value == prefix[0: len(self.value)]:
            for subtree in self.subtrees:
                if subtree.value == prefix[0: len(subtree.value)]:
                    subtree.remove(prefix)

                    # This is after the level below has been removed
                    # Thus if there exists an element,
                    # then it connects to some other branch
                    if len(subtree.subtrees) == 0:
                        self.subtrees.remove(subtree)
                        self.num_leaves -= 1

            # Recalculates Weight after inserting
            if self.weight_type == 'sum':
                self.weight = self._get_sum_weights()
                self.subtrees.sort(key=self._take_weight_list, reverse=True)

            elif self.weight_type == 'average':
                self.weight = self._get_ave_weights()
                self.subtrees.sort(key=self._take_weight_list, reverse=True)

        else:
            return


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-nested-blocks': 4
    })
