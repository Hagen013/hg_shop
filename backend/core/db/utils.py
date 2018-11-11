from itertools import chain


SORTING_PATTERN = {
    'Вид установки': 0,
    'Корпус': 1,
    'Цвет корпуса': 2,
    'Тип цоколя': 3,
    'Тип светодиода': 4,
    'Количество светодиодов, шт.': 5,

    'Цвет': 6,
    'Длина волны, нм': 7,
    'Цветовая температура, °К': 8,
    'Коэффициент CRI': 9,
    'Производитель кристалла': 10,

    'Входное напряжение, В': 11,
    'Входной ток, А': 12,
    'Выходное напряжение, В': 13,
    'Выходной ток, А': 14,
    'Мощность, Вт': 15,

    'Световой поток, Лм': 16,
    'Номинальная освещенность, люкс': 17,
    'Сила света, мкд': 18,

    'Угол свечения, °': 19,
    'Угол обзора, °': 20,
    'Дальность действия, м': 21,
    'Задержка включения, с': 22,
    'Управление': 23,
    'Количество выходных каналов': 24,
    'Количество подключаемых зон': 25,
    'Особенности': 26,

    'Габаритный размер, мм': 27,
    'Установочный размер, мм': 28,
    'Диаметр, мм': 29,
    'Установочный диаметр, мм': 30,
    'Высота': 31,
    'Ширина': 32,
    'Шаг нарезки, мм': 33,

    'Рабочая температура, °С': 34,
    'Степень защиты': 35,
    'Срок службы, ч': 36,

    'Единица измерения': 37,
    'Норма упаковки': 38,

    'Техническая документация': 39,

    'Сопутствующие товары': 40}


SORTING_KEY = lambda attribute_pair: SORTING_PATTERN[attribute_pair[0]]

# Сортировка аттрибутов продукта из JSONFild в соответствии
# c SORING_PATTERN

def sort_attributes(attributes, sorting_key=SORTING_KEY):
    try:
        return sorted(attributes.items(), key=sorting_key)

    # В случае возникновения ошибки при наличии в аттрибутах товара
    # отсутствующего в SORTING_PATTERN ключа возвращаем отсортированные
    # пары + отсутсвующие добавляются в конец списка
    except KeyError:
        attrs_keys = set(attributes.keys())
        patrn_keys = set(SORTING_PATTERN.keys())
        
        difference = attrs_keys.difference(patrn_keys)
        intersection = attrs_keys.intersection(patrn_keys)

        if len(intersection) > 0:
            body = dict((k, attributes[k]) for k in intersection)
            body = sorted(body.items(), key=sorting_key)
        else:
            body = []
        # Для tale длину не проверяем - наличие ключа возбудило исключение
        tale = (dict((k, attributes[k]) for k in difference)).items()

        return chain(body, tale)

