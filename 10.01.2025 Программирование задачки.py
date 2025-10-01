# 1 - шифр цезаря
"""
import random

def cezar(text,sdvig,decode=False):
    dictt = {}
    r_dictt={}
    symbols = sorted(list(set(text)))
    for symbol_id in range(len(symbols)):
        if -len(symbols)<=symbol_id+sdvig<len(symbols):
            symbol_id_plus_sdvig=symbol_id+sdvig
        elif symbol_id+sdvig>=len(symbols):
            symbol_id_plus_sdvig=(symbol_id+sdvig)%(len(symbols))
        else:
            symbol_id_plus_sdvig=-(symbol_id+sdvig)%(len(symbols))

        dictt[symbols[symbol_id]]=symbols[symbol_id_plus_sdvig]
        r_dictt[symbols[symbol_id_plus_sdvig]]= symbols[symbol_id]
    new_text = ""
    if not decode:
        for i in text:
            new_text+=dictt[i]
        return new_text
    else:
        for i in text:
            new_text+=r_dictt[i]
        return new_text

text = input("Введите текст ")
while 1:
    try:
        sdvig = int(input("Введите сдвиг "))
        break
    except:
        pass


if input(f"Шифрованный текст: {cezar(text,1)}. Хотите дешифровать текст? (Y\\N) ") in ["y","Y"]:
    print(cezar(cezar(text,1),1,1))
"""

# 2 stas
"""
def check_winner(scores,student_score):
    if student_score in sorted(scores)[-3:] or student_score>scores[-1]:
        print(sorted(scores)[-3:],student_score)
        print("Вы в тройке победителей!")
    else:
        print("Вы не попали в тройку победителей.")
while 1:
    try:
        l = input("Введите список баллов участников олимпиады по формату: n1,n2,n3,...,nk ")
        l = list(map(int, l.split(",")))

        break
    except:

        pass
while 1:
    try:
        sc = int(input("Введите количество баллов, которое заработал stas "))
        break
    except:
        pass

check_winner(l,sc)
"""
# 3 pekarnya
"""

def print_pack_report(num:int):
    if num%3==0 and num%5==0:
        print(f"{num} - расфасуем по 3 или по 5")
    elif num%3==0 and not(num%5==0):
        print(f"{num} - расфасуем по 3")
    elif not (num % 3 == 0) and num%5==0:
        print(f"{num} - расфасуем по 5")
    else:
        print(f"{num} - не заказываем!")

while 1:
    try:
        inp = int(input("Введите ЦЕЛОЕ число БОЛЬШЕ 1 (1 например) "))

        break
    except:

        pass
print_pack_report(inp)
"""
#4
"""
from random import choice,shuffle
from string import printable
nums = printable[:10]
abc=printable[10:31]
ABC = printable[31:62]
spec = printable[62:]
while 1:
    try:
        length = int(input("Введите длину пароля"))
        break
    except:

        pass
nums_allow = input("Добавить цифры? (Y/N)").upper()
ABC_allow = input("Добавить верхний регистр? (Y/N)").upper()
spec_allow = input("Добавить специальные символы? (Y/N)").upper()
abs_allow = input("Добавить нижний регистр? (Y/N)").upper()

result = []
total_parts=0
if abs_allow=="Y":
    total_parts+=1
if ABC_allow=="Y":
    total_parts+=1
if nums_allow=="Y":
    total_parts+=1
if spec_allow=="Y":
    total_parts+=1

if abs_allow=="Y":
    abc_part = [choice(abc) for i in range(length//total_parts)]
    result+=abc_part
if ABC_allow=="Y":
    ABC_part = [choice(ABC) for i in range(length//total_parts)]
    result+=ABC_part
if nums_allow=="Y":
    nums_part = [choice(nums) for i in range(length//total_parts)]
    result+=nums_part
if spec_allow=="Y":
    spec_part = [choice(spec) for i in range(length//total_parts)]
    result+=spec_part

shuffle(result)
print("".join(result))
"""
#5 rimsky cool
def converter(roman_tests):
    roman_to_int = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    result = []
    for num in roman_tests:
        if isinstance(num,str):
            most = "I"
            for i in num:
                if roman_to_int[i]>=most:
                    result
