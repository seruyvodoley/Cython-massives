"""модуль для создания и работы с динамическими массивами"""
# cython: language_level = 3
# distutils: language = c
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
from cpython.float cimport PyFloat_FromDouble, PyFloat_AsDouble
from cpython.int cimport PyInt_AsLong

# определение структуры arraydescr для описания типов данных
cdef struct arraydescr:
    char * typecode
    int itemsize
    object (*getitem)(array, int)
    int (*setitem)(array, int, py_object)

# функция для получения элемента типа double
cdef object double_getitem(array a, int index):
    return (<double *> a.data)[index]
    
# функция для установки элемента типа double
cdef int double_setitem(array a, int index, object obj):
    if not isinstance(obj, int) and not isinstance(obj, float):
        return -1

    cdef double value = PyFloat_AsDouble(obj)
    if index >= 0:
        (<double *> a.data)[index] = value
    return 0

# функция для получения элемента типа int
cdef object int_getitem(array a, int index):
    return (<int *> a.data)[index]

# функция для установки элемента типа int
cdef int int_setitem(array a, int index, object obj):
    if not isinstance(obj, int) and not isinstance(obj, float):
        return -1

    cdef int value = PyInt_AsLong(obj)
    if index >= 0:
        (<int *> a.data)[index] = value
    return 0

# дескрипторы для поддерживаемых типов данных
cdef arraydescr[2] descriptors = [
    arraydescr("d", sizeof(double), double_getitem, double_setitem),
    arraydescr("i", sizeof(int), int_getitem, int_setitem)
]

# перечисление для типов данных
cdef enum TypeCode:
    INT = 1
    DOUBLE = 0

# преобразование символа типа данных в enum TypeCode
cdef int char_typecode_to_int(str typecode):
    if typecode == "d":
        return TypeCode.DOUBLE
    if typecode == "i":
        return TypeCode.INT
    return -1

def degree_of_two(number):
    """
    проверяет, является ли число степенью двойки

    :param number: проверяемое число
    :type number: int

    :return: True, если число - степень двойки, иначе False
    :rtype: bool
    """
    if number == 0:
        return False
    if number == 1:
        return True
    if number & 1:
        return False
    return degree_of_two(number >> 1)

