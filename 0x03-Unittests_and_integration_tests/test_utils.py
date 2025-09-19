#!/usr/bin/env python3
"""
This module contains unit tests for the access_nested_map function
defined in the utils module.
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """
    TestAccessNestedMap contains unit tests for the access_nested_map
    function to verify it correctly retrieves values from nested maps.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: object) -> None:
        """Test that access_nested_map returns expected results for the valid paths."""
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == "__main__":
    unittest.main()
