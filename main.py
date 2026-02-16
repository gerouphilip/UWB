from _ast import Continue
import random
from classes.game import Person, bcolors
from classes.magic import*
from classes.inventory import Item
import json
with open("classes/data.json", "r") as f:
    data = json.load(f)



# Create Black Magic and balance spells
fire = Spell("Heater", 10, 700, "black")
thunder = Spell("Blanket", 18, 1100, "black")
blizzard = Spell("Fresh Air", 30, 1600, "black")
meteor = Spell("Help", 85, 2400, "black")
quake = Spell("In the Zone", 175, 3200, "black")


# Create White Magic and balance spells
cure = Spell("Move to the back couch", 12, 800, "white")
cura = Spell("Nap", 25, 1600, "white")
curaga = Spell("Restore", 50, 4800, "white")

# Create some Items
potion = Item("Coffee", "potion", "Heals 600 HP", 600)
hipotion = Item("Monster", "potion", "Heals 1200 HP", 1200)
superpotion = Item("NOS", "potion", "Heals 2000 HP", 2000)

elixer = Item("Chips", "elixer", "Fully restore HP/MP of 1 party member", 9999)
hielixer = Item("VeggieTray", "elixer", "Fully restore HP/MP of all party members", 9999)

grenade = Item("Walkthrough", "attack", "Deals 2200 damage", 2200)


player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, thunder, blizzard, meteor, curaga]

player_items = [{"item": potion, "quantity": 5}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 2}, {"item": elixer, "quantity": 4},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]

# Instantiate People
# player1 = Person("Philip", 6500, 450, 320, 40, player_spells, player_items)
philip_data = data["players"]["Philip"]

player1 = Person(
    "Philip",
    philip_data["base_hp"],
    philip_data["base_mp"],
    philip_data["base_atk"],
    philip_data["base_df"],
    player_spells,
    player_items
)

player1.level = philip_data["level"]
player1.xp = philip_data["xp"]
player1.wins = philip_data.get("wins", 0)
player1.losses = philip_data.get("losses", 0)

#player2 = Person("Mike  ", 6000, 350, 290, 45, player_spells, player_items)
mike_data = data["players"]["Mike"]
player2 = Person(
    "Mike  ",
    mike_data["base_hp"],
    mike_data["base_mp"],
    mike_data["base_atk"],
    mike_data["base_df"],
    player_spells,
    player_items
)

player2.level = mike_data["level"]
player2.xp = mike_data["xp"]
player2.wins = mike_data.get("wins", 0)
player2.losses = mike_data.get("losses", 0)

#player3 = Person("Solon ", 6200, 300, 360, 35, player_spells, player_items)
solon_data = data["players"]["Solon"]
player3 = Person(
    "Solon ",
    solon_data["base_hp"],
    solon_data["base_mp"],
    solon_data["base_atk"],
    solon_data["base_df"],
    player_spells,
    player_items
)

player3.level = solon_data["level"]
player3.xp = solon_data["xp"]
player3.wins = solon_data.get("wins", 0)
player3.losses = solon_data.get("losses", 0)

#player4 = Person("QB    ", 5800, 300, 260, 70, player_spells, player_items)
QB_data = data["players"]["QB"]
player4 = Person(
    "QB    ",
    QB_data["base_hp"],
    QB_data["base_mp"],
    QB_data["base_atk"],
    QB_data["base_df"],
    player_spells,
    player_items
)

player4.level = QB_data["level"]
player4.xp = QB_data["xp"]
player4.wins = QB_data.get("wins", 0)
player4.losses = QB_data.get("losses", 0)

#enemy1 = Person("The Game  ", 18000, 400, 360, 60, enemy_spells, [])
TheGame_data = data["enemies"]["The Game"]
enemy1 = Person(
    "The Game  ",
    TheGame_data["base_hp"],
    TheGame_data["base_mp"],
    TheGame_data["base_atk"],
    TheGame_data["base_df"],
    enemy_spells,
    []
)
enemy1.level = TheGame_data["level"]
enemy1.xp_reward = TheGame_data["xp_reward"]

