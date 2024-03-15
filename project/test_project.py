from project import food_list, how_to_cook, save_recipe
import pytest
from unittest.mock import patch, mock_open, MagicMock


def test_food_list():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [
            {
                "id": 1,
                "title": "dish",
                "nutrition": {
                    "nutrients": [{"name": "Calories", "amount": 10, "unit": "kcal"}]
                },
            }
        ]
    }
    with patch("requests.get") as mock_get:
        mock_get.return_value = mock_response
        result = food_list("papaya", "asian", 400)
        assert result == "dish, ID: 1, Calories: 10"


def test_how_to_cook():
    mock_response = MagicMock()
    mock_response.json.return_value = [{"steps": [{"number": 1, "step": "scrub"}]}]
    with patch("requests.get") as mock_get:
        mock_get.return_value = mock_response
        result = how_to_cook(1)
        assert result == "Step 1: scrub\n"


def test_save_recipe():
    m = mock_open()
    with patch("builtins.open", m) as mock_file:
        save_recipe("filename", "some data")
    mock_file.assert_called_with("filename.txt", "w")
    mock_file().write.assert_called_with("some data")


def test_food_list_calorie_not_number():
    with pytest.raises(ValueError):
        food_list("apple", "asian", "not a number")


def test_how_to_cook_not_number():
    with pytest.raises(ValueError):
        how_to_cook("f")


# When you want to mock an API call, you can use MagicMock to simulate the response. When you want to mock the open function to simulate reading from or writing to a file, you can use mock_open(). This allows you to test your code's behavior when interacting with files without actually needing to create or modify any real files.
# so magicmock function is use to test request url like api. json.return_value will return a list of dictionaries . witth patch("requets.get") as mock_get will say inside this block ,it should behave as request.get


"""
with patch("requests.get") as mock_get: This line is saying "while we're inside this block of code, whenever we call requests.get, don't actually do what requests.get normally does. Instead, use this fake version we're creating, which we're calling mock_get."

mock_get.return_value = mock_response: This line is saying "when we call our fake version of requests.get, don't do what requests.get normally does (which is to send a request to a URL and return the response). Instead, just give back this mock_response we've prepared."
So, in simpler terms, these two lines together are saying "pretend to call requests.get, but actually just return this mock_response we've made". This is useful in testing because it lets us control exactly what requests.get returns, so we can test how our code handles different responses.
"""
