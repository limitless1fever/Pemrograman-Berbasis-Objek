# Nama : Pirlo Syabila Hafuza
# NIM : 250916008
# Kelas : Informatika A1'25


import random

class Character:
    totalCharacter = 0

    def __init__(self, name, health, attack, defence, mana):
        self.name = name
        self.__health = health
        self.attack = attack
        self.defence = defence
        self._mana = mana
        self.skills = []
        self.inventory = Inventory()
        Character.totalCharacter +=1

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

    def Attacking(self, target):
        print(f'{self.name} menyerang {target.name}')
        target.takeDamage(self.attack)

    def add_skill(self, skill: 'Skill'):
        if len(self.skills) >= Skill.maxSkill:
            print(f"{self.name} sudah mencapai batas maksimal skill ({Skill.maxSkill})")
            return
        self.skills.append(skill)
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


class Skill:
    maxSkill = 3
    def __init__(self, name, mana_cost, damage_multiplier):
        self.name = name
        self.mana_cost = mana_cost
        self.damage_multiplier = damage_multiplier

class Inventory():
    def __init__(self):
        self.items = {}

    def add_item(self, name, heal, quantity):
        if name in self.items:
            self.items[name]['quantity'] += quantity
        else:
            self.items[name] = {'heal' : heal, 'quantity' : quantity}

    def use_items(self, name):
        for key, data in self.items.items():
            if key.lower() == name.lower() and data['quantity'] > 0:
                data['quantity'] -= 1
                return key, data['heal']
        return

    def isEmpty(self):
        return all(data['quantity'] <= 0 for data in self.items.values())

    def show_items(self):
        for name, data in  self.items.items():
            if data['quantity'] > 0:
                print(f"{name} x {data['quantity']} (Heal: {data['heal']})")

class Player(Character):
    def __init__(self, name, health, attack, defence, mana, crit_chance=0.3):
        super().__init__(name, health, attack, defence, mana)
        self.crit = crit_chance

    def Attacking(self, target):
        print(f'{self.name} menyerang {target.name}')
        damage = self.attack

        if random.random() < self.crit:
            damage *=2
            print('\nCritical Hit!, Damage Digandakan')

        self._mana = min(100, self._mana + 5)
        print(f'{self.name} Memulihkan 5 mana')
        target.takeDamage(damage)

class Enemy(Character):
    def __init__(self, name, health, attack, defence, mana, resistance=0.2):
        super().__init__(name, health, attack, defence, mana)
        self.resistance = resistance

    def takeDamage(self, damage):
        reduced = int(damage * (1 - self.resistance))
        print(f'\n{self.name} Menahan {int(self.resistance * 100)}% Damage')
        super().takeDamage(reduced)

class GameMaster:
    gameRunning = False
    def __init__(self, Player, Enemy):
        self.Player = Player
        self.Enemy = Enemy
        
    def battleStart(self):
        print('\n' + '=' * 40)
        print('Battle Start')
        print(f'{self.Player.name} VS {self.Enemy.name}')
        print('=' * 40)
        turn = 1

        while self.Player.isAlive() and self.Enemy.isAlive():
            print(f'\n{"="*15} Cycle {turn} {"="*15}')

            self._Turn(self.Player, self.Enemy)
            if not self.Enemy.isAlive():
                print(f'\n{self.Player.name} memenangkan pertarungan')
                return f'Victory [{self.Player.name}]'

            self._Turn(self.Enemy, self.Player)
            if not self.Player.isAlive():
                print(f'\n{self.Enemy.name} memenangkan pertarungan')
                return f'Victory [{self.Enemy.name}]'

            turn += 1

    def _Turn(self, current_character, opponent):
        print(f'\nGiliran {current_character.name}')
        print(f'HP: [{current_character.health}]/[100] | Mana: [{current_character.mana}]/[100]')

        while True:
            print('\nAction')
            print('1. Basic Attack')
            print('2. Skill')
            print('3. Item')

            choice = input(f'{current_character.name}, Pilih Aksi: ')

            if choice == '1':
                current_character.Attacking(opponent)
                return

            elif choice == '2':
                if not current_character.skills:
                    print(f'{current_character.name} belum memiliki skill')
                    continue

                print('\nSkill yang tersedia:')
                for skill in current_character.skills:
                    print(f'- {skill.name} (Mana: {skill.mana_cost})')
                print('- back (kembali ke menu)')

                skill_name = input('\nKetik nama skill yang ingin digunakan: ')

                if skill_name.lower() == 'back':
                    continue

                if current_character.use_skill(skill_name, opponent):
                    return

            elif choice == '3':
                if current_character.inventory.isEmpty():
                    print(f'{current_character.name} belum memiliki Item')
                    continue

                print('\nItem yang tersedia:')
                current_character.inventory.show_items()
                print('- back (kembali ke menu)')

                item_name = input('\nKetik nama item yang ingin digunakan: ')

                if item_name.lower() == 'back':
                    continue

                if current_character.use_item(item_name):
                    return

            else:
                print('Input tidak valid, pilih 1, 2 atau 3.')


if __name__ == "__main__":
    fireball = Skill("Fireball", 20, 2.5)
    wind_slash = Skill("Wind Slash", 10, 1.5)
    ice_bullet= Skill("Ice Bullet", 15, 1.8)

    Nezha = Player("Nezha", 100, 15, 5, 50)
    Nezha.add_skill(fireball)
    Nezha.add_skill(wind_slash)

    Nezha.inventory.add_item("Potion", 30, 2)

    Mengya = Enemy("MengYa", 100, 12, 4, 40)
    Mengya.add_skill(ice_bullet)

    # Memulai Game
    game = GameMaster(Nezha, Mengya)
    result = game.battleStart()

    print(f"\nHASIL PERTARUNGAN: {result}")
    print(Character.total_character())