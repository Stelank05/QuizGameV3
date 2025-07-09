import math
import os
import random

from classes.player import Player

from controls.file_handler import *
from controls.sort_functions import *

from common_data import CommonData

letters: list[str] = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

consonants: list[str] = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]
vowels: list[str] = ["a", "e", "i", "o", "u"]
symbols: list[str] = ["_", "!", "#", "£", "$", "&"]

def valid_int(test: str) -> bool:
    try:
        x = int(test)
        return True
    except ValueError:
        return False

def generate_user_id() -> str:
    if len(CommonData.players) == 0: return "U0001"

    return f"U{str(int(CommonData.players[-1].user_id.replace("U", "")) + 1).rjust(4, "0")}"

def generate_guest_id() -> str:
    if len(CommonData.guests) == 0: return "G0001"

    return f"G{str(int(CommonData.guests[-1].user_id.replace("G", "")) + 1).rjust(4, "0")}"

def unique_username(username: str, account_username: str | None) -> bool:
    name_sort_users(CommonData.players)

    user: Player = username_found(username, 0, len(CommonData.players))

    if user:
        if user.username == account_username: return True
        return False
    return True

def username_found(username: str, start_index: int, end_index: int) -> Player:
    if start_index > end_index: return None
    
    mid_point: int = math.floor((start_index + end_index) / 2)

    if mid_point >= len(CommonData.players): return None

    if CommonData.players[mid_point].username == username:
        return CommonData.players[mid_point]
    elif CommonData.players[mid_point].username > username:
        return username_found(username, start_index, mid_point - 1)
    elif CommonData.players[mid_point].username < username:
        return username_found(username, mid_point + 1, end_index)
    else:
        return None

def valid_password(password: str) -> bool:
    if len(password) < CommonData.min_password_length:
        return False
    
    for character in password:
        if not valid_int(character) and not character.isalpha() and character not in symbols:
            return False
    
    return True

def generate_shift_key() -> str:
    c_shift: int = random.randint(1, 21) - 1
    v_shift: int = (random.randint(1, 5) - 1) + (5 * (random.randint(1, 5) - 1))
    s_shift: int = (random.randint(1, 6) - 1) + (6 * (random.randint(1, 4) - 1))
    n_shift: int = (random.randint(1, 10) - 1) + (10 * (random.randint(1, 2) - 1))

    return (letters[c_shift] + letters[v_shift] + letters[s_shift] + letters[n_shift])

def split_shift_key(shift_key: str) -> list[int]:
    shifts: list[int] = []

    for key in shift_key:
        shifts.append(letters.index(key))

    for i in range(len(shifts)):
        shifts[i] += 1

    shifts[1] = shifts[1] % 5
    shifts[2] = shifts[2] % 6
    shifts[3] = shifts[3] % 10

    return shifts

def encrypt_password(original: str) -> tuple[str, str]:
    shift_key: str = generate_shift_key()
    shifts: list[int] = split_shift_key(shift_key)

    character_type: str
    add: str

    password: str = ""

    for letter in original:
        character_type = get_character_type(letter)

        if character_type == "n":
            password += str((int(letter) + shifts[3]) % 10)
        elif character_type == "v":
            add = vowels[(vowels.index(letter.lower()) + shifts[1]) % 5]
            if letter.isupper(): add = add.upper()
            password += add
        elif character_type == "c":
            add = consonants[(consonants.index(letter.lower()) + shifts[0]) % 21]
            if letter.isupper(): add = add.upper()
            password += add
        elif character_type == "s":
            password += symbols[(symbols.index(letter) + shifts[2]) % 6]

    return [password, shift_key]

def decrypyt_password(encrypted: str, shift_key: str) -> str:
    shifts: list[int] = split_shift_key(shift_key)

    character_type: str
    shift: int
    add: str
    
    password: str = ""

    for letter in encrypted:
        character_type = get_character_type(letter)

        if character_type == "n":
            shift = int(letter) - shifts[3]
            if shift < 0: shift += 10
            password += str(shift)
        elif character_type == "v":
            shift = vowels.index(letter.lower()) - shifts[1]
            if shift < 0: shift += 5
            add = vowels[shift]
            if letter.isupper(): add = add.upper()
            password += add
        elif character_type == "c":
            shift = consonants.index(letter.lower()) - shifts[0]
            if shift < 0: shift += 21
            add = consonants[shift]
            if letter.isupper(): add = add.upper()
            password += add
        elif character_type == "s":
            shift = symbols.index(letter.lower()) - shifts[2]
            if shift < 0: shift += 6
            add = symbols[shift]
            password += add

    return password

def get_character_type(character: str) -> str:
    if valid_int(character):
        return "n"

    if not character.isalpha():
        return "s"

    if character.lower() in vowels:
        return "v"

    return "c"

def login(entered_username: str, entered_password: str) -> None:
    for user in CommonData.players:
        if correct_details(user, entered_username, entered_password):
            return True
    
    return False

def correct_details(user: Player, username: str, password: str) -> bool:
    if username != user.username:
        return False
    
    if password == decrypyt_password(user.password, user.password_shift):
        return True
    
    return False

def write_user_file(new_user: Player) -> None:
    user_path: str = os.path.join(CommonData.player_folder, f"{new_user.user_id}.json")
    write_json_file(user_path, new_user.make_dictionary())

def write_guest_file(new_guest: Player) -> None:
    guest_path: str = os.path.join(CommonData.player_folder, f"{new_guest.user_id}.json")
    write_json_file(guest_path, new_guest.make_dictionary())

"""
password = "coloursyay"
print(valid_password(password))
details = encrypt_password(password)
print(details)
print(decrypyt_password(details[0], details[1]))
#"""