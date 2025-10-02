from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime
from utils import display, bug, getNumber
def main():
    arr = [
        "Encrypt (n,e,m)",
        "Decrypt (p,q,e,c)",
        "Generate p and q",
        "Exit()"
    ]
    while True:
        print("================= RSA Cipher =================")
        display(arr)
        print("================= RSA Cipher =================")

        choice = getNumber("Enter your choice: ")
        if choice == 1:
            encrypt()
        elif choice == 2:
            decrypt()
        elif choice == 3:
            generate()
        elif choice == 4:
            print("==================== Exit ====================")
            exit(0)
        else:
            bug(2)


def encrypt():
    n = getNumber("Enter n (number base): ")
    if n is None:
        bug(3)
        return
    e = getNumber("Enter e (number base) (default is 0x10001): ")
    if e is None:
        e = 0x10001
    message = input("Enter your message: ")
    m = bytes_to_long(message.encode())
    c = pow(m,e,n)
    print("Cipher (dec):", c)
    print("Cipher (hex):", hex(c))
    # print("Cipher (bin):", bin(c))

def decrypt():
    p = getNumber("Enter p (number base): ")
    q = getNumber("Enter q (number base): ")
    if q is None or p is None:
        bug(3)
        return
    e = getNumber("Enter e (number base) (default is 0x10001): ")
    if e is None:
        e = 0x10001
    c = getNumber("Enter c (number base): ")
    if c is None:
        bug(3)
        return
    n = p * q
    phi = (p-1) * (q-1)
    try: 
        d = pow(e,-1,phi) 
        m = pow(c,d,n)
        message = long_to_bytes(m)
        print("Message (byte):", message)
        print("Message (hex)", message.hex())
    except:
        print("Can't calculate d")
    pass


def generate():
    bit = getNumber("Enter number of bit for q (number base): ")
    q = getPrime(bit)
    bit = getNumber("Enter number of bit for p (number base): ")
    p = getPrime(bit)
    print("N =", p * q)
    print("q =", q)
    print("p =", p)

if __name__ == "__main__":
    main()