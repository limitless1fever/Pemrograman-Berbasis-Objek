class Character:
    totalCharacter = 0

    def __init__(self, name, health, attack, defence, mana):
        self.name = name
        self.__health = health
        self.attack = attack
        self.defence = defence
        self._mana = mana
        self.skills = []
        Character.totalCharacter +=1

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

        print(f'{self.name} terkena damage sebsar {hit}, sisa HP [{self.health}]/[100] ')

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


class Skill:
    maxSkill = 3
    def __init__(self, name, mana_cost, damage_multiplier):
        self.name = name
        self.mana_cost = mana_cost
        self.damage_multiplier = damage_multiplier


class gameMaster:
    gameRunning = False
    def __init__(self, character1, character2):
        self.character1 = character1
        self.character2 = character2
        
    def battleStart(self):
        print('\n' + '=' * 40)
        print('Battle Start')
        print(f'{self.character1.name} VS {self.character2.name}')
        print('=' * 40)
        turn = 1

        while self.character1.isAlive() and self.character2.isAlive():
            print(f'\n{"="*15} Cycle {turn} {"="*15}')

            self._Turn(self.character1, self.character2)
            if not self.character2.isAlive():
                print(f'\n{self.character1.name} memenangkan pertarungan')
                return f'Victory {self.character1.name}'

            self._Turn(self.character2, self.character1)
            if not self.character1.isAlive():
                print(f'\n{self.character2.name} memenangkan pertarungan')
                return f'Victory {self.character2.name}'

            turn += 1

    def _Turn(self, current_character, opponent):
        print(f'\nGiliran {current_character.name}')
        print(f'HP: [{current_character.health}]/[100] | Mana: [{current_character._mana}]/[100]')

        while True:
            print('\nAction')
            print('1. Basic Attack')
            print('2. Skill')

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

            else:
                print('Input tidak valid, pilih 1 atau 2.')


if __name__ == "__main__":
    fireball = Skill("Fireball", 20, 2.5)
    wind_slash = Skill("Wind Slash", 10, 1.5)
    ice_bullet= Skill("Ice Bullet", 15, 1.8)

    character1 = Character("Nezha", 100, 15, 5, 50)
    character1.add_skill(fireball)
    character1.add_skill(wind_slash)

    character2 = Character("MengYa", 100, 12, 4, 40)
    character2.add_skill(ice_bullet)

    # Memulai Game
    game = gameMaster(character1, character2)
    result = game.battleStart()

    print(f"\nHASIL PERTARUNGAN: {result}")
    print(Character.total_character())