cdef class array:
    """
    класс для динамического массива

    Примеры создания:
    - `arr = Array('i', [1, 2, 3])` создает массив с целыми числами
    - `arr = Array('d', [1.0, 2.0, 3.0])` создает массив с числами с плавающей запятой
    """
    cdef public size_t length
    cdef char * data
    cdef arraydescr * descr
    cdef int capacity
    cdef str mtypecode

    def __cinit__(self, str typecode = 'i', object obj = []):
        """
        конструктор класса array

        :param typecode: тип данных массива ('d' для double, 'i' для int)
        :type typecode: str
        :param obj: инициализирующий список (по умолчанию None)
        :type obj: object

        :raises MemoryError: если не удалось выделить память для массива
        """
        self.mtypecode = typecode
        cdef int mtypecode = char_typecode_to_int(typecode)
        self.descr = &descriptors[mtypecode]

        self.length = len(obj)
        self.capacity = self.length
        while not degree_of_two(self.capacity):
            self.capacity += 1
        self.data = <char *> PyMem_Malloc((self.capacity * 2) * self.descr.itemsize)

        for i in range(self.length):
            self.__setitem__(i, obj[i])
        if not self.data:
            raise MemoryError

    def __dealloc__(self):
        """
        освобождение памяти, занятой массивом, при удалении объекта
        """
        PyMem_Free(self.data)

    def initialize(self):
        """
        Инициализация массива значениями от 0 до length-1
        """
        cdef int i
        if self.mtypecode == "i":
            for i in range(self.length):
                self.__setitem__(i, i)
        elif self.mtypecode == "d":
            for i in range(self.length):
                self.__setitem__(i, float(i))


    def len(self):
        """
        длина массива
        :return: длина массива
        :rtype: int
        """
        return self.length

    def append(self, item):
        """
        добавить в конец

        :param item: элемент для добавления
        :type item: int / float

        :raises ValueError: елси не число и не дробь
        """
        if self.mtypecode == "i" and isinstance(item, int) or self.mtypecode == "d" and isinstance(item, float):
            new_length = self.length + 1
            if self.capacity == new_length:
                self.capacity *= 2
                self.data = <char *> PyMem_Realloc(self.data, self.capacity * self.descr.itemsize)
            self.length += 1
            self.__setitem__(self.length - 1, item)
        else:
            raise ValueError("Тип данных не подходит для массива")

    def remove(self, item):
        """
        удалить первый попавшийся жлемент из массива
        :param item: удаляемый элемент
        :type item: int / float

        :raises ValueError:  если нет такого элемента
        """
        cdef int index = -1
        for i in range(self.length):
            if self[i] == item:
                index = i
                break
        if index != -1:
            for i in range(index, self.length - 1):
                self[i] = self[i + 1]
            self.length -= 1
            if self.length * 2 < self.capacity:
                self.data = <char *> PyMem_Realloc(self.data, self.length * self.descr.itemsize)
        else:
            raise ValueError("такого элемента нет")

    def insert(self, index, item):
        """
        вставить жлемент по индексу

        :param index: индекс для вставки
        :type index: int
        :param item: элемент для вставки
        :type item: int / float
        """
        if index < 0:
            index = self.length + index  # Преобразование отрицательного индекса в положительный
        if 0 <= index < self.length:
            self.data = <char *> PyMem_Realloc(self.data, (self.length + 1) * self.descr.itemsize)
            self.length += 1
            prev_element, self[index] = self[index], item
            for i in range(index + 1, self.length):
                prev_element, self[i] = self[i], prev_element
        elif index >= self.length:
            self.append(item)
        else:
            self.data = <char *> PyMem_Realloc(self.data, (self.length + 1) * self.descr.itemsize)
            self.length += 1
            prev_element, self[index] = self[index], item
            for i in range(index, 0, -1):
                prev_element, self[i] = self[i], prev_element

    def pop(self, index = -1):
        """
        удалиь и вернуть элемент по индексу

        :param index: индекс удалемого
        :type index: int

        :return: удаленный элемент
        :rtype: int/float

        :raises IndexError: если индекса нет в массиве
        """
        if index < 0:
            if abs(index) > self.length:
                raise IndexError
            else:
                index = self.length + index
        else:
            if index >= self.length:
                raise IndexError
        deleted_element = self[index]
        for i in range(index, self.length - 1):
            self[i] = self[i + 1]
        self.length -= 1
        self.data = <char *> PyMem_Realloc(self.data, self.length * self.descr.itemsize)
        return deleted_element


    def reversed(self):
        """
        вывести массив наоборот

        :return: массив перевертыш
        :rtype: Array
        """
        swap, reverse_index  = 0, -1
        for i in range(self.length // 2):
            swap = self[i]
            self[i] = self[reverse_index]
            self[reverse_index] = swap
            reverse_index -= 1

    def __getitem__(self, int index):
        """
        возвращать элемент по индексу

        :param index: индекс элемента
        :type index: int

        :return: эдемент массива
        :rtype: int or float

        :raises IndexError: если такого индекса нет
        """
        if 0 <= index < self.length:
            return self.descr.getitem(self, index)
        elif (self.length * (-1)) <= index <= -1:
            index = self.length + index
            return self.descr.getitem(self, index)
        else:
            raise IndexError

    def __setitem__(self, int index, object value):
        """
        установить ноове значение ждя элемента по индексу

        :param index: индекс изменяемого
        :type index: int
        :param value: новое значение для элемента
        :type value: int / float

        :raises IndexError: если такого индекса нет
        """
        if not isinstance(value, (int, float)):
            raise ValueError("надо int или float")
        if 0 <= index < self.length:
            self.descr.setitem(self, index, value)
        elif (self.length * -1) <= index <= -1:
            index = self.length + index
            self.descr.setitem(self, index, value)
        else:
            raise IndexError

    def __len__(self):
        """
        длина массива
        :return: длина массива
        :rtype: int
        """
        return self.length

    def __sizeof__(self):
        """
        получить размер массива в памяти
        :return: сколько памяти занимет
        :rtype:int
        """
        return self.descr.itemsize * self.capacity

    def __eq__(self, array other):
        """
        проверим равенство двух массивов

        :param other: другой массив для сравнения
        :type other: array

        :return: True, если массивы равны, False в противном случае
        :rtype: bool
        """
        if isinstance(other, array):
            if self.length == other.length:
                for i in range(self.length):
                    if self[i] != other[i]:
                        return False
                return True
        return False

    def __str__(self):
        """
        вернуть строку

        rtype: str
        return: список в строковом виде
        """
        return str(list(self))

    # метод для итерации
    def __iter__(self):
        """
        просто методдля итерации
        :rtype: Array
        """
        for i in range(self.length):
            yield self[i]
