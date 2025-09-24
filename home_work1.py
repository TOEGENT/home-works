#1
"""
number = int(input('Введите ваше число: '))

if number % 2 == 0:
    print('Число четное и ',end="")
else:
    print('Число нечетное и ',end="")

if 10 < number < 50:
    print('принадлежит диапазону')
else:
    print('не принадлежит диапазону')
"""
# 2
"""
from random import choice,shuffle
from string import printable
nums = printable[:10]
abc=printable[10:62]
spec = printable[62:]
length = int(input("Введите длину пароля"))
l_each=length//3
nums_part = [choice(nums) for i in range(l_each)]
abc_part =[choice(abc) for i in range(l_each)]
spec_part = [choice(spec) for i in range(l_each)]
result = nums_part+abc_part+spec_part
shuffle(result)
print("".join(result))
"""

#3
"""
text = input("Введите текст").lower()
unic = set(text)
counts = {}
for s in unic:
    counts[s]=text.count(s)
for i,key in enumerate(counts,1):
    print(f"{i}) : {key} ({counts[key]} раз)")
    if i==3:
        break
"""
