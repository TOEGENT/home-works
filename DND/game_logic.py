from random import choices
from textwrap import dedent

from DND.goofy_user_protection import safe_input, closest_match


class Item:
    def __init__(self, name: str, description: str, owner):
        self.name = name
        self.description = description
        self.owner = owner

    def get_description(self):
        print(
            dedent(
                f"""
            ОПИСАНИЕ ПРЕДМЕТА {self.name}
            {self.description}
            """
            )
        )

    def use(self):
        print("В бою этот предмет не получится использовать!")


class HealthBottle(Item):
    def __init__(self, name, description, hp):

        super().__init__(name=name, descrition=description)
        self.hp = hp

    def use(self):
        self.owner.hp += self.hp


class Inventory:
    def __init__(self,owner, **items:Item):
        self.owner=owner
        self.items = items
    def show_items(self):
        print(f"ИНВЕНТАРЬ ИГРОКА {self.owner.name} (для выбора предмета напишите его id или название)")
        for id,item in enumerate(self.items,1):
            print(f"{id} - {item}")








class Mob:
    def __init__(self, name, hp, defence, damage, luck, inventory):
        self.name = name
        self.hp = hp
        self.defence = defence
        self.damage = damage
        self.luck = luck
        self.inventory =inventory

    def attack(self, other):
        other.hp -= choices(
            [self.damage, 0], [self.luck * (1 - other.defence / 100), 1 - self.luck]
        )[0]

    def get_stats(self):
        print(
            dedent(
                f"""
                СТАТУС ГЕРОЯ {self.name}:
                - {self.hp} здоровья
                - {self.defence} защиты
                - {self.damage} наносимого урона противникам
                - {self.luck} удачи
                """
            )
        )

    def get_inventory(self):
        return self.inventory.show_items()



class Wizard(Mob):
    def __init__(self, name, hp, defence, damage, luck):
        super().__init__(name=name, hp=hp, defence=defence, damage=damage, luck=luck)



class Warrior(Mob):
    def __init__(self, name, hp, defence, damage, luck):
        super().__init__(name=name, hp=hp, defence=defence, damage=damage, luck=luck)


class Gunner(Mob):
    def __init__(self, name, hp, defence, damage, luck):
        super().__init__(name=name, hp=hp, defence=defence, damage=damage, luck=luck)
