# 1 - шифр цезаря

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
"""
MCMLXXXIV
1) 5 (V)
2) 1 - I<V (V) -> 5-1=4
3) X - X>V (X) -> 4+10 = 14
4) X - X=X (X) -> 14+10 = 24
5) X - X=X (X) -> 24+10 = 34
6) L - L>X (L) -> 34+50 = 84
7) M -> M>L (M) -> 84+1000 = 1084
8) C -> C<M (M) -> 1084-100 = 984
9) M -> M=M (M) -> 984+1000 = 1984

1984

1) 4 -> V -> 5-4=1 -> I -> IV
2) 80 -> C -> 100-80=20 -> 20 not in roman.values -> L -> 80-50 = 30 not in roman.values -> closest div = 10 -> 30/10 = 3 -> XXX -> LXXX
3) 900 -> M -> 1000-900 -> 100 -> C -> CM
4) 1000 - M
result = MCMLXXXIV
"""

#5 rimsky cool
"""
def converter(roman_tests):
    roman_to_int = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000,
    }
    int_to_roman = {
        1: 'I',
        5: 'V',
        10: 'X',
        50: 'L',
        100: 'C',
        500: 'D',
        1000: 'M'
    }
    result = []
    for num in roman_tests:
        if isinstance(num,str):
            num=num[::-1]
            most = num[0]
            total = roman_to_int[num[0]]
            for i in num[1:]:
                if roman_to_int[i]>=roman_to_int[most]:
                    total+=roman_to_int[i]
                    most = i
                else:
                    total-=roman_to_int[i]
            result.append(total)
        else:
            total=""
            snum = str(num)[::-1]
            c=0
            for i in snum:
                if i=="0":
                    c+=1
                    continue
                i+=c*"0"
                l = sorted([(abs(int(i)-j),j) for j in roman_to_int.values()])
                closest_plus = l[0]
                remain = closest_plus[0]
                closest = closest_plus[1]
                if int(i) in int_to_roman.keys():
                    total=int_to_roman[int(i)]+total
                elif remain in int_to_roman.keys():
                    if closest<int(i):
                        total = int_to_roman[closest] + int_to_roman[remain] +  total
                    else:
                        total=int_to_roman[remain]+int_to_roman[closest]+total
                else:
                    if closest>int(i):
                        second_closest_plus = l[1]
                        remain = second_closest_plus[0]
                        closest = second_closest_plus[1]
                        if remain in int_to_roman.keys():
                            total +=int_to_roman[closest]+int_to_roman[remain]

                    closest_div = 0
                    mod=float("inf")
                    for i in sorted(list(int_to_roman.keys()),reverse=True):
                        if remain%i==0:
                            closest_div=i
                            break
                    total =int_to_roman[closest] + remain//closest_div*int_to_roman[closest_div] + total # остаток допустим 30 (80-50) разбиваем на 3*10 = XXX
                c+=1
            result.append(total)
    return result
print(converter([i for i in range(1,1000)]))
print(converter(converter([i for i in range(1,1000)])))
"""
"""
words = ["лололошка", "бананы"]
from random import choice

def play_deadman(tryes=6):  # уменьшил попытки до 6 — как в классике
    word = words[choice(range(len(words)))]
    guess_total = ["_" for _ in range(len(word))]
    print("Добро пожаловать в висельницу! Ваша задача - угадать слово быстрее, чем человек успеет повесится. Удачи!")

    for _ in range(tryes):  
        print("".join(guess_total))

        guess_symbol = input("Введите букву: ").lower()

        if guess_symbol in word:
            for i, letter in enumerate(word):
                if letter == guess_symbol:
                    guess_total[i] = guess_symbol
            print("Угадали!")
        else:
            print("Не угадали!")

        if "".join(guess_total) == word:
            print("Вы угадали слово! Поздравляю!")
            return 1

    print(f"Вы так долго угадывали слово, что человек уже успел повесится! Заданное слово было {word}")
    return 0

play_deadman()
"""
