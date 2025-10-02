
def bug(number):
    print("=================== Error ====================")
    if number == 1:
        print("Must be enter number(dec, hex, bin) and base(10, 16, 2)")
    elif number == 2:
        print("Must be choice in range.")
    elif number == 3:
        print("Can't be black it!")
    print("=================== Error ====================")


def display(arr):
    for i in range(len(arr)):
        print(str(i+1) + ". " + arr[i])

def getNumber(message):
    try: 
        inp = input(message).split()
        if len(inp) == 1:
            n = int(inp[0])
        elif len(inp) == 2:
            number, base = inp[0], inp[1]
            n = int(number, int(base))
        else:
            n = None
        return n
    except:
        bug(1)
        return None