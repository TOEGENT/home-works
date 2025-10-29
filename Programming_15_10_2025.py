import difflib
import re


def safe_input(string="", expect_type=str, filter=lambda x: x):
    while True:
        if not (isinstance(expect_type, re.Pattern)):  # если не регулярное выражение
            try:
                temp = expect_type(
                    input(string)
                )  # Если expect_type — скомпилированное регулярное выражение, то проверяем ввод через полное совпадение (re.fullmatch)
                if filter(temp):  # если подходит по условию
                    return temp
                else:
                    print("Неверный ввод!")
            except (ValueError, TypeError):
                print("Неверный ввод!")
        else:  # если регулярка, то смотрим на соответствие
            user_input = input(string)
            if re.fullmatch(expect_type, user_input):
                return user_input
            print("Неверный ввод!")


def closest_match(target, choices):
    return difflib.get_close_matches(target, choices, n=1, cutoff=0)[
        0
    ]  # cutoff=0 гарантирует, что всегда вернётся хотя бы один "наиболее близкий" вариант,
    # даже если совпадение очень слабое (для улучшения UX в интерактивном режиме)


# 1 угадай число

"""
from random import randint


def guess_num(num,tryes):
    if tryes==0:
        print(f"Попыток не осталось! Вы не угадали число {num}")
        return 0
    if tryes==1:
        if num%2==0:
            guess = safe_input("угадай число (оно чётное) ", int)
        else:
            guess = safe_input("угадай число (оно нечётное) ", int)
    else:
        guess = safe_input("угадай число ",int)
    if guess==num:
        print("Поздравляю! Вы угадали!")
        return 1
    elif guess<num:
        print(f"Не угадали! Число больше! Осталось {tryes-1} попыток")
    else:
        print(f"Не угадали! Число меньше! Осталось {tryes-1} попыток")
    return guess_num(num,tryes-1)

guess_num(100,3)

"""


# 2 text analyzer
'''
from collections import Counter
vowels="aeiouyаеёиоуыэюя"
text = safe_input("Введите строку текста ")
counts = Counter(text)
top_3 = ", ".join([i[0] for i in counts.most_common(3)]) # most_common возвращает связку символ-количество, поэтому берём первый элемент циклом
vowels_count = sum([text.count(vowel) for vowel in vowels ])
print(f"""----------------СТАТИСТИКА----------------
количество гласных символов: {vowels_count}
количество негласных символов: {len(text)-vowels_count}
количество пробелов: {text.count(" ")}
топ 3 самых встречающихся сисволов: {top_3}
количество слов: {len(text.split(" "))}
""")
'''
# 3 rock_paper_scissors
"""
from random import choice

def rock_paper_scissors(wins_):
    moves = ["камень", "ножницы", "бумага"]
    def winner(robot, player):
        robot_id = moves.index(robot)
        player_id = moves.index(player)
        comb = {
            0:2,
            1:0,
            2:1,
        }
        if comb[robot_id]==player_id:
            return "игрок"
        elif comb[player_id]==robot_id:
            return "робот"
        else:
            return "ничья"

    print("Добро пожаловать в 'Камень-ножницы-бумага!")
    wins = {"игрок":0,
            "робот":0}
    while wins["робот"]<wins_ and wins["игрок"]<wins_:
        player_input = safe_input("Введите то, что будете выкидывать (камень/ножницы/бумага) ")
        player_choice = closest_match(player_input, moves)
        robot_choice = choice(moves)
        result = winner(robot_choice,player_choice)
        if result!="ничья":
            wins[result]+=1
        print(f"Ваш выбор: {player_choice}")
        if result!="ничья":
            print(f"робот выбрал {robot_choice}, {result} победил! победы {result}а: {wins[result]}!")
        else:
            print(f"робот выбрал {robot_choice}, {result}!")
    if wins["игрок"]==wins_:    
        print("Вы победили!")
    else:
        print("Вы проиграли!")
rock_paper_scissors(3)
"""

# 5 - bank

from random import randint
from datetime import datetime


class Card:
    def __init__(self, name):
        self.id = "".join(
            [str(randint(0, 9)) for i in range(16)]
        )  # Учебная реализация: настоящие номера карт должны проходить проверку по алгоритму Луна

        self.expiration = (datetime.now().day, datetime.now().year + 10)
        self.code = "".join(
            [str(randint(0, 9)) for i in range(3)]
        )  # В реальных системах CVV НИКОГДА не хранится и не проверяется таким образом!

        self.balance = 100
        self.name = name

    def statistic(self, balance=1, id=1, exp=1, ccv=1):
        print(f"Статистика карты {self.name}")

        if id:
            print(f"Номер карты: {self.id}")
        if exp:
            print(f"Дата истечения: {self.expiration}")
        if ccv:
            print(f"CCV: {self.code}")
        if balance:
            print(f"Баланс {self.balance}")


