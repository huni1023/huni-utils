import pytest

np = pytest.importorskip("numpy")
from huniutils.measurement.ctt import calculate_item_difficulty


def test_calculate_item_difficulty_basic():
    responses = [3, 4, 5]
    result = calculate_item_difficulty(5, responses)
    assert np.isclose(result, np.mean(responses) / 5)

def test_calculate_item_difficulty_raises_with_nan():
    with pytest.raises(ValueError):
        calculate_item_difficulty(5, [1, 2, np.nan])
