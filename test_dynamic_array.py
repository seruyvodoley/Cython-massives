"""тесты для модуля dynamic_array_c"""

import unittest
from dynamic_array_c import array
import time

TEST_LEN = [
    ('d', [], 0),
    ('d', [1.0], 1),
    ('d', [1.0, 1.0], 2),
    ('d', [1.0, 2.0], 2),
    ('d', [1.0, 9999.0, 3.0, 4.0, 1.0], 5),
    ('i', [], 0),
    ('i', [1], 1),
    ('i', [1, 1], 2),
    ('i', [1, 2], 2),
    ('i', [1, 9999, 3, 4, 1], 5),
]

TEST_GETITEM = [
    ('d', [2.0, 3.0, 4.0], 3),
    ('i', [5, 1, 1], 3),
]

TEST_APPEND = [
    ('d', [], 1.0, array('d', [1.0])),
    ('d', [1.0], 1.0, array('d', [1.0, 1.0])),
    ('d', [2.0], 1.0, array('d', [2.0, 1.0])),
    ('d', [2.0, 5.0], 1.0, array('d', [2.0, 5.0, 1.0])),
    ('i', [], 1, array('i', [1])),
    ('i', [1], 1, array('i', [1, 1])),
    ('i', [2], 1, array('i', [2, 1])),
    ('i', [2, 5], 1, array('i', [2, 5, 1])),
]

TEST_APPEND_ERROR = [
    ('d', [], "string"),
    ('d', [1.0], "string"),
    ('i', [1], "string")
]

TEST_INSERT = [
    ('d', [], 0, 8.0, array('d', [8.0])),
    ('d', [2.0, 5.0], 1, 8.0, array('d', [2.0, 8.0, 5.0])),
    ('d', [2.0, 5.0], -1, 8.0, array('d', [2.0, 8.0, 5.0])),
    ('d', [2.0, 5.0], -2, 8.0, array('d', [8.0, 2.0, 5.0])),
    ('i', [], 0, 8, array('i', [8])),
    ('i', [1], 0, 8, array('i', [8, 1])),
    ('i', [2, 5], 1, 8, array('i', [2, 8, 5])),
    ('i', [2, 5], 1, 8, array('i', [2, 5, 8])),
    ('i', [4, 4, 1], -1, 8, array('i', [4, 4, 8, 1])),
    ('i', [4, 4, 1], -3, 8, array('i', [8, 4, 4, 1]))
]

TEST_REMOVE = [
    ('d', [1.0], 1.0, array('d', [])),
    ('d', [2.0, 2.0, 2.0], 2.0, array('d', [2.0, 2.0])),
    ('d', [2.0, 5.0], 5.0, array('d', [2.0])),
    ('i', [1], 1, array('i', [])),
    ('i', [2, 2, 2], 2, array('i', [2, 2])),
    ('i', [2, 5], 5, array('i', [2])),
]

TEST_POP = [
    ('d', [1.0], 0, 1.0, array('d', [])),
    ('d', [2.0, 1.0, 6.0], 1, 1.0, array('d', [2.0, 6.0])),
    ('d', [2.0, 5.0], 1, 5.0, array('d', [2.0])),
    ('d', [2.0, 5.0], -1, 5.0, array('d', [2.0])),
    ('d', [2.0, 5.0], -2, 2.0, array('d', [5.0])),
    ('i', [1], 0, 1, array('i', [])),
    ('i', [2, 1, 4], 1, 1, array('i', [2, 4])),
    ('i', [2, 5], 1, 5, array('i', [2])),
    ('i', [2, 5], -1, 5, array('i', [2])),
    ('i', [2, 5], -2, 2, array('i', [5])),
]

TEST_POP_INDEX_ERROR = [
    ('d', [], 1),
    ('d', [10.0], 5),
    ('d', [2.0], -2),
    ('i', [], 1),
    ('i', [3, 1], 5),
    ('i', [4], -2),
]

TEST_REVERSED = [
    ('d', [], array('d', [])),
    ('d', [1.0], array('d', [1.0])),
    ('d', [2.0, 2.0, 2.0], array('d', [2.0, 2.0, 2.0])),
    ('d', [2.0, 5.0], array('d', [5.0, 2.0])),
    ('i', [], array('i', [])),
    ('i', [1], array('i', [1])),
    ('i', [2, 2, 2], array('i', [2, 2, 2])),
    ('i', [2, 5], array('i', [5, 2])),
]

TEST_EQ = [
    ('d', [], array('d', [])),
    ('d', [1.0], array('d', [1.0])),
    ('d', [2.0, 2.0, 2.0], array('d', [2.0, 2.0, 2.0])),
    ('d', [2.0, 5.0], array('d', [2.0, 5.0])),
    ('i', [], array('i', [])),
    ('i', [1], array('i', [1])),
    ('i', [2, 2, 2], array('i', [2, 2, 2])),
    ('i', [2, 5], array('i', (2, 5))),
]


