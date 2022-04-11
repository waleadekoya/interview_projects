from typing import Union

__author__ = "Wale Adekoya"


def collatz_conjecture(n: int) -> int:
    """
    A python program which takes a numeric input and
    shows how many steps it takes until the Collatz sequence reaches 1
    :param n:
    :return : int
    """
    count_of_steps: Union[int, float] = 0
    while n > 1:
        if n % 2 == 0:  # n is even
            n = n / 2
        else:  # n is odd
            n = 3 * n + 1
        count_of_steps += 1

    return count_of_steps
