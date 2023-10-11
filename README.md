# Модуль для работы с динамическими массивами типов данных int, float

В модуле предусмотрены следующие методы:
- создание динамических массивов для чисел разных типов(целые (`long`),
числа с плавающей точкой (`double`));
- создание пустого массива;
- создание массива, заполненного заранее заданными данными;
- реализуйте следующие функции для работы с массивом:
    - добавление элемента в конец массива (`append`);
    - вставка элемента в нужную позицию (`insert`);
    - удаление первого вхождения элемента в массив (`remove`);
    - удаление первого вхождения элемента в массив с возвратом (`pop`);
    - инвертирование массива (`__reversed__` для поддержки функции `reversed`);
    - определение длины массива (поддержка функции `len`);
    - определение количества памяти, занимаемой массивом (`sys.getsizeof`, `__sizeof__`);
    - сравнение со стандартным массивом из модуля array или списком (`__eq__`);
- возможность итерирования по массиву;
- алгоритм бинарного поиска, возвращающий индекс найденного элемента
или `None` если ничего не найдено

##  Общее

Модуль `dynamic_array_c` выполнен как Си-расширение для питон - написан на Cython.

Метод инициализации класса `array` может принимать два аргумента:
- код типа в виде строки, `'d'` для чисел с плавающей точкой и `'i'`
для целых чисел;
- набор инициализирующих данных, которые сразу будут занесены в массив.

Модуль `binary_search` содержит алгоритм бинарного поиска. Поддерживает работу с 
объектами из `dynamic_array`.

```python
search(array: Iterable, item: Any=False) -> Optional[int]:
```

В Файлах `test_dynamic_array.py` и`test_binary_search.py` 
размещены тесты для проверки решения. Тесты можно запустить с помощью 
модуля `unittest` или `pylint`.

Для компиляции этого модуля на Cython команда:

```bash
python setup.py build_ext --inplace
```

Запустить тесты можно командой:

```bash
pytest test_dynamic_array.py -s
```

## Входные и выходные данные

Пример входных данных для бинарного поиска:

Исходный список: ```[-3, 0, 2, 5, 5]```, ```0```<br>
Результат: ```1```<br>

Исходный список: ```[-3, 0, 2, 5, 5]```, ```5```<br>
Результат: ```3```<br>

Исходный список: ```[-3, 0, 2, 5, 5]```, ```10```<br>
Результат: ```None```<br>
# -