class Bank_Account:
    def __init__(self):
        self.cards = []

    def create_card(self):
        name_ = safe_input("Введите имя для новой карты: ")
        confirmation = closest_match(
            safe_input(
                "Вы уверены что хотите создать новую банковскую карту? "
            ).lower(),
            ["да", "нет"],
        )
        if confirmation == "да":
            self.cards.append(Card(name_))
            self.find_card_by_id(name_).statistic()

    def find_card_by_id(self, id):
        for card in self.cards:
            if card.id == id or card.name == id:
                return card
        return None

    def add_funds(self):
        print("выберите карту, в которую хотите пополнить деньги")
        for card in self.cards:
            print(card.name)
        _choice = closest_match(safe_input(), [card_.name for card_ in self.cards])
        choiced_card = self.find_card_by_id(_choice)
        choiced_card.statistic()
        amount = safe_input(
            f"Введите сколько хотите пополнить для карты {choiced_card.name} ", int
        )
        confirmation = closest_match(
            safe_input(
                f"Делаем пополнение для карты {choiced_card.name} в размере {amount}? "
            ),
            ["да", "нет"],
        )
        if confirmation == "да":
            choiced_card.balance += amount
            choiced_card.statistic(id=0, ccv=0, exp=0)

    def deduction(self):
        print("выберите карту, c которой хотите списать деньги")
        for card in self.cards:
            print(card.name)
        _choice = closest_match(safe_input(), [card_.name for card_ in self.cards])
        choiced_card = self.find_card_by_id(_choice)
        choiced_card.statistic()
        amount = safe_input(
            f"Введите сколько хотите снять с карты {choiced_card.name} ",
            int,
            lambda x: x <= choiced_card.balance,
        )
        confirmation = closest_match(
            safe_input(f"Списываем с карты {choiced_card.name} {amount}? "),
            ["да", "нет"],
        )
        if confirmation == "да":
            choiced_card.balance -= amount
            choiced_card.statistic(id=0, ccv=0, exp=0)

    def transfer(self):
        while True:
            card_id = safe_input(
                "Введите номер вашей карты, с которой будет производится списание:\n ",
                re.compile(r"^\d{13,19}$"),
            )
            card = self.find_card_by_id(card_id)
            if card == None:
                print("Такой карты у вас нет!")
                continue
            card_CCV = safe_input("Введите код CCV:\n ", re.compile(r"^\d{3}$"))
            if card_CCV == card.code:
                card.statistic()
                money = safe_input(
                    "Введите сумму, которую хотите списать ",
                    int,
                    filter=lambda x: x <= card.balance,
                )
                card_id2 = safe_input(
                    "Введите номер вашей карты, на которую будет производится пополнение:\n ",
                    re.compile(r"^\d{13,19}$"),
                )
                card2 = self.find_card_by_id(card_id2)
                if card2 == None:
                    print("Такой карты у вас нет!")
                    continue
                card_CCV2 = safe_input("Введите код CCV:\n ", re.compile(r"^\d{3}$"))
                if card_CCV2 == card2.code:

                    card2.statistic()
                    inp = safe_input(
                        f"Подтвердить перевод c карты {card.name} на карту {card2.name} в размере {money}? "
                    )
                    user_choice = closest_match(inp.lower(), ["да", "нет"])
                    if user_choice == "да":
                        card.balance -= money
                        card2.balance += money
                        card.statistic(id=0, exp=0, ccv=0)
                        card2.statistic(id=0, exp=0, ccv=0)
                        return 1
                    else:
                        break
                else:
                    print("Неверный код!")

            else:
                print("Неверный код!")

    def check_bank_account(self):
        print("выберите карту, о которой хотите узнать инфомацию")
        for card in self.cards:
            print(card.name)
        _choice = closest_match(safe_input(), [card_.name for card_ in self.cards])
        choiced_card = self.find_card_by_id(_choice)
        choiced_card.statistic()

    def GUI(self):
        print(
            "Добро пожаловать в меню управления счётом в банке! Чтобы выйти напишите 'выход'"
        )

        while True:
            print("Выберите действие:")
            moves = ["перевод", "пополнение", "списание", "проверка", "создание"]

            function_call = dict(
                zip(
                    moves,
                    [
                        self.transfer,
                        self.add_funds,
                        self.deduction,
                        self.check_bank_account,
                        self.create_card,
                    ],
                )
            )  # вызов соответствующей функции
            move_raw = safe_input(
                "Перевод/Пополнение счёта / Списание со счёта / Проверка баланса счёта / Создание новой карты "
            )
            if move_raw == "выход":
                return 1
            function_call[
                closest_match(
                    move_raw.lower(),
                    ["перевод", "пополнение", "списание", "проверка", "создание"],
                )
            ]()  # преобразование ввода пользователя и вызов нужной функции


account = Bank_Account()
account.GUI()
