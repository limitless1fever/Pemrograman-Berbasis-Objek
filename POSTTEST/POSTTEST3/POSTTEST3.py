# Nama : Pirlo Syabila Hafuza
# NIM : 2509106008
# Kelas : Informatika A1'25

import random
from abc import ABC, abstractmethod


# Abstract class
class Character(ABC):
    totalCharacter = 0

    def __init__(self, name, health, attack, defence, mana):
        self.name = name
        self.__health = health
        self.attack = attack
        self.defence = defence
        self._mana = mana
        self.skills = []
        self.inventory = Inventory()  # Komposisi
        Character.totalCharacter += 1

    # Abstract method
    @abstractmethod
    def Attacking(self, target):
        pass

    # Abstract method
    @abstractmethod
    def battle_cry(self):
        pass

    # Instance method, dipakai bersama oleh Player dan Enemy
    def introduce(self):
        print(f'{self}')
        self.battle_cry()

    @property
    def mana(self):
        return self._mana

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value > 100:
            print(f'Health {value} Melebihi Batas, Set ke [100]')
            self.__health = 100
        elif value < 0:
            print(f'Health {value} Tidak Valid, Set ke [0]')
            self.__health = 0
        else:
            self.__health = value

    @classmethod
    def total_character(cls):
        return f'Total karakter terdaftar ada: [{cls.totalCharacter}]'

    @staticmethod
    def calculate_damage(attack, defence):
        return max(1, attack - defence)

    def isAlive(self):
        return self.health > 0

    def takeDamage(self, damage):
        hit = self.calculate_damage(damage, self.defence)
        self.health -= hit

        print(f'{self.name} terkena damage sebesar {hit}, sisa HP [{self.health}]/[100] ')

    def add_skill(self, skill: 'Skill'):
        if len(self.skills) >= Skill.maxSkill:
            print(f"{self.name} sudah mencapai batas maksimal skill ({Skill.maxSkill})")
            return
        self.skills.append(skill)  # Agregasi
        print(f"{self.name} mempelajari skill baru: [{skill.name}]")

    def use_skill(self, skill_name, target):
        skill = next((s for s in self.skills if s.name.lower() == skill_name.lower()), None)

        if not skill:
            print(f"{self.name} tidak memiliki skill '{skill_name}'.")
            return False

        if self._mana < skill.mana_cost:
            print(f"Mana {self.name} tidak cukup ({self._mana}/{skill.mana_cost})")
            return False

        print(f'\n{self.name} menggunakan skill [{skill.name}] pada {target.name}')
        self._mana -= skill.mana_cost

        base_damage = self.calculate_damage(self.attack, target.defence)
        final_damage = int(base_damage * skill.damage_multiplier)

        target.takeDamage(final_damage)
        return True

    def use_item(self, item_name):
        result = self.inventory.use_items(item_name)

        if not result:
            print(f"{self.name} tidak memiliki item '{item_name}'.")
            return False

        name, heal = result
        self.health = min(100, self.health + heal)
        print(f'{self.name} menggunakan item [{name}], sisa HP [{self.health}]/[100]')
        return True

    # Operator overloading
    def __str__(self):
        return f'{self.name} | HP: [{self.health}]/[100] | Mana: [{self.mana}]/[100]'


class Skill:
    maxSkill = 3

    def __init__(self, name, mana_cost, damage_multiplier):
        self.name = name
        self.mana_cost = mana_cost
        self.damage_multiplier = damage_multiplier

    # Duck typing (Skill dan Item sama-sama punya describe())
    def describe(self):
        return f'{self.name} (Mana: {self.mana_cost})'


class Item:
    def __init__(self, name, heal, quantity):
        self.name = name
        self.heal = heal
        self.quantity = quantity

    # Duck typing
    def describe(self):
        return f'{self.name} x {self.quantity} (Heal: {self.heal})'


class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, name, heal, quantity):
        if name in self.items:
            self.items[name].quantity += quantity
        else:
            self.items[name] = Item(name, heal, quantity)  # Komposisi

    def use_items(self, name):
        for key, item in self.items.items():
            if key.lower() == name.lower() and item.quantity > 0:
                item.quantity -= 1
                return key, item.heal
        return

    def isEmpty(self):
        return all(item.quantity <= 0 for item in self.items.values())

    def available(self):
        return [item for item in self.items.values() if item.quantity > 0]


# Duck typing: menerima objek apa pun yang punya describe()
def tampilkan_daftar(judul, daftar):
    print(f'\n{judul}')
    for entri in daftar:
        print(f'- {entri.describe()}')
    print('- back (kembali ke menu)')


