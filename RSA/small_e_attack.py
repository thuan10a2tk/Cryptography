from Crypto.Util.number import long_to_bytes
from utils import getNumber, bug, display
from sympy import integer_nthroot
def main():
    arr = [
        "Attack",
        "Exit()",
    ]
    while True:
        print("================= Small e attack =================")
        display(arr)
        print("================= Small e attack =================")
        choice = getNumber("Enter your choice: ")
        if choice == 1:
            attack()
        elif choice == 2:
            print("==================== Exit ====================")
            exit(0)
        else:
            bug(2)
    
def attack():
    n = getNumber("Enter n (number base): ")
    if n is None:
        bug(3)
        return
    e = getNumber("Enter e (number base) (default is 3): ")
    if e is None:
        e = 3
    c = getNumber("Enter c (number base): ")
    if c is None:
        bug(3)
        return
    times = getNumber("Enter times (number base) (default is 10000): ")
    if times is None:
        times = 10000
    for i in range(times):
        m_pow_e = n * i + c
        m, exact = integer_nthroot(m_pow_e, e)
        if exact:
            message = long_to_bytes(m)
            print("Attack succesfully with", i + 1, "times")
            print("Message (bytes)", message)
            print("Message (hex)", message.hex())
            return
    print("Try larger times or try another ways")
    
if __name__ == "__main__":
    main()