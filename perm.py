"""
This is a module for working with permutations.
"""

from typing import List, Set


def validate_permutation(p):
    """
    Validates whether a given input parameter is a proper permutation.
    :param p:  The permutation to check.
    """
    if not isinstance(p, list):
        raise ValueError("A permutation should be a list of integers")

    for i in p:
        if not isinstance(i, int):
            raise ValueError("A permutation should be a list of integers")

    if set(p) != set(range(len(p))):
        raise ValueError("A permutation should only contain each position exactly once")


def permutation_from_cycles(n: int, cycles: List[List[int]]) -> List[int]:
    """
    Creates a permutation in list form from a given list of cycles.
    :param n: Length of the permutation.
    :param cycles: The list of cycles which represents the permutation.
    :return: List representation of the permutation.
    """
    mapping = list(range(n))

    for cycle in cycles:
        for fr, to in zip(cycle, cycle[1:] + [cycle[0]]):
            if mapping[fr] != fr:
                raise ValueError("Cycles should not overlap")

            mapping[fr] = to

    return mapping


def trivial_permutation(n: int) -> List[int]:
    """
    Creates the trivial permutation of length n.
    :param n: Length of the permutation to create.
    :return:  List representation of the permutation.
    """
    return list(range(n))


def cycles(p: List[int]) -> List[Set[int]]:
    """
    Gives the list of cycles which represent the given permutation.
    :param p: The list representation of the permutation.
    :return:  Cycle representation of the given permutation.
    """
    validate_permutation(p)

    todo = list(range(len(p)))
    cycles = []

    while todo:
        start = todo.pop(0)

        cycle = (start,)
        position = p[start]

        while position != start:
            todo.remove(position)
            cycle += (position, )
            position = p[position]

        cycles.append(cycle)

    return cycles


def print_permutation(p: List[int]):
    """
    Prints the given permutation in cycle representation.
    :param p:  Permutation to print.
    """
    validate_permutation(p)

    C = cycles(p)
    s = ''
    for cycle in C:
        cyclestr = '('
        for el in cycle:
            cyclestr += str(el) + ','
        s += cyclestr[:len(cyclestr) - 1] + ')'
    if s == '':
        s = '()'
    print(s)


def is_trivial(p: List[int]) -> bool:
    """
    Returns true iff `p' is the trivial permutation.
    :param p: Permutation to check.
    """
    validate_permutation(p)

    for i in range(len(p)):
        if p[i] != i:
            return False
    return True


def test_permutation(n: int) -> List[int]:
    """
    Creates a nasty permutation of length `n`, with a very large period.
    :param n: Length of the permutation to create.
    :return: Nasty permutation of length `n' in list representation.
    """
    permutation = [i + 1 for i in range(n)]
    cycle_length = 2
    cycle_index = 0

    while cycle_length + cycle_index < n:
        permutation[cycle_index + cycle_length - 1] = cycle_index
        cycle_index += cycle_length
        cycle_length += 1

    if n > 0:
        permutation[n - 1] = cycle_index

    return permutation
