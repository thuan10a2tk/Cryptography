'''

'''
from utils import *

def rail_fence_encrypt(message: str, key: int)-> str:
    if key == 1:
        return message
    cipher = ""
    direction_down = False
    rail = [[] for _ in range(key)]
    row = 0
    for ch in message:
        rail[row].append(ch)
        if row == 0 or row == key - 1:
            direction_down = not direction_down
        row += 1 if direction_down else -1
    for r in rail:
        for c in r:
            cipher += c
    return cipher

def rail_fence_decrypt(cipher: str, key: int)-> str:
    if key == 1:
        return cipher
    arr = [0] * key
    direction_down = False
    row = 0
    l = len(cipher)
    for i in range(l):
        arr[row] += 1
        if row == 0 or row == key - 1:
            direction_down = not direction_down
        row += 1 if direction_down else -1
    rail = [] * key
    for i in range(len(arr)):
        rail.append(list(cipher[:arr[i]]))
        cipher = cipher[arr[i]:]

    message = ""
    direction_down=False
    row = 0
    for i in range(l):
        message += rail[row].pop(0)
        if row == 0 or row == key - 1:
            direction_down = not direction_down
        row += 1 if direction_down else -1
    return message

def permutation_encrypt(message: str, key: list, n: int)-> str:
    assert len(key) == n
    assert all( int(k) in range(1, n+1) for k in key)
    matrix = []
    pad = n - len(message) % n
    message += '*' * pad
    for i in range(0, len(message), n):
        matrix.append(message[i:i+n])
    cipher = ""
    for k in key:
        k_idx = int(k) - 1
        for row in matrix:
            cipher += row[k_idx]
    return cipher

def permutation_decrypt(cipher: str, key: list, n: int)-> str:
    assert len(key) == n
    assert all( int(k) in range(1, n+1) for k in key)

    num_rows = len(cipher) // n
    matrix = [ [''] * n for _ in range(num_rows) ]
    for k in key:
        k_idx = int(k) - 1
        for r in range(num_rows):
            matrix[r][k_idx] = cipher[0]
            cipher = cipher[1:]
    message = ""
    for row in matrix:
        message += ''.join(row)
    return message.replace('*', '')
    


def main():
    arr = [
        "Rail Fence Encryption",
        "Rail Fence Decryption",
        "Permutation Encryption",
        "Permutation Decryption",
        "Exit"
    ]
    display_menu(arr, "Transposition Cipher")
    while True:
        choice = getNumber("Enter your choice: ", 10)
        if choice == 1:
            data = getString("Enter your data: ")
            key  = getNumber("Enter your key(number): ", 10)
            if key <= 0:
                print("Key must be a positive integer.")
                continue
            print(rail_fence_encrypt(data, key))
        elif choice == 2:
            data = getString("Enter your data: ")
            key  = getNumber("Enter your key(number): ", 10)
            if key <= 0:
                print("Key must be a positive integer.")
                continue
            print(rail_fence_decrypt(data, key))
        elif choice == 3:
            data = getString("Enter your data: ")
            n = getNumber("Enter the length of key: ", 10)
            key = getString("Enter the key (permutation from 1 to n and separate by space): ").split()
            print(permutation_encrypt(data, key, n))
        elif choice == 4:
            data = getString("Enter your data: ")
            n = getNumber("Enter the length of key: ", 10)
            key = getString("Enter the key (permutation from 1 to n and separate by space): ").split()
            print(permutation_decrypt(data, key, n))
        else:
            exit(0)

if __name__ == "__main__":
    main()