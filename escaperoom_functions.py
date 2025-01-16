
# Escape room game functions

# Define the escape room map with unified 'objects' for doors and furniture
escape_room_map = {
    'Game Room': {
        'description': 'An eerie room with a Piano, Couch and a Locked Door with a ghost on it.',
        'objects': {
            'Ghost Door': {'type': 'door', 'leads_to': 'Master Bedroom', 'locked': True},
            'piano': {'type': 'furniture', 'item': 'Ghost Key', 'unlocks': 'Ghost Door'},
            'couch': {'type': 'furniture', 'item': 'empty'}
        }
    },
    'Master Bedroom': {
        'description': 'A dark and dusty master bedroom with various doors.',
        'objects': {
            'Spider Door': {'type': 'door', 'leads_to': 'Kids Room', 'locked': True},
            'Skull Door': {'type': 'door', 'leads_to': 'Living Room', 'locked': True},
            'Ghost Door': {'type': 'door', 'leads_to': 'Game Room', 'locked': False},
            'Queen Bed': {'type': 'furniture', 'item': 'Spider Key', 'unlocks': 'Spider Door'}
        }
    },
    'Kids Room': {
        'description': 'A small creepy bedroom with only one door.',
        'objects': {
            'Spider Door': {'type': 'door', 'leads_to': 'Master Bedroom', 'locked': False},
            'Double Bed': {'type': 'furniture', 'item': 'Skull Key', 'unlocks': 'Skull Door'},
            'Dresser': {'type': 'furniture', 'item': 'Pumpkin Key', 'unlocks': 'Pumpkin Door'}
        }
    },
    'Living Room': {
        'description': 'A spooky living room with a dining table and a door with a pumpkin on it.',
        'objects': {
            'Dining Table': {'type': 'furniture', 'item': 'empty'},
            'Skull Door': {'type': 'door', 'leads_to': 'Living Room', 'locked': False},
            'Pumpkin Door': {'type': 'door', 'leads_to': 'Finish', 'locked': True}
        }
    },
    'Finish': {
        'description': 'You have made it to the final room. Congratulations!',
        'objects': {}
    }
}

# Wallet to store items like keys
wallet = []

# Variable to track if the game has ended
game_terminated = False


def game_start():
    """Starts the game and provides player introduction"""
    print("You wake up on an unfamiliar couch in an eerie room without windows.")
    print("You feel uneasy. You need to escape from this place!\n")

    explore = input("Do you want to explore the room you're in? (y/n): ").lower()

    if explore == 'y':
        explore_room('Game Room')
    elif explore == 'n':
        print("You chose not to explore. You remain trapped forever.")
        print("Game over. You failed to escape.\n\n")
        game_start()  # Restart the game
    else:
        print("Invalid choice. Please type 'y' or 'n'.")
        game_start()


def game_end():
    """Ends the game when the player reaches the final room"""
    global game_terminated
    print("\nCongratulations! You have escaped the room. The game is over.")
    game_terminated = True
    return


def explore_room(current_room):
    """Handles room exploration with objects"""
    global game_terminated

    if game_terminated:
        return

    room_data = escape_room_map[current_room]
    print("\n" + room_data['description'])

    if current_room == 'Finish':
        game_end()
        return

    print(f"You can explore the following objects in {current_room}:")

    for item in room_data['objects']:
        print(item.capitalize())

    choice = input("\nWhat would you like to examine?: ").lower()

    valid_objects = {obj.lower(): obj for obj in room_data['objects']}

    if choice in valid_objects:
        examine_object(current_room, valid_objects[choice])
    else:
        print("\nInvalid choice. Please type a valid object.")
        explore_room(current_room)


def examine_object(current_room, object_choice):
    """Handles room interaction with objects and gives hints"""
    global game_terminated

    if game_terminated:
        return

    room_data = escape_room_map[current_room]
    object_data = room_data['objects'][object_choice]

    if object_data['type'] == 'furniture':
        if object_data['item'] == 'empty':
            print("\nYou examine the " + object_choice + ". It's just an ordinary piece of furniture. Nothing useful here.")
        else:
            print(f"\nYou examine the {object_choice} and find a {object_data['item']} hidden under it.")
            wallet.append(object_data['item'])
            print(f"The {object_data['item']} has been added to your wallet.")

    elif object_data['type'] == 'door':
        try_open_door(current_room, object_choice)

    if current_room != 'Finish':
        explore_room(current_room)


def try_open_door(current_room, door_choice):
    global game_terminated

    if game_terminated:
        return

    room_data = escape_room_map[current_room]
    door_data = room_data['objects'][door_choice]

    if door_data['locked']:
        required_key_name = next(
            (obj['item'] for room in escape_room_map.values() for obj in room['objects'].values()
             if obj.get('unlocks') == door_choice),
            None
        )

        if required_key_name is None:
            print(f"There is no known key for this door: {door_choice}. You will need to find another way to open it.")
            return

        if required_key_name in wallet:
            print(f"\nThe {required_key_name} is in your wallet. Do you want to use it to unlock the {door_choice}? (y/n)")

            choice = input().lower()
            if choice == 'y':
                print(f"\nYou use the {required_key_name} to unlock {door_choice}.")
                door_data['locked'] = False
                if door_choice.lower() == 'pumpkin door':
                    print("\nYou unlock the Pumpkin Door and step into the final room!")
                    game_end()
                    return
                else:
                    print(f"\nThe {door_choice} is now unlocked. You step into {door_data['leads_to']}.")
                    explore_room(door_data['leads_to'])
            else:
                print(f"\nYou chose not to unlock the {door_choice} for now.")
        else:
            print(f"\nThe {door_choice} is locked. You need the {required_key_name} to open it.")
            return

    else:
        print(f"\nThe {door_choice} is already unlocked.")
        if current_room != 'Finish':
            explore_room(door_data['leads_to'])
