from random import choices
from textwrap import dedent

from DND.goofy_user_protection import safe_input, closest_match
from abc import abstractmethod

class Item:
    def __init__(self, name: str,weight, description: str, owner="unknown"):
        self.name = name
        self.description = description
        self.owner = owner
        self.weight=weight
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
    def __init__(self, name,weight, description,owner, hp):

        super().__init__(name=name,weight=weight, description=description,owner=owner)
        self.hp = hp

    def use(self):
        self.owner.hp += self.hp
class Armor(Item):
    def __init__(self, name,weight, description,owner, defence):

        super().__init__(name=name,weight=weight, description=description,owner=owner)
        self.defence=defence

    def use(self,log=False):
        if self.owner.equipped_armor==None:
            self.owner.defence+=self.defence
            self.owner.equipped_armor=self
            if log:
                print(f"{self.name} было успешно экипировано!")
        else:
            if log:
                print(f"Снимите одежду прежде чем одевать новую!")
    def unuse(self,log=False):
        if self.owner.equipped_armor!=None:
            self.owner.defence-=self.defence
            self.owner.equipped_armor=None
            if log:
                print(f"{self.name} было успешно снято!")
        else:
            if log:
                print(f"Экипируйте одежду прежде чем снимать!")


class Inventory:
    def __init__(self,owner, items:list):
        self.owner=owner
        self.items = items
    def show_items(self):
        print(f"ИНВЕНТАРЬ ИГРОКА {self.owner.name} (для выбора предмета напишите его id или название)")
        for id,item in enumerate(self.items,1):
            print(f"{id} - {item}")
    def add_item(self,item:Item):
        self.items.append(item)









class Mob:
    def __init__(self, name, hp, defence, damage, luck,max_weight):

        self.name = name
        self.hp = hp
        self.defence = defence
        self.damage = damage
        self.luck = luck
        self.inventory=Inventory(self.name,[])
        self.equipped_armor=None
        self.max_weight=max_weight

    def attack(self, other,log=False):
        damage=choices(
            [self.damage*(100/self.other.defence), 0], [self.luck, 1 - self.luck])[0]
        other.hp -= damage
        if log:
            if damage!=0:
                print(f"{self.name} нанёс {damage} урона!")
            else:
                print(f"{self.name} промахнулся!")

    def stats(self):
        return (
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
    def pick_item(self,item):
        pass


class Wizard(Mob):
    def __init__(self, name, hp, defence, damage, luck,stats,max_weight):
        super().__init__(name=name, hp=hp, defence=defence, damage=damage, luck=luck,max_weight=max_weight)
        self.wisdom=stats[0]
        self.concentration=stats[1]
        self.intuition=stats[2]

    def stats(self):
        return (
            dedent(
                f"""
                СТАТУС ГЕРОЯ {self.name}:
                - {self.hp} здоровья
                - {self.defence} защиты
                - {self.damage} наносимого урона противникам
                - {self.luck} удачи
                - {self.wisdom} мудрости
                - {self.concentration} концентрации
                - {self.intuition} интуиции
                """
            )
        )
class Warrior(Mob):
    def __init__(self, name, hp, defence, damage, luck,stats:list,max_weight):
        super().__init__(name=name, hp=hp, defence=defence, damage=damage, luck=luck,max_weight=max_weight)
        self.power=stats[0]
        self.durability=stats[1]
        self.spirit=stats[2]
    def stats(self):
        return (
            dedent(
                f"""
                СТАТУС ГЕРОЯ {self.name}:
                - {self.hp} здоровья
                - {self.defence} защиты
                - {self.damage} наносимого урона противникам
                - {self.luck} удачи
                - {self.power} силы
                - {self.durability} прочности
                - {self.spirit} духа
                """
            )
        )

class Archer(Mob):
    def __init__(self, name, hp, defence, damage, luck,stats:list,max_weight):
        super().__init__(name=name, hp=hp, defence=defence, damage=damage, luck=luck,max_weight=max_weight)
        self.dexterity=stats[0]
        self.vision=stats[1]
        self.stamina=stats[2]
    def stats(self):
        return (
            dedent(
                f"""
                СТАТУС ГЕРОЯ {self.name}:
                - {self.hp} здоровья
                - {self.defence} защиты
                - {self.damage} наносимого урона противникам
                - {self.luck} удачи
                - {self.dexterity} ловкости
                - {self.vision} зрения
                - {self.stamina} выносливости
                """
            )
        )


class World:
    def __init__(self,player,combat_mobs,exploration_mobs,trade_mobs,events):
        self.player=player
        self.combat_mobs=combat_mobs
        self.exploration_mobs=exploration_mobs
        self.events=events
        self.trade_mobs=trade_mobs
    def change_situation(self,situation):
        if situation==Exploration:
            return situation(player=self.player,mobs=self.exploration_mobs,events=self.events,world=self)
        if situation==Combat:
            return situation(player=self.player,mobs=self.combat_mobs,world=self)

class Situation:
    def __init__(self,player:Mob,mobs:list,world:World):
        self.player=player
        self.mobs=mobs
        self.world=world
        self.commands=["/инвентарь","/осмотреться","/атаковать","/использовать"]
    @abstractmethod
    def process_input(self,input:str):
        pass




class Exploration(Situation):
    def __init__(self,player:Mob,mobs:list,events:list,world):
        super().__init__(player,mobs,world)
        self.events=events
        self.commands = ["/инвентарь", "/осмотреться", "/атаковать", "/использовать"]
    def process_input(self,input:str):
        self.subject = None
        if len(input.split(" ")) < 2:
            self.input = closest_match(input, self.commands)
        else:
            self.input=closest_match(input.split(" ")[0],self.commands)
            mobs_names= [mob.name for mob in self.mobs]
            subject_name=closest_match(input.split(" ")[1],mobs_names)
            self.subject = self.mobs[mobs_names.index(subject_name)]

        if self.input=="/инвентарь":
            self.player.get_inventory()
        if self.input=="/осмотреться":
            print("Вокруг вас:")
            for event in self.events+self.mobs:
                print(event.name)
        if self.input=="/атаковать" and self.subject!=None:
            self.world.change_situation(Combat)



class Combat(Situation):
    def __init__(self,player:Mob,mobs:list,subject,world):
        super().__init__(player,mobs,world)
        self.commands = ["/инвентарь", "/атаковать","/бежать" "/использовать"]
        self.subject=subject
        self.process_input("/атаковать")

    def process_input(self,input:str):
        self.input = closest_match(input,self.commands)

        if self.input=="/инвентарь":
            self.player.get_inventory()

        if self.input=="/атаковать":
            self.player.attack(self.subject)
        if self.input=="/бежать":
            total_luck = self.player.luck/100
            for mob in self.mobs:
                total_luck*=mob.luck/100
            action=choices([Exploration,None],[total_luck,1-total_luck])
            if isinstance(action,Exploration):
                self.world.change_situation(Exploration)