class TestArray(unittest.TestCase):
    """тест модуля dynamic_array_c"""

    def test_len(self):
        """тест метода len"""
        for typecode, data, expected in TEST_LEN:
            with self.subTest(typecode=typecode, data=data, expected=expected):
                test_array = array(typecode, data)
                self.assertEqual(len(test_array), expected)

    def test_getitem(self):
        """тест индексации"""
        for typecode, data, array_len in TEST_GETITEM:
            test_array = array(typecode, data)
            for index in range(array_len):
                with self.subTest(typecode=typecode, data=data, index=index):
                    item = test_array.__getitem__(index)
                    self.assertEqual(item, data[index])

    def test_getitem_failed(self):
        """тест исключения IndexError при индексации"""
        for typecode, data, array_len in TEST_GETITEM:
            test_array = array(typecode, data)
            for index in [array_len, -(array_len + 1)]:
                with self.subTest(typecode=typecode, data=data, index=index):
                    with self.assertRaises(IndexError):
                        test_array.__getitem__(index)

    def test_setitem(self):
        """тест __setitem__"""
        for typecode, data, array_len in TEST_GETITEM:
            test_array = array(typecode, data)
            for index in range(array_len):
                with self.subTest(typecode=typecode, data=data, index=index):
                    test_array.__setitem__(index, -42)
                    self.assertEqual(test_array[index], -42)

    def test_setitem_failed(self):
        """тест исключения IndexError для __setitem__"""
        for typecode, data, array_len in TEST_GETITEM:
            test_array = array(typecode, data)
            for index in [array_len, -(array_len + 1)]:
                with self.subTest(typecode=typecode, data=data, index=index):
                    with self.assertRaises(IndexError):
                        test_array.__setitem__(index, 42)

    def test_append(self):
        """тест метода append"""
        for typecode, data, item, expected in TEST_APPEND:
            with self.subTest(typecode=typecode, data=data,
                              item=item, expected=expected):
                test_array = array(typecode, data)
                test_array.append(item)
                self.assertEqual(len(test_array), len(expected))
                for i, expected_item in enumerate(expected):
                    array_item = test_array[i]
                    if typecode == 'd':
                        self.assertTrue(isinstance(array_item, float))
                    elif typecode == 'i':
                        self.assertTrue(isinstance(array_item, int))
                    self.assertEqual(array_item, expected_item)

    def test_append_value_error(self):
        """
        работает ли TypeError для append()
        """
        for typecode, data, item in TEST_APPEND_ERROR:
            with self.subTest(typecode=typecode, data=data, item=item):
                test_array = array(typecode, data)
                with self.assertRaises(ValueError):
                    test_array.append(item)

    def test_insert(self):
        """тест метода insert"""
        for typecode, data, index, item, expected in TEST_INSERT:
            with self.subTest(typecode=typecode, data=data, index=index,
                              item=item, expected=expected):
                test_array = array(typecode, data)
                test_array.insert(index, item)
                self.assertEqual(len(test_array), len(expected))

    def test_remove(self):
        """тест метода remove"""
        for typecode, data, item, expected in TEST_REMOVE:
            with self.subTest(typecode=typecode, data=data,
                              item=item, expected=expected):
                test_array = array(typecode, data)
                test_array.remove(item)
                self.assertEqual(len(test_array), len(expected))
                for i, expected_item in enumerate(expected):
                    array_item = test_array[i]
                    if typecode == 'd':
                        self.assertTrue(isinstance(array_item, float))
                    elif typecode == 'i':
                        self.assertTrue(isinstance(array_item, int))
                    self.assertEqual(array_item, expected_item)

    def test_pop(self):
        """тест метода pop"""
        for typecode, data, index, expected_item, expected_array in TEST_POP:
            with self.subTest(typecode=typecode, data=data, index=index,
                              expected_item=expected_item,
                              expected_array=expected_array):
                test_array = array(typecode, data)
                item = test_array.pop(index)
                self.assertEqual(item, expected_item)
                self.assertEqual(len(test_array), len(expected_array))
                for i, ex_item in enumerate(expected_array):
                    array_item = test_array[i]
                    if typecode == 'd':
                        self.assertTrue(isinstance(array_item, float))
                    elif typecode == 'i':
                        self.assertTrue(isinstance(array_item, int))
                    self.assertEqual(array_item, ex_item)

    def test_pop_failed(self):
        """тест метода pop с исключением IndexError"""
        for typecode, data, index in TEST_POP_INDEX_ERROR:
            with self.subTest(typecode=typecode, data=data, index=index):
                test_array = array(typecode, data)
                with self.assertRaises(IndexError):
                    test_array.pop(index)

    def test_reversed(self):
        """тест метода reversed"""
        for typecode, data, expected in TEST_REVERSED:
            with self.subTest(typecode=typecode, data=data, expected=expected):
                test_array = array(typecode, data)
                test_array.reversed()
                self.assertEqual(test_array, expected)

    def test_eq(self):
        """Тест сравнения с array.array"""
        for typecode, data, expected in TEST_EQ:
            with self.subTest(typecode=typecode, data=data, expected=expected):
                my_array = array(typecode, data)
                self.assertEqual(my_array, expected)

    def test_time_append(self):
        start = time.time()
        for _ in range(10000):
            my_array = array('i', [])
            for i in range(10000):
                my_array.append(i)
        print(f"\n\033[33Время append {time.time() - start} сек. \033\0м")