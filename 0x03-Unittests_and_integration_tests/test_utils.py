#!/usr/bin/env python3
"""
The program contains unit tests for the access_nested_map function
defined in the utils module.
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """
    The function contains unit tests for the access_nested_map
    function to verify it correctly retrieves values from nested maps
    with errors raised for invalid paths.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: object) -> None:
        """Used to make sure that access_nested_map returns expected results for valid paths."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map: dict, path: tuple, expected_message: str) -> None:
        """Shows that access_nested_map raises KeyError with the right message for invalid paths."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), expected_message)


if __name__ == "__main__":
    unittest.main()
