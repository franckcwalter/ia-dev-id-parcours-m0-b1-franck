# tests/test_addition.py — exemple sans API pour comprendre pytest
def addition(a: int, b: int) -> int:
    return a + b


def test_addition_simple():
    assert addition(2, 3) == 5


def test_addition_negatifs():
    assert addition(-1, -2) == -3


import pytest

@pytest.mark.parametrize("a,b,attendu", [
    (0, 0, 0),
    (10, -3, 7),
    (1, 1, 2),
])
def test_addition_param(a, b, attendu):
    assert addition(a, b) == attendu