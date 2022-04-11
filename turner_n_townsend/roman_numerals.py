from typing import Tuple, Dict, Union

__author__ = "Wale Adekoya"


def calculate_roman_numeral(*args: Union[Tuple[str], str]) -> int:
    """
     A Python program which takes a series of roman numerals as input
     and outputs their value as a number
    :param args: Tuple of strings or a single string - variable number of arguments
    :return: int
    """
    valid_roman_numerals: Dict[str, int] = dict(
        I=1, V=5, X=10, C=100, M=1000
    )
    roman_numeral: int = 0
    for arg in args:
        if len(arg) == 1:
            roman_numeral += valid_roman_numerals.get(arg, 0)
        else:
            for item in arg:
                roman_numeral += valid_roman_numerals.get(item, 0)
    return roman_numeral
