from _ast import Continue

from classes.game import Person, bcolors
from classes.magic import*
from classes.inventory import Item



# Create Black Magic and balance spells
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 10, 100, "black")
quake = Spell("Quake", 10, 100, "black")

# Create White Magic and balance spells
cure = Spell("Cure", 10, 100, "white")
cura = Spell("Cura", 18, 200, "white")

# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Superpotion", "potion", "Heals 200 HP", 200)
elixer = Item("Elixer", "elixer", "Fully restore HP/MP of 1 party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restore HP/MP of all party members", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure]
player_items = [{"item": potion, "quantity": 5}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 2}, {"item": elixer, "quantity": 4},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]

# Instantiate People
player1 = Person("Philip", 460, 65, 60, 34, player_spells, player_items)
player2 = Person("Mike  ", 460, 65, 60, 34, player_spells, player_items)
player3 = Person("Solon ", 460, 65, 60, 34, player_spells, player_items)
player4 = Person("QB    ", 460, 65, 60, 34, player_spells, player_items)

enemy = Person("The Game", 1200, 65, 40, 25, [], [])

players = [player1, player2, player3, player4]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "A NEW GAME IS CHALLENGED!" + bcolors.ENDC)

while running:
    print("===================================================")
    print("\n\n")

    for player in players:
        player.get_stats()

    print("\n")

    for player in players:

        player.choose_action()
        choice = input("Choose an action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            print(player.name + " attacked for ", dmg, " points of damage. Enemy HP: ", enemy.get_hp())

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose a spell:")) -1
            if magic_choice == -1:
                Continue

            spell = player.magic[magic_choice]
            magic_dmg = player.magic[magic_choice].generate_damage()


            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP!\n" + bcolors.ENDC)
                Continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                if player.hp > player.maxhp:
                    player.hp = player.maxhp
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP" + bcolors.ENDC)
            elif spell.type == "black":
                enemy.take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), " points of damage" + bcolors.ENDC)

        elif index == 2:
            player.choose_items()
            item_choice = int(input("Choose an item: ")) - 1

            if item_choice == -1:
                Continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + item.name + " is gone" + bcolors.ENDC)
                Continue

            player.items[item_choice]["quantity"] -= 1



            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) + " HP" + bcolors.ENDC)

            elif item.type == "elixer":
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " Fully restore HP/MP" + bcolors.ENDC)

            elif item.type == "attack":
                enemy.take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) + " damage" + bcolors.ENDC)

    enemy_choice = 1

    enemy_dmg = enemy.generate_damage()
    player1.take_damage(enemy_dmg)
    print("Enemy attacks for ", enemy_dmg)

    print("----------------------------------")
    print("Enemy HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC+ "\n")




    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "You Lose!" + bcolors.ENDC)
        running = False
