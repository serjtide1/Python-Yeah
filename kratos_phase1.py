import random

PLAYER_MAX_HEALTH = 100
ENEMY_TYPES = [
    {"name": "Draugr", "health": 40, "attack": (8, 14)},
    {"name": "Hel-Walker", "health": 50, "attack": (10, 16)},
    {"name": "Dark Elf", "health": 60, "attack": (12, 18)},
]

def kratos_say(text):
    print(f"\nKratos: {text}\n")

def create_enemy():
    enemy = random.choice(ENEMY_TYPES)
    return {
        "name": enemy["name"],
        "health": enemy["health"],
        "attack": enemy["attack"]
    }

def combat(player):
    enemy = create_enemy()
    kratos_say(f"A {enemy['name']} stands before you. Prepare yourself.")

    while enemy["health"] > 0 and player["health"] > 0:
        print(f"Your Health: {player['health']} | Rage: {player['rage']}")
        print(f"{enemy['name']} Health: {enemy['health']}")
        print("Choose an action:")
        print("1. Attack")
        print("2. Dodge")
        print("3. Focus Rage")

        choice = input("> ").strip()

        if choice == "1":
            damage = random.randint(12, 20) + player["rage"]
            enemy["health"] -= damage
            kratos_say(f"You strike with force. Damage dealt: {damage}")
            player["rage"] = max(0, player["rage"] - 1)

        elif choice == "2":
            if random.random() < 0.5:
                kratos_say("You evade the attack. The enemy falters.")
                continue
            else:
                kratos_say("You mistime the dodge.")

        elif choice == "3":
            player["rage"] += 2
            kratos_say("You steady your breath. Rage builds.")

        else:
            kratos_say("Indecision will kill you.")
            continue

        if enemy["health"] > 0:
            enemy_damage = random.randint(*enemy["attack"])
            player["health"] -= enemy_damage
            kratos_say(f"The {enemy['name']} strikes you for {enemy_damage}.")

    if player["health"] <= 0:
        kratos_say("You have fallen. Learn from this failure.")
        return False

    kratos_say(f"The {enemy['name']} is dead. Move forward.")
    player["rage"] += 1
    return True

def game():
    player = {
        "health": PLAYER_MAX_HEALTH,
        "rage": 0,
        "room": 1
    }

    kratos_say("Do not expect mercy. Each step forward is earned.")

    while player["health"] > 0:
        kratos_say(f"You enter room {player['room']}.")

        survived = combat(player)
        if not survived:
            break

        player["room"] += 1

        if player["room"] > 5:
            kratos_say("You have survived this trial. For now.")
            break

    kratos_say("The path ends here.")

if __name__ == "__main__":
    game()
