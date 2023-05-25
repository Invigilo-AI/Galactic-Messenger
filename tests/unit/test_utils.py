from typing import TypedDict

from galactic_messenger.src.utils import compose, is_schema


def test_compose():
    def add_7(x):
        return x + 7

    def mul_13(x):
        return x * 13

    add_7_and_mul_13 = compose(add_7, mul_13)

    assert add_7_and_mul_13(9) is add_7(mul_13(9))


def test_is_schema():
    class X(TypedDict):
        x: str

    x = {"x": "xyz"}

    assert is_schema(x, X) is True

    class Y(TypedDict):
        y: str

    x = {"z": "xyz"}

    assert is_schema(x, Y) is False
