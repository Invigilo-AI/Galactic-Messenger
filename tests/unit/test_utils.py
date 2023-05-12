from utils import compose


def test_compose():
    def add_7(x):
        return x + 7

    def mul_13(x):
        return x * 13

    add_7_and_mul_13 = compose(add_7, mul_13)

    assert add_7_and_mul_13(9) is add_7(mul_13(9))
