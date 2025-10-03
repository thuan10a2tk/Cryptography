from sympy.ntheory.modular import crt
from sympy import integer_nthroot
from utils import display, bug, getNumber
from Crypto.Util.number import long_to_bytes


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x, y = y1, x1 - (a // b) * y1
    return g, x, y

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        print(f"No modular inverse for {a} mod {m}")
        return None
    return x % m

def chinese_remainder_theorem(remainders, moduli):
    """
    Solve system:
      x ≡ remainders[i] (mod moduli[i])
    """
    if len(remainders) != len(moduli):
        print("remainders and moduli must have same length")
        return None
    
    M = 1
    for m in moduli:
        M *= m  # product of all moduli
    
    x = 0
    for r, m in zip(remainders, moduli):
        Mi = M // m
        inv = mod_inverse(Mi, m)
        x += r * Mi * inv
    
    return x % M

def main():
    arr = [
        "Attack by implement function",
        "Attack by built in function from sympy",
        "Exit()"
    ]
    while True:
        print("======================= Chinese Remainder Theorem =======================")
        display(arr)
        print("======================= Chinese Remainder Theorem =======================")
        choice = getNumber("Enter your choice: ")
        if choice == 1:
            attack1()
        elif choice == 2:
            attack2()
        elif choice == 3:
            exit(0)
        else:
            bug(3)

def attack1():
    remainders = []
    moduli = []
    n = getNumber("Enter number of equations (number base): ")
    for i in range(n):
        r = getNumber(f"Enter remainder (c) for equation {i+1} (number base): ")
        remainders.append(r)
    for i in range(n):
        m = getNumber(f"Enter modulus (n) for equation {i+1} (number base): ")
        moduli.append(m)
    if len(moduli) != len(set(moduli)) or len(moduli) == 0:
        print("====================== Moduli must be pairwise coprime ======================")
        return
    M = chinese_remainder_theorem(remainders, moduli)
    
    if M is None:
        print("==================== Can't use this method ====================")
    else:
        print("Founded =", M)
        extract_message(M)

def attack2():
    remainders = []
    moduli = []
    n = getNumber("Enter number of equations (number base): ")
    for i in range(n):
        r = getNumber(f"Enter remainder (c) for equation {i+1} (number base): ")
        remainders.append(r)
    for i in range(n):
        m = getNumber(f"Enter modulus (n) for equation {i+1} (number base): ")
        moduli.append(m)

    if len(moduli) != len(set(moduli)) or len(moduli) == 0:
        print("==================== Moduli must be pairwise coprime ====================")
        return
    M, mod = crt(moduli, remainders)  
    if M is None:
        print("================== Can't use this method ==================")
    else:
        print("Founded =", M, "and mod =", mod)
        extract_message(M)

def extract_message(M):
    e = getNumber("Enter e (number base) (default is 3): ")
    if e is None:
        e = 3
    m, exact = integer_nthroot(M, e)
    if exact:
        print("================= Perfect root found =================")
        message = long_to_bytes(m)
        print("Message (bytes)", message)
        print("Message (hex)", message.hex())
    else:
        print("============ Try another e, or use another method =============")

if __name__ == "__main__":
    main()
