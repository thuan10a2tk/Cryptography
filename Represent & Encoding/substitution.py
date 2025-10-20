'''
    
'''
from utils import *
import random

alphabet = "abcdefghijklmnopqrstuvwxyz"
al_dic = {c:i for i,c in enumerate(alphabet)}
def caesar_encrypt(message: str, key: int)-> str:
    cipher = ""
    key = key % 26
    for m in message:
        if m.islower():
            idx = al_dic[m]
            cipher += alphabet[(idx + key) % 26]
        elif m.isupper():
            idx = al_dic[m.lower()]
            cipher += (alphabet[(idx + key) % 26]).upper()
        else:
            cipher += m
    return cipher
    
def caesar_decrypt(cipher: str, key: int)-> str:
    key = key % 26
    message = ""
    for c in cipher:
        if c.islower():
            idx = al_dic[c]
            message += alphabet[(idx - key)  % 26]
        elif c.isupper():
            idx = al_dic[c.lower()]
            message += (alphabet[(idx - key)  % 26]).upper()
        else:
            message += c
    return message

def vigenere_encrypt(message: str, key: str)-> str:
    assert all(k in alphabet for k in key)
    cipher = ""
    l = len(key)
    key = key.upper()
    offset = 65
    for i,m in enumerate(message):
        if m.islower():
            c = ((ord(m.upper()) - offset) + (ord(key[i%l]) - offset)) % 26 + offset
            cipher += (chr(c)).lower()
        elif m.isupper():
            c = ((ord(m) - offset) + (ord(key[i%l]) - offset)) % 26 + offset
            cipher += chr(c)
        else:
            cipher += m
    return cipher

def vingenere_decrypt(cipher: str, key: str)-> str:
    assert all(k in alphabet for k in key)
    message = ""
    l = len(key)
    key = key.upper()
    offset = 65
    for i, c in enumerate(cipher):
        if c.islower():
            m = ((ord(c.upper()) - offset) - (ord(key[i%l]) - offset)) % 26 + offset
            message += (chr(m)).lower()
        elif c.isupper():
            m = ((ord(c) - offset) - (ord(key[i%l]) - offset)) % 26 + offset
            message += chr(m)
        else:
            message += c
    return message

def monoalphabet_encrypt(message: str, key:str)->str:
    if len(set(list(key))) != 26:
        key =''.join(random.sample(alphabet, len(alphabet)))
        print(f"New key: {key}")
    dic = {m:c for m,c in zip(alphabet, key)}
    cipher = ""
    for m in message:
        if m in dic:
            cipher += dic[m]
        else:
            cipher += m
    return cipher
def monoalohabet_decrypt(cipher: str, key: str)->str:
    assert len(set(list(key))) == 26
    dic = {c:m for m,c in zip(alphabet, key)}
    message = ""
    for c in cipher:
        if c in dic:
            message += dic[c]
        else:
            message += c
    return message

def main():
    arr = [
        "Caesar encryption",
        "Caesar decryption",
        "Vigenere encryption",
        "Vigenere decryption",
        "Monoalphabet encryption",
        "Monoalphabet decryption",
        "Exit"
    ]
    display_menu(arr, "Substitution Cipher")
    while(True):
        choice = getNumber("Enter your choice: ", 10)
        if choice == 1:
            data = getString("Enter your data: ")
            key = getNumber("Enter your key: ", 10)
            print(caesar_encrypt(data,key))
        elif choice == 2:
            data = getString("Enter your data: ")
            key = getNumber("Enter your key: ", 10)
            print(caesar_decrypt(data,key))
        elif choice == 3:
            data = getString("Enter your data: ")
            key = getString("Enter your key: ")
            print(vigenere_encrypt(data,key))
        elif choice == 4:
            data = getString("Enter your data: ")
            key = getString("Enter your key: ")
            print(vingenere_decrypt(data,key))
        elif choice == 5:
            data = getString("Enter your data: ")
            key = getString("Enter your key: ")
            print(monoalphabet_encrypt(data, key))
        elif choice == 6:
            data = getString("Enter your data: ")
            key = getString("Enter your key: ")
            print(monoalohabet_decrypt(data, key))
        else:
            exit(0)

if __name__ == '__main__':
    main()