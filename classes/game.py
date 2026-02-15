import random
from classes.magic import*

class bcolors:
     HEADER = '\033[95m'
     OKBLUE = '\033[94m'
     OKGREEN = '\033[92m'
     WARNING = '\033[93m'
     FAIL = '\033[91m'
     ENDC = '\033[0m'
     BOLD = '\033[1m'
     UNDERLINE = '\033[4m'


#class Person:
#    def __init__(self, name, hp, mp, atk, df, magic, items):
#        self.maxhp = hp
#        self.hp = hp
#        self.maxmp = mp
#        self.mp = mp
#        self.atkl = atk - 10
#        self.atkh = atk + 10
#        self.df = df
#        self.magic = magic
#        self.actions = ["Attack", "Magic", "Items"]
#        self.items = items
#        self.name = name

class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        # Base stats (permanent growth values)
        self.base_hp = hp
        self.base_mp = mp
        self.base_atk = atk
        self.base_df = df

        # Level system
        self.level = 1
        self.xp = 0

        # Current scaled stats
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp

        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df

        self.magic = magic
        self.actions = ["Attack", "Magic", "Items"]
        self.items = items
        self.name = name

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)


    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
        return self.hp

    def get_hp(self):
        return self.hp

    def get_mp(self):
        return self.mp

    def get_max_hp(self):
        return self.maxhp

    def get_max_mp(self):
        return self.maxmp

    def get_actions(self):
        return self.actions

    def reduce_mp(self, cost):
        self.mp -= cost
        if self.mp <= 0:
            self.mp = 0


    def choose_action(self):
        i = 1
        print("\n" + bcolors.BOLD + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + "Choose an Action:" + bcolors.ENDC)
        for item in self.actions:
            print("    " + str(i) + ": " + item)
            i += 1

    def choose_magic(self):
        i = 1
        print(bcolors.OKBLUE + bcolors.BOLD + "Choose a Spell:" + bcolors.ENDC)
        for spell in self.magic:
            print("    " + str(i) + ": " + spell.name, "(cost", str(spell.cost) + ")")
            i += 1

    def heal(self, dmg):
        self.hp += dmg
        if self.hp <= self.maxhp:
            self.hp = self.maxhp

    def choose_items(self):
        i = 1
        print(bcolors.OKGREEN + bcolors.BOLD + "Choose an Item:" + bcolors.ENDC)
        for item in self.items:
            print("    " + str(i) + "." + item["item"].name, ": ",  item["item"].description, " (x" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        alive_enemies = []

        print("\n" + bcolors.BOLD + bcolors.FAIL + "Choose a Target:" + bcolors.ENDC)

        for index, enemy in enumerate(enemies):
            if enemy.get_hp() > 0:
                print("    " + str(len(alive_enemies) + 1) + "." + enemy.name)
                alive_enemies.append(index)

        if not alive_enemies:
            return None

        choice = int(input("Choose target: ")) - 1

        if choice < 0 or choice >= len(alive_enemies):
            return None

        return alive_enemies[choice]


    def get_stats(self):
        hp_bar = ""
        bar_ticks = (self.hp / self.maxhp) * 100 / 4
        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        mp_bar = ""
        bar_ticks = (self.mp / self.maxmp) * 100 / 10

        while bar_ticks > 0:
            mp_bar += "█"
            bar_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += " "


        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 9:
            decrease = 9 - len(hp_string)

            while decrease > 0:
                current_hp += " "
                decrease -= 1

            current_hp += hp_string

        else:
            current_hp = hp_string

        mp_string = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""

        if len(mp_string) < 7:
            decrease = 7 - len(mp_string)

            while decrease > 0:
                current_mp += " "
                decrease -= 1

            current_mp += mp_string

        else:
            current_mp = mp_string


        print("                         _________________________             __________")
        print(bcolors.BOLD + self.name + ":      " +  current_hp + "  |" + bcolors.OKGREEN + hp_bar + bcolors.ENDC + "|  "  +
              bcolors.BOLD + current_mp +  "  |" + bcolors.OKBLUE + mp_bar + bcolors.ENDC +"|")

    def get_enemy_stats(self):
        hp_bar = ""
        bar_ticks = (self.hp / self.maxhp) * 100 / 2
        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 11:
            decrease = 11 - len(hp_string)

            while decrease > 0:
                current_hp += " "
                decrease -= 1

            current_hp += hp_string

        else:
            current_hp = hp_string

        print("                             __________________________________________________")
        print(
            bcolors.BOLD + self.name + ":    " + current_hp + "  |" + bcolors.FAIL + hp_bar + bcolors.ENDC + "|  ")


    def choose_enemy_spell(self):
        available_spells = []

        pct = self.hp / self.maxhp * 100

        for spell in self.magic:
            if self.mp < spell.cost:
                continue

            if spell.type == "white" and pct > 50:
                continue

            available_spells.append(spell)

        if len(available_spells) == 0:
            return None, None

        spell = random.choice(available_spells)
        magic_dmg = spell.generate_damage()

        return spell, magic_dmg

    def gain_xp(self, amount):
        print(self.name + " gained", amount, "XP!")
        self.xp += amount

        xp_to_level = self.level * 1000

        if self.xp >= xp_to_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp = 0

        print(self.name + " leveled up to Level", self.level, "!")

        self.base_hp += 500
        self.base_mp += 50
        self.base_atk += 40
        self.base_df += 10

        self.scale_with_level()

    def scale_with_level(self):
        multiplier = 1 + (self.level * 0.2)

        self.maxhp = int(self.base_hp * multiplier)
        self.maxmp = int(self.base_mp * multiplier)

        scaled_atk = int(self.base_atk * multiplier)
        self.atkl = scaled_atk - 10
        self.atkh = scaled_atk + 10

        self.df = int(self.base_df * multiplier)

        self.hp = self.maxhp
        self.mp = self.maxmp
