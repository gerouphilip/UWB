from _ast import Continue
import random
from classes.game import Person, bcolors
from classes.magic import*
from classes.inventory import Item



# Create Black Magic and balance spells
fire = Spell("Heater", 7, 500, "black")
thunder = Spell("Blanket", 10, 800, "black")
blizzard = Spell("Fresh Air", 18, 1800, "black")
meteor = Spell("Help", 50, 3400, "black")
quake = Spell("In the Zone", 125, 5000, "black")

# Create White Magic and balance spells
cure = Spell("Move to the back couch", 10, 750, "white")
cura = Spell("Nap", 18, 2000, "white")
curaga = Spell("Restore", 36, 7000, "white")

# Create some Items
potion = Item("Coffee", "potion", "Heals 350 HP", 350)
hipotion = Item("Monster", "potion", "Heals 1000 HP", 1000)
superpotion = Item("NOS", "potion", "Heals 2000 HP", 2000)
elixer = Item("Chips", "elixer", "Fully restore HP/MP of 1 party member", 9999)
hielixer = Item("VeggieTray", "elixer", "Fully restore HP/MP of all party members", 9999)
grenade = Item("Walkthrough", "attack", "Deals 3500 damage", 3500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, thunder, blizzard, meteor, curaga]

player_items = [{"item": potion, "quantity": 5}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 2}, {"item": elixer, "quantity": 4},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]

# Instantiate People
player1 = Person("Philip", 7460, 465, 325, 34, player_spells, player_items)
player2 = Person("Mike  ", 6460, 365, 285, 44, player_spells, player_items)
player3 = Person("Solon ", 7460, 265, 415, 24, player_spells, player_items)
player4 = Person("QB    ", 6960, 165, 275, 64, player_spells, player_items)

enemy1 = Person("The Game  ", 19200, 650, 400, 85, enemy_spells, [])
enemy2 = Person("Sleep Dep.", 11200, 650, 340, 75, enemy_spells, [])
enemy3 = Person("Chat      ", 13200, 650, 240, 54, enemy_spells, [])

players = [player1, player2, player3, player4]

enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "A NEW GAME IS CHALLENGED!" + bcolors.ENDC)

while running:
    print("===================================================")
    print("\n")

    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("Choose an action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg - enemies[enemy].df)
            print(player.name.replace(" ", "") + " attacked " + enemies[enemy].name.replace(" ", "") +" for ", dmg, " points of damage")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has been defeated.")
                del enemies[enemy]

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

                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), " points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has been defeated.")
                    del enemies[enemy]


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
            if player.items[item_choice]["quantity"]== 0:
                del player.items[item_choice]

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) + " HP" + bcolors.ENDC)

            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                    else:
                        player.hp = player.maxhp
                        player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " Fully restore HP/MP" + bcolors.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) + " damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has been defeated.")
                    del enemies[enemy]

    #check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1
    #Check if player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
        running = False
    #Check if enemy won
    elif defeated_players == 3:
        print(bcolors.FAIL + "You Lose!" + bcolors.ENDC)
        running = False


    #Enemy Stat increase
    enemy2.atkl += 10  # increase by 1 every turn
    enemy2.atkh += 10  # increase by 1 every turn
    enemy2.df += 5
    #Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # Chose attack
            target = random.randrange(0, 4)
            enemy_dmg = enemies[0].generate_damage()
            players[target].take_damage(enemy_dmg - players[target].df)
            print(enemy.name.replace(" ","") + " attacks " + players[target].name.replace(" ", "") + " for ", enemy_dmg)

            if players[target].get_hp() == 0:
                print(players[target].name.replace(" ", "") + " has fallen asleep.")
                del players[player]

        if enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()

            if spell is None:
                continue  # enemy skips magic turn

            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                if enemy.hp > enemy.maxhp:
                    enemy.hp = enemy.maxhp
                print(bcolors.OKBLUE + "\n" + spell.name + " heals " + enemy.name.replace(" ", "") + " for", str(magic_dmg), "HP" + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, 4)

                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s" + spell.name + " deals", str(magic_dmg), " points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has fallen asleep.")
                    del players[target]

            #print("Enemy chose", spell, "damage is", magic_dmg)



