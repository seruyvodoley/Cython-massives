"""тесты для бинарного поиска"""

import unittest
from dynamic_array_c import array
import binary_search

TEST_BINARY_SEARCH = [
    ('d', [1, 2, 3, 4], 3, 2),
    ('d', [1, 2, 3, 4], 5, None),
    ('d', [1, 2, 3, 4], 0, None),
    ('i', [1, 2, 3, 4], 4, 3),
    ('i', [1, 2, 3, 4], 5, None),
    ('i', [1, 2, 3, 4], 5, None),
    ('i', [1, 1, 1, 1], 1, 0),
    ('i', [], 42, None),
    ('i', [1], 1, 0),
    ('i', [1, 2, 2, 4], 2, 1),
    ('i', [-3, 0, 2, 5, 5], 0, 1),
    ('i', [-3, 0, 2, 5, 5], 5, 3),
    ('i', [-3, 0, 2, 5, 5], 10, None)
]


class TestArray(unittest.TestCase):
    """Тест модуля binary_search"""
    def test_binary_search(self):
        """Тест бинарного поиска"""
        for typecode, data, item, expected_index in TEST_BINARY_SEARCH:
            test_array = array(typecode, data)
            with self.subTest(typecode=typecode, data=data,
                              item=item, expected_index=expected_index):
                self.assertEqual(binary_search.binary(test_array, item), expected_index)
