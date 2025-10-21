import difflib
import re
from datetime import datetime
from decimal import Decimal



def safe_input(string="", expect_type=str, filter=lambda x: x):
    while True:
        if not (isinstance(expect_type, re.Pattern)):  # если не регулярное выражение
            try:
                temp = expect_type(input(
                    string))  # Если expect_type — скомпилированное регулярное выражение, то проверяем ввод через полное совпадение (re.fullmatch)
                if filter(temp):  # если подходит по условию
                    return temp
                else:
                    print("Неверный ввод!")
            except(ValueError, TypeError):
                print("Неверный ввод!")
        else:  # если регулярка, то смотрим на соответствие
            user_input = input(string)
            if re.fullmatch(expect_type, user_input):
                return user_input
            print("Неверный ввод!")


def closest_match(target, choices):
    return difflib.get_close_matches(target, choices, n=1, cutoff=0)[
        0]  # cutoff=0 гарантирует, что всегда вернётся хотя бы один "наиболее близкий" вариант,


goods={}
def add(good:dict):
    good_key = list(good.keys())[0]
    good_value = list(good.values())[0][0]
    if good_key in goods.keys():
        goods[good_key].append(good_value)
    else:
        goods.update(good)
def add_by_note(note:str):
    note_splitted = note.split(" ")
    name = note_splitted[0]
    amount=Decimal(note_splitted[1])
    expiration_date=datetime.strptime(note_splitted[2], "%Y-%m-%d")

    return add({name:[{"amount":amount,"expiration_date":expiration_date}]})

def find(name:str) -> list:
    matches=[]
    for key in list(goods.keys()):
        if name.lower() in key.lower():
            matches.append(key)
    return matches

def amount(name):
    return sum(len(goods[match]) for match in find(name))


print("Вы у холодильника")
while 1:
    print("Выберете вариант действий")
    choice=closest_match(safe_input("Положить в холодильник предмет / Найти в холодильнике "),["положить","найти"])
    if choice=="положить":
        choice2 = safe_input("Напишите название предмета, его количество и срок годности (по желанию) по формату: ПРОДУКТ КОЛИЧЕСТВО СРОК\n(срок годности по формату ГОД-МЕСЯЦ-ДЕНЬ) ",add_by_note)
        print("Предмет успешно положен в холодильник!")
    if choice=="найти":
        choice3 = safe_input("Напишите название предмета по формату: ПРОДУКТ ",find)
        print(find(choice3))
