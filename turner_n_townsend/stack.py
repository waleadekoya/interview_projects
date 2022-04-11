import collections
from argparse import ArgumentParser
from functools import reduce
from typing import Callable, Optional

from utils import logger

__author__ = "Wale Adekoya"


class StackException(Exception):
    pass


class Fifth(collections.UserList):
    """
    Fifth is a new stack-based language.
    A stack is a data structure which can only have elements added to the top.
    Fifth stores a stack of integers and supports commands to manipulate that stack.
    Operations always apply to the top of the stack.
    Fifth supports the following arithmetic operators: + - * /

    Each of these applies the operator to the two values on the top of the stack
    and pushes the result to the top of the stack.
    If division results in a non-integer, it will round down.

    Fifth also supports the following commands:
        PUSH x - push x onto the top of the stack, where x is a valid integer
        POP - remove the top element of the stack
        SWAP - swap the top two elements of the stack
        DUP - duplicate the top element of the stack
    """

    def __init__(self, stack):
        super().__init__(stack)
        logger.info(f"Stack is {self.data}")

    def PUSH(self, item: int) -> None:
        self.append(item)
        self.log_message(self.PUSH, item)

    def POP(self) -> None:
        self.remove(self.data[-1])
        self.log_message(self.POP, self.data[-1])

    def SWAP(self) -> None:
        copy = self.data.copy()[-2:]
        self.data[-1] = copy[0]
        self.data[-2] = copy[1]
        self.log_message(self.SWAP)

    def DUP(self) -> None:
        self.append(self.data[-1])
        self.log_message(self.DUP)

    def __error_msg(self, operator: str) -> None:
        if len(self.data[-2:]) == 1:
            raise StackException(f"'{operator}' arithmetic operator requires at least two values")

    def ADD(self) -> None:
        self.__error_msg("+")
        addition: int = sum(self.data[-2:])
        self.__get_operation_output(addition, self.ADD)

    def SUBTRACT(self) -> None:
        self.__error_msg("-")
        subtract: int = self.data[-2] - self.data[-1]
        self.__get_operation_output(subtract, self.SUBTRACT)

    def __get_operation_output(
            self,
            value: int,
            func: Callable[[int | str | None], int | str | None]
    ) -> None:
        if len(self.data) > 2:
            self.data = self.data[0:-2] + [value]
        else:
            self.data = [value]
        self.log_message(func)

    def MULTIPLY(self) -> None:
        self.__error_msg("*")
        multiply: int = reduce(lambda x, y: x * y, self.data[-2:])
        self.__get_operation_output(multiply, self.MULTIPLY)

    def DIVIDE(self) -> None:
        self.__error_msg("/")
        division: int = reduce(lambda x, y: int(round(x / y, 0)), self.data[-2:])
        self.__get_operation_output(division, self.DIVIDE)

    def log_message(self, command: Callable, item: Optional[int] = None) -> None:
        if command.__name__ in ["DUP", "SWAP", "POP"]:
            logger.info(f"Command: {command.__name__}")
        elif command.__name__ in ["ADD", "MULTIPLY", "SUBTRACT", "DIVIDE"]:
            logger.info(f"{command.__name__}")
        else:
            logger.info(f"{command.__name__} {item}")
        logger.info(f"Stack is {self.data}")


class ArgsParse:

    @classmethod
    def arg_parser(cls):
        parser = ArgumentParser(prog="Fifth", description="handles commands for Stack data types")
        parser.add_argument("--stack", nargs="+", type=int, help="a data structure containing a stack of integers")
        parser.add_argument("--PUSH", type=int, help="adds the given element to the stack")
        for command, value in cls.__args_options().items():
            parser.add_argument(f"--{command}", help=value.get("help"), action="store_true")
        args = parser.parse_args()
        return args

    @classmethod
    def __args_options(cls):
        note = "last two values on the top of the stack and push the result to the top of the stack"
        return {
            **dict(
                POP=dict(help="removes the given element from the stack", type=bool),
                SWAP=dict(help="swap the top two elements of the stack", type=bool),
                DUP=dict(help="duplicate the top element of the stack", type=bool), ),
            **{
                "ADD": dict(help=f"adds {note}", type=bool),
                "SUBTRACT": dict(help=f"subtracts {note}", type=bool),
                "MULTIPLY": dict(help=f"multiply {note}", type=bool),
                "DIVIDE": dict(help=f"divides {note}", type=bool),
            }
        }