# Scale enemy stats based on level
enemy1.scale_with_level()
#enemy2 = Person("Sleep Dep.", 14000, 350, 300, 50, enemy_spells, [])
SleepDep_data = data["enemies"]["Sleep Dep."]
enemy2 = Person(
        "Sleep Dep.",
    SleepDep_data["base_hp"],
    SleepDep_data["base_mp"],
    SleepDep_data["base_atk"],
    SleepDep_data["base_df"],
    enemy_spells,
    []
)
enemy2.level = SleepDep_data["level"]
enemy2.xp_reward = SleepDep_data["xp_reward"]

# Scale enemy stats based on level
enemy2.scale_with_level()
#enemy3 = Person("Chat      ", 12000, 450, 270, 75, enemy_spells, [])
Chat_data = data["enemies"]["Chat"]
enemy3 = Person(
    "Chat      ",
    Chat_data["base_hp"],
    Chat_data["base_mp"],
    Chat_data["base_atk"],
    Chat_data["base_df"],
    enemy_spells,
    []
)
enemy3.xp_reward = Chat_data["xp_reward"]
enemy3.level = Chat_data["level"]

# Scale enemy stats based on level
enemy3.scale_with_level()

players = [player1, player2, player3, player4]

enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "A NEW GAME IS CHALLENGED!" + bcolors.ENDC)


def save_game(players, filename="classes/data.json"):
    with open(filename, "r") as f:
        data = json.load(f)

    for player in players:
        data["players"][player.name.strip()] = {
            "level": player.level,
            "xp": player.xp,
            "base_hp": player.base_hp,
            "base_mp": player.base_mp,
            "base_atk": player.base_atk,
            "base_df": player.base_df,
            "wins": getattr(player, "wins", 0),
            "losses": getattr(player, "losses", 0)
        }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


# Call this after the battle
save_game(players)


while running:
    print("===================================================")
    print("\n")

    for player in players:
        if player.get_hp() == 0:
            continue
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        if player.get_hp() == 0:
            continue

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
               # del enemies[enemy]

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
                  #  del enemies[enemy]



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
                    for player in players:
                        player.gain_xp(enemies[enemy].xp_reward)

                        #player.xp += enemies[enemy].xp_reward  # Award XP to all players
                        #player.level_up()    # Check and level up players if needed
                #    del enemies[enemy]
                    if enemies[target].get_hp() == 0:
                        print(enemies[target].name.replace(" ", "") + " has been defeated.")

    #check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1
        if enemy.get_hp() == 0 and not hasattr(enemy, "xp_given"):
            print(enemy.name.replace(" ", "") + " has been defeated.")
            for player in players:
                player.gain_xp(enemy.xp_reward)
            enemy.xp_given = True  # Prevent giving XP multiple times


    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1
    #Check if player won
    if all(enemy.get_hp() == 0 for enemy in enemies):
        print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
        for player in players:
            player.wins += 1
            save_game(players)
        running = False
    #Check if enemy won
    elif defeated_players == 3:
        print(bcolors.FAIL + "You Lose!" + bcolors.ENDC)
        for player in players:
            player.losses += 1
            save_game(players)
        running = False


    #Enemy Stat increase
    enemy2.atkl += 10  # increase by 10 every turn
    enemy2.atkh += 10  # increase by 10 every turn
    enemy2.df += 5
    #Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if len(players) == 0:
            print("\n")
            print(bcolors.FAIL + bcolors.BOLD + "You Lose!" + bcolors.ENDC)
            running = False
            break

        if enemy_choice == 0:
            # Chose attack
            target = random.randrange(0, len(players))

            enemy_dmg = enemies[0].generate_damage()
            players[target].take_damage(enemy_dmg - players[target].df)
            print(enemy.name.replace(" ","") + " attacks " + players[target].name.replace(" ", "") + " for ", enemy_dmg)

            if players[target].get_hp() == 0:
                print(players[target].name.replace(" ", "") + " has fallen asleep.")
                #del players[player]
                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has fallen asleep.")

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
                target = random.randrange(0, len(players))


                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s" + spell.name + " deals", str(magic_dmg), " points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has fallen asleep.")
                    #del players[target]
                    if players[target].get_hp() == 0:
                        print(players[target].name.replace(" ", "") + " has fallen asleep.")

            #print("Enemy chose", spell, "damage is", magic_dmg)

    #players = [p for p in players if p.get_hp() > 0]
    enemies = [e for e in enemies if e.get_hp() > 0]


