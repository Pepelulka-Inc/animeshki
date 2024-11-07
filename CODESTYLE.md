# Best practises python

принципы распространяются на все проекты

## Общее
* Снижать когнитивную нагрузку для тех, кто будет читать и использовать код
* Держать близкие по сути сущности близко к друг другу
* Простое лучше сложного
* Явное лучше неявного

## Форматировние

Для форматирования используем ruff с длиной строки 100 символов, форматируем все
```python
ruff format src tests
```

## Типизация
Все методы функции и классы должны иметь аннотации типов
* Аннотировать все аргументы и возвращаемые значения
* Не аннотировать возвращаемое значение у функций, которые ничего не возвращают
* Полностью аннотировать Generic типы(List[int], List[Any], а не List или list)
* не использовать list/dict аннотации, использовать List/ Dict

## Тесты

Для unit-тестов используем pytest

## Дизайн и проектирование

1.1 Импорты
* Импорты разделены на категории, отделяемые одним переносом строки: стандартные модули(typing, os, random...) внешние модули(aiokafka, attrs) потом наши внутренние модули, если они будут
* Не использовать относительные импорты
* Не использовать импорты со звездочкой
* Если символов для импорта больше 10 использовать as
```python
# Плохо
from foo import *
from foo import something, SOME_OTHER_THING, ANOTHER_LONG_FUCKING_THING, thing_with_extremely_long_name, kek, another thing
from foo import (something, SOME_OTHER_THING, ANOTHER_LONG_FUCKING_THING, thing_with_extremely_long_name,
                    kek, another thing)
from numpy import *

# Хорошо
import numpy as np
from foo import(
        SOME_OTHER_THING,
        something,
        ANOTHER_LONG_FUCKING_THING,
        kek,
        another_thing
)
```

1.2 Названия классов и интерфейсов
* Названия классов исключительно CamelCase
* В аббревиатурах только первая заглавная Http, Url
* Префикс I для интерфейсов
* Префикс Base для базовых классов
* Префикс _ если класс приватный и используется только на уровне модуля
* Для классов, которые реализуют интерфейсы суффикс в виде названия основного интерфейса MyHandler: IHandler

1.3 Аргументы, kwargs
* Стараться избегать kwargs, если нужны - указывать тип
* Если у функции больше 2-ух аргументов вызывать только через явное указание аргументов a=b


1.4*

Давайте #TODO ставить только если заведена таска(?)