class Interpreter(Fifth):
    """
    A python program which works as a fifth interpreter.
    Each line of input to the program represent a single fifth command.
    The result of each command is outputted to the terminal. Handle errors sensibly.

    Example:
    py src\turner_n_townsend\stack.py -help

    Terminal
    py src\turner_n_townsend\stack.py --stack 12 23 34 45 67 --PUSH 35
    [11-Apr-22 19:29:13] [Turner & Townsend] [INFO] Stack is [12, 23, 34, 45, 67]
    [11-Apr-22 19:29:13] [Turner & Townsend] [INFO] PUSH 35
    [11-Apr-22 19:29:13] [Turner & Townsend] [INFO] Stack is [12, 23, 34, 45, 67, 35]

    Terminal:
    py src\turner_n_townsend\stack.py --stack 34 45 56 67 33 72 --POP
    [11-Apr-22 19:28:19] [Turner & Townsend] [INFO] Stack is [34, 45, 56, 67, 33, 72]
    [11-Apr-22 19:28:19] [Turner & Townsend] [INFO] Command: POP
    [11-Apr-22 19:28:19] [Turner & Townsend] [INFO] Stack is [34, 45, 56, 67, 33]


    Terminal:
    py src\turner_n_townsend\stack.py  --stack 34 45 56 67 33 72 --DUP
    Output:
    [11-Apr-22 19:27:13] [Turner & Townsend] [INFO] Stack is [34, 45, 56, 67, 33, 72]
    [11-Apr-22 19:27:13] [Turner & Townsend] [INFO] Command: DUP
    [11-Apr-22 19:27:13] [Turner & Townsend] [INFO] Stack is [34, 45, 56, 67, 33, 72, 72]

    Terminal:
    py src\turner_n_townsend\stack.py --stack 34 45 56 67 3 2 --SWAP
    Output:
    [11-Apr-22 19:23:44] [Turner & Townsend] [INFO] Stack is [12, 34, 23, 45, 34, 56, 45, 67]
    [11-Apr-22 19:23:44] [Turner & Townsend] [INFO] Command: SWAP
    [11-Apr-22 19:23:44] [Turner & Townsend] [INFO] Stack is [12, 34, 23, 45, 34, 56, 67, 45]

    Terminal:
    py src\turner_n_townsend\stack.py --stack  12 23 34 45 67 --ADD
    Output:
    [11-Apr-22 19:38:31] [Turner & Townsend] [INFO] Stack is [12, 23, 34, 45, 67]
    [11-Apr-22 19:38:31] [Turner & Townsend] [INFO] ADD
    [11-Apr-22 19:38:31] [Turner & Townsend] [INFO] Stack is [12, 23, 34, 112]
    """

    def __init__(self):
        self.__args = ArgsParse.arg_parser()
        self.data = self.__args.stack
        super().__init__(self.__args.stack)
        self.__run_command()

    def __run_command(self):
        logger.info(vars(self.__args))
        if self.__args.PUSH:
            self.PUSH(self.__args.PUSH)
        if self.__args.POP:
            self.POP()
        if self.__args.SWAP:
            self.SWAP()
        if self.__args.DUP:
            self.DUP()
        if self.__args.DIVIDE:
            self.DIVIDE()
        if self.__args.MULTIPLY:
            self.MULTIPLY()
        if self.__args.SUBTRACT:
            self.SUBTRACT()
        if self.__args.ADD:
            self.ADD()


if __name__ == "__main__":
    Interpreter()
