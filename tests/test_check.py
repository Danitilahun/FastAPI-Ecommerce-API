import pytest

def product(a:int , b: int):
    return a * b

@pytest.mark.parametrize(
    "values, expected_value",
    [
        ({"a": 1, "b" : 2 }, 2),
        ({"a": 10, "b" : 4 }, 40),
        ({"a": 5, "b" : 3 }, 15),
    ]
)
def test_product(values,expected_value):
    result = product(values["a"],values["b"])
    assert result == expected_value
