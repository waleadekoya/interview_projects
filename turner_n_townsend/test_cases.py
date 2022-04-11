import unittest

from parameterized import parameterized

from collatz_conjecture import collatz_conjecture
from roman_numerals import calculate_roman_numeral
from stack import Fifth, StackException


class TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.stack = Fifth([])

    @parameterized.expand([
        ("case 1", 35, 13),
        ("case 2", 8, 3),
        ("case 3", 10, 6),
    ])
    def test_collatz_conjecture(self, test_case, input_arg, expected):
        self.assertEqual(collatz_conjecture(input_arg), expected)

    @parameterized.expand([
        ("case 1", "X", 10),
        ("case 2", "VI", 6),
        ("case 3", "MXVII", 1017),
        ("case 4", ("MXVII", "X"), 1027),
        ("case 5", ("MXVII", "VI", "X"), 1033),
    ])
    def test_get_roman_numeral(self, test_case, input_arg, expected):
        self.assertEqual(calculate_roman_numeral(*input_arg), expected)

    def test_push(self):
        self.stack.PUSH(3)
        self.stack.PUSH(11)
        self.assertEqual(self.stack, [3, 11])

    @parameterized.expand([
        (Fifth([10, 11, 13, 14, 28]), Fifth([10, 11, 13, 14])),
        (Fifth([11, 13]), Fifth([11])),
        (Fifth([1, 5, 7, 9]), Fifth([1, 5, 7])),
    ])
    def test_pop(self, input_arg, expected):
        stack: Fifth[int] = input_arg
        stack.POP()
        self.assertEqual(stack, expected)

    @parameterized.expand([
        (Fifth([10, 11, 13, 14, 28]), Fifth([10, 11, 13, 28, 14])),
        (Fifth([11, 13]), Fifth([13, 11])),
        (Fifth([1, 5, 7, 9]), Fifth([1, 5, 9, 7])),
    ])
    def test_swap(self, input_arg, expected):
        stack: Fifth[int] = input_arg
        stack.SWAP()
        self.assertEqual(stack, expected)

    @parameterized.expand([
        (Fifth([10, 11, 13, 14, 28]), Fifth([10, 11, 13, 14, 28, 28])),
        (Fifth([11, 13]), Fifth([11, 13, 13])),
        (Fifth([1, 5, 7, 9]), Fifth([1, 5, 7, 9, 9])),
    ])
    def test_dup(self, input_arg, expected):
        stack: Fifth[int] = input_arg
        stack.DUP()
        self.assertEqual(stack, expected)

    @parameterized.expand([
        (Fifth([10, 11, 13, 14, 28]), Fifth([10, 11, 13, 14 + 28])),
        (Fifth([11, 13]), Fifth([11 + 13])),
        (Fifth([1, 5, 7, 9]), Fifth([1, 5, 16])),
    ])
    def test_add(self, input_arg, expected):
        stack: Fifth[int] = input_arg
        stack.ADD()
        self.assertEqual(stack, expected)

    @parameterized.expand([
        (Fifth([10, 11, 13, 14, 28]), Fifth([10, 11, 13, 14 - 28])),
        (Fifth([11, 13]), Fifth([11 - 13])),
        (Fifth([1, 5, 7, 9]), Fifth([1, 5, 7 - 9])),
    ])
    def test_subtract(self, input_arg, expected):
        stack: Fifth[int] = input_arg
        stack.SUBTRACT()
        self.assertEqual(stack, expected)

    @parameterized.expand([
        (Fifth([10, 11, 13, 14, 28]), Fifth([10, 11, 13, 14*28])),
        (Fifth([11, 13]), Fifth([13*11])),
        (Fifth([1, 5, 7, 9]), Fifth([1, 5, 9*7])),
    ])
    def test_multiply(self, input_arg, expected):
        stack: Fifth[int] = input_arg
        stack.MULTIPLY()
        self.assertEqual(stack, expected)

    @parameterized.expand([
        ("case 1", Fifth([10, 11, 13, 28, 14]), Fifth([10, 11, 13, 2])),
        ("case 2", Fifth([28, 14]), Fifth([2])),
    ])
    def test_divide(self, case, input_arg, expected):
        stack: Fifth[int] = input_arg
        stack.DIVIDE()
        self.assertEqual(stack, expected)

    def test_error(self):
        stack: Fifth[int] = Fifth([2])
        with self.assertRaises(StackException):
            stack.ADD()


if __name__ == '__main__':
    unittest.main()
