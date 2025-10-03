from utils import display, bug, getNumber
from Crypto.Util.number import bytes_to_long, long_to_bytes

def main():
    arr = [
        "Internal Attack (n, d, e)",
        "External Attack (n, e, c)",
        "Exit()"
    ]
    while True:
        print("================ Common n Attack ================")
        display(arr)
        print("================ Common n Attack ================")

        choice = getNumber("Enter your choice: ")
        if choice == 1:
            internal_attack()
        elif choice == 2:
            external_attack()
        elif choice == 3:
            print("==================== Exit ====================")
            exit(0)
        else:
            bug(2)

def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        print('============= Modular inverse does not exist =============')
        return None
    else:
        return x % m

def recover_phi_from_d(e, d, n, max_iter=1000000):
    ed_minus_1 = e * d - 1 
    
    k = ed_minus_1 // n

    iters = 0 
    while k <= ed_minus_1:
        if iters >= max_iter:
            print('============= Max iterations reached =============')
            return None
        if ed_minus_1 % k == 0:
            phi = ed_minus_1 // k
            if phi < n:
                return phi
        k += 1
        iters += 1

    return None
    

def internal_attack():
    n = getNumber("Enter n (number base): ")
    d = getNumber("Enter d (number base): ")
    e = getNumber("Enter e (number base): ")
    if n is None or d is None or e is None:
        bug(3)
        return
    max_iter = getNumber("Enter max iterations (default is 1000000): ")
    if max_iter is None:
        max_iter = 1000000
    print("Recovering phi from n, d, e with max iterations =", max_iter)
    phi = recover_phi_from_d(e, d, n)
    if phi is None:
        print("Failed to recover phi")
        return
    print("Recovered phi:", phi)
    e_victim = getNumber("Enter victim's e (number base) (default is 0x10001): ")
    if e_victim is None:
        e_victim = 0x10001
    d_victim = modinv(e_victim, phi)
    if d_victim is None:
        print("Failed to recover d_victim")
        return
    print("Recovered d_victim:", d_victim)
    c_victim = getNumber("Enter victim's c (number base): ")
    if c_victim is None:
        bug(3)
        return
    m_victim = pow(c_victim, d_victim, n)
    message = long_to_bytes(m_victim)
    print("Recovered m_victim (bytes):", message)
    print("Recovered m_victim (hex):", message.hex())



def external_attack():
    n = getNumber("Enter n (number base): ")
    e = getNumber("Enter e (number base): ")
    e_victim = getNumber("Enter victim's e (number base) (default is 0x10001): ")
    if e_victim is None:
        e_victim = 0x10001
    c = getNumber("Enter c (number base): ")
    c_victim = getNumber("Enter victim's c (number base): ")


    if n is None or e is None or c is None or c_victim is None:
        bug(3)
        return
    m = recover_message(n, e, e_victim, c, c_victim)
    if m is None:
        print("Failed to recover m")
        return
    message = long_to_bytes(m)
    print("Recovered m (byte):", message)
    print("Recovered m (hex):", message.hex())

def recover_message(n, e, e_victim, c, c_victim):
    g, u, v = egcd(e, e_victim)
    if g != 1:
        print("e and e_victim are not coprime, gcd =", g)
        return
    
    def pow_with_signed_exponent(base: int, exp: int, mod: int) -> int:
        if exp >= 0:
            return pow(base, exp, mod)
        # exp < 0: cần nghịch đảo base mod mod rồi lũy thừa abs(exp)
        inv = modinv(base, mod)
        if inv is None:
            raise ValueError("Base không khả nghịch modulo n, không thể xử lý mũ âm.")
        return pow(inv, -exp, mod)
    
    try:
        partA = pow_with_signed_exponent(c, u, n)
        partB = pow_with_signed_exponent(c_victim, v, n)
    except:
        print("Failed to compute modular exponentiation with signed exponent.")
        return None
    m = (partA * partB) % n
    return m

if __name__ == "__main__":
    main()