class Player(Character):
    def __init__(self, name, health, attack, defence, mana, crit_chance=0.3):
        super().__init__(name, health, attack, defence, mana)
        self.crit = crit_chance

    # Override abstract method
    def Attacking(self, target):
        print(f'{self.name} menyerang {target.name}')
        damage = self.attack

        if random.random() < self.crit:
            damage *= 2
            print('\nCritical Hit!, Damage Digandakan')

        self._mana = min(100, self._mana + 5)
        print(f'{self.name} Memulihkan 5 mana')
        target.takeDamage(damage)

    # Override abstract method
    def battle_cry(self):
        print(f'{self.name}: "Aku tidak akan menyerah!"')


class Enemy(Character):
    def __init__(self, name, health, attack, defence, mana, resistance=0.2):
        super().__init__(name, health, attack, defence, mana)
        self.resistance = resistance

    # Override abstract method
    def Attacking(self, target):
        print(f'{self.name} menyerang {target.name}')
        target.takeDamage(self.attack)

    # Override abstract method
    def battle_cry(self):
        print(f'{self.name}: "Hadapi dinginnya kekalahan!"')

    # Override instance method
    def takeDamage(self, damage):
        reduced = int(damage * (1 - self.resistance))
        print(f'\n{self.name} Menahan {int(self.resistance * 100)}% Damage')
        super().takeDamage(reduced)


class GameMaster:
    gameRunning = False

    # Asosiasi + DIP: karakter hanya lewat parameter, bertipe abstraksi Character
    def battleStart(self, first: Character, second: Character):
        print('\n' + '=' * 40)
        print('Battle Start')
        print(f'{first.name} VS {second.name}')
        print('=' * 40)

        # Polimorfisme via pewarisan: satu loop, objek subclass berbeda
        for character in (first, second):
            character.introduce()

        turn = 1
        while True:
            print(f'\n{"=" * 15} Cycle {turn} {"=" * 15}')

            for current, opponent in ((first, second), (second, first)):
                self._Turn(current, opponent)
                if not opponent.isAlive():
                    print(f'\n{current.name} memenangkan pertarungan')
                    return f'Victory [{current.name}]'

            turn += 1

    def _Turn(self, current_character, opponent):
        print(f'\nGiliran {current_character.name}')
        print(current_character)

        while True:
            print('\nAction')
            print('1. Basic Attack')
            print('2. Skill')
            print('3. Item')

            choice = input(f'{current_character.name}, Pilih Aksi: ')

            if choice == '1':
                current_character.Attacking(opponent)  # Polimorfisme: Player / Enemy
                return

            elif choice == '2':
                if not current_character.skills:
                    print(f'{current_character.name} belum memiliki skill')
                    continue

                tampilkan_daftar('Skill yang tersedia:', current_character.skills)
                skill_name = input('\nKetik nama skill yang ingin digunakan: ')

                if skill_name.lower() == 'back':
                    continue

                if current_character.use_skill(skill_name, opponent):
                    return

            elif choice == '3':
                if current_character.inventory.isEmpty():
                    print(f'{current_character.name} belum memiliki Item')
                    continue

                tampilkan_daftar('Item yang tersedia:', current_character.inventory.available())
                item_name = input('\nKetik nama item yang ingin digunakan: ')

                if item_name.lower() == 'back':
                    continue

                if current_character.use_item(item_name):
                    return

            else:
                print('Input tidak valid, pilih 1, 2 atau 3.')


if __name__ == "__main__":
    # Bukti abstraksi: abstract class tidak bisa diinstansiasi
    print('=== Bukti Abstract Class ===')
    try:
        Character("Test", 100, 10, 5, 50)
    except TypeError as e:
        print(f'Character tidak bisa diinstansiasi: {e}')
    print('=' * 28)

    fireball = Skill("Fireball", 20, 2.5)
    wind_slash = Skill("Wind Slash", 10, 1.5)
    ice_bullet = Skill("Ice Bullet", 15, 1.8)

    Nezha = Player("Nezha", 100, 15, 5, 50)
    Nezha.add_skill(fireball)
    Nezha.add_skill(wind_slash)

    Nezha.inventory.add_item("Potion", 30, 2)

    Mengya = Enemy("MengYa", 100, 12, 4, 40)
    Mengya.add_skill(ice_bullet)

    game = GameMaster()
    result = game.battleStart(Nezha, Mengya)

    print(f"\nHASIL PERTARUNGAN: {result}")
    print(Character.total_character())