from utils import display, bug, getNumber
from Crypto.Util.number import long_to_bytes, getPrime, isPrime
import requests 
from rsa import generate
import math
from sympy import integer_nthroot
def main():
    arr = [
        "Factoring via api of https://factordb.com/",
        "Factoring by fermat",
        "Generate p and q",
        "Exit"
    ]
    while True:
        print("================ Factoring N in RSA ================")
        display(arr)
        print("================ Factoring N in RSA ================")
        choice  = getNumber("Enter your choice: ")
        if choice == 1:
            factor1()
        elif choice == 2:
            fermat_factor()
        elif choice == 3:
            generate()
        elif choice == 4:
            print("================ Good bye! ================")
            exit(1)
        else:
            bug(2)


def factor1():
    # curl -X GET  https://factordb.com/api?query=<number>
    n = getNumber("Enter n (number base): ")
    if n is None:
        bug(3)
        return
    api = f"https://factordb.com/api?query={n}"
    res = requests.get(api)
    data = res.json()
    print(data)
    status = data['status']
    if status == 'FF':
        factors = data['factors']
        phi = phi_from_factorization(factors)
        decrypt(phi,n)
    else:
        print("Can't factor by this! Try another ways.")

def phi_from_factorization(factors):
    phi = 1
    for p_str, e in factors:
        p = int(p_str)
        if e == 1:
            phi *= (p - 1)
        else:
            phi *= (p ** (e - 1)) * (p - 1)
    return phi

def fermat_factor():
    n = getNumber("Enter n (number base): ")
    if n is None:
        bug(3)
        return
    if n % 2 == 0:
        return 2, n//2
    a = math.isqrt(n)
    if a * a < n:
        a += 1

    while True:
        b2 = a * a - n
        b, exact = integer_nthroot(b2,2)
        if exact:
            p, q = a - b, a + b
            assert p * q == n
            print("================ Factoring sucessfully ================")
            print(p,q)
            phi = (p - 1) * (q - 1)
            decrypt(phi,n)
        a += 1

def decrypt(phi,n):
    e = getNumber("Enter e (number base) (default 0x10001): ")
    if e is None:
        e = 65537
    c = getNumber("Enter c (number base): ")
    if c is None:
        bug(3)
        return
    try: 
        d = pow(e,-1, phi)
    except:
        print("Can't calculate d")
        return
    m = pow(c,d,n)
    message = long_to_bytes(m)
    print("Message (byte):",message)
    print("Message (hex):", message.hex())

if __name__ == "__main__":
    main()