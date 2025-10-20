'''
            ASCII <-> BASE
    ASCII take 8 bit to represent
    To count how many bit take to represent in a base this formula
                bit per base = log2 of B
    -> base64 - 6 bits
    -> base32 - 5 bits
    -> base16 - 4 bits (hex)
    
    Bellow will implement Base64/32 encode/decode 
'''
'''
            Chuyển đổi giữa các base
    N(b1): số N được biễu diễn trong cơ số b1
    N(10): giá trị của N trong hệ thập phân (base 10)
    N(b2): biễn diễn của cùng số đó trong cơ số b2

    Giả sử: N(b1) = gồm k giá trị a từ k -> 0
    với mỗi ai thuộc 0 -> b1 - 1

    Bước 1 chuyển đổi sang base 10 làm trung gian
                N(10) = ai x b1^i

    Bước 2 chuyển đổi sang base b2
                N(10) = q1 X b2 + r0
                  q1  = q2 X b2 + r1
                  q2  = q3 X b2 + r2
                      .
                      .
                      .
                 qm-1 = qm X b2 + rm-1
                  qm  = 0
            => N(b2) = (rm-1 rm-2 ... r1 r0) (b2)
'''
from utils import *
b64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
b32_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"

def b64encode(message: str) -> str:
    binary = "".join(f'{ord(c):08b}' for c in message)
    pad = len(binary) % 6
    binary += '0' * pad

    encode = ""
    for i in range(0, len(binary), 6):
        pos = int(binary[i:i+6],2)
        encode += b64_alphabet[pos]
    
    encode += '=' * (pad // 2)
    return encode

def b64decode(encode: str) -> str:
    encode = encode.replace('=','')
    assert all(c in b64_alphabet for c in encode)

    message = ""
    binary = "".join(f'{b64_alphabet.index(c):06b}' for c in encode)
    for i in range(0,len(binary),8):
        data = binary[i:i+8]
        if len(data) == 8:
            message += chr(int(data,2))
    
    return message


def b32encode(message: str) -> str:
    binary = "".join(f'{ord(c):08b}' for c in message)
    pad = len(binary) % 5
    binary += pad * '0'

    encode = ""
    for i in range(0,len(binary),5):
        pos = int(binary[i:i+5],2)
        encode += b32_alphabet[pos]
    
    while len(encode) % 8 != 0:
        encode += '='
    return encode

def b32decode(encode: str) -> str:
    encode = encode.replace("=",'')
    assert all(c in b32_alphabet for c in encode)
    binary = ''.join(f'{b32_alphabet.index(c):05b}' for c in encode)

    message = ""
    for i in range(0, len(binary),8):
        data = binary[i:i+8]
        if len(data) == 8:
            message += chr(int(data, 2))
    return message


def main():
    arr = [
        "Base64 Encoding",
        "Base64 Decoding",
        "Base32 Encoding",
        "Base32 Decoding",
        "Exit"
    ]
    display_menu(arr, "Encoding/Decoding")
    while(True):
        c = getNumber("Enter your choice: ", 10)
        if c == 1:
            data = getString("Enter your data: ")
            print(b64encode(data))
        elif c == 2:
            data = getString("Enter your data: ")
            print(b64decode(data))
        elif c == 3:
            data = getString("Enter your data: ")
            print(b32encode(data))
        elif c == 4:
            data = getString("Enter your data: ")
            print(b32decode(data))
        else:
            exit(0)
    # pass

if __name__ == "__main__":
    main()