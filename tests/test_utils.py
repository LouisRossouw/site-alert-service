import os
import json
import pytest
import time
from lib.utils import write_to_json, read_json, calculate_request_time


def test_json_read_write(tmp_path):
    """
    Test that we can write data to a JSON file and read it back correctly.
    This is a 'unit test' because it tests a specific piece of logic in isolation.
    """
    # Setup: Create a temporary file path using pytest's built-in tmp_path fixture
    test_file = tmp_path / "test.json"
    data = {"key": "value", "number": 123}

    # Action: Write data
    write_to_json(str(test_file), data)

    # Action: Read data back
    result = read_json(str(test_file))

    # Assertion: Check if the data matches
    assert result == data
    assert result["key"] == "value"
    assert result["number"] == 123


def test_calculate_request_time():
    """
    Test the calculation of request time.
    """
    # Setup: mock a start time
    start = time.time() - 1.0  # Simulate something that started 1 second ago

    # Action
    duration = calculate_request_time(start)

    # Assertion: It should be roughly 1 second
    assert duration >= 1.0
    assert duration < 2.0  # Unless the computer is extremely slow!
