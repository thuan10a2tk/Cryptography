# This script copy from crypto_hack challenge writeup of sandy999 and r4sti player
# https://cryptohack.org/challenges/big/ - Version 1
# https://cryptohack.org/challenges/big2/ - Version 2

from utils import display, bug, getNumber
import math
from Crypto.Util.number import *
from sympy.ntheory import *
from sympy.core import *

def main():
    arr = [
        "Attack version 1",
        "Attack version 2",
        "Exit()",
    ]
    while True:
        print("===================== Small d attack =====================")
        display(arr)
        print("===================== Small d attack =====================")
        choice = getNumber("Enter your choice: ")
        if choice == 1:
            attack1()
        elif choice == 2:
            attack2()
        elif choice == 3:
            exit(0)
        else:
            bug(2)

def convergents(e):
    n = [] # Nominators
    d = [] # Denominators
    for i in range(len(e)):
        if i == 0:
            ni = e[i]
            di = 1
        elif i == 1:
            ni = e[i]*e[i-1] + 1
            di = e[i]
        else: # i > 1
            ni = e[i]*n[i-1] + n[i-2]
            di = e[i]*d[i-1] + d[i-2]

        n.append(ni)
        d.append(di)
    return n,d

def get_cf_expansion(x, y):
    cf_list = []
    x0 = x
    y0 = y
    q0 = x//y
    x0 = (x-y*q0)
    cf_list.append(q0)
    while x0 != 0:
        temp = y0
        y0 = x0
        x0 = temp
        q0 = x0//y0
        x0 = (x0-y0*q0)
        cf_list.append(q0)
    return cf_list

def is_square(apositiveint):
  x = apositiveint // 2
  seen = set([x])
  while x * x != apositiveint:
    x = (x + (apositiveint // x)) // 2
    if x in seen: return False
    seen.add(x)
  return True



def attack1():
    # example
    # N = 0x8da7d2ec7bf9b322a539afb9962d4d2ebeb3e3d449d709b80a51dc680a14c87ffa863edfc7b5a2a542a0fa610febe2d967b58ae714c46a6eccb44cd5c90d1cf5e271224aa3367e5a13305f2744e2e56059b17bf520c95d521d34fdad3b0c12e7821a3169aa900c711e6923ca1a26c71fc5ac8a9ff8c878164e2434c724b68b508a030f86211c1307b6f90c0cd489a27fdc5e6190f6193447e0441a49edde165cf6074994ea260a21ea1fc7e2dfb038df437f02b9ddb7b5244a9620c8eca858865e83bab3413135e76a54ee718f4e431c29d3cb6e353a75d74f831bed2cc7bdce553f25b617b3bdd9ef901e249e43545c91b0cd8798b27804d61926e317a2b745
    # e = 0x86d357db4e1b60a2e9f9f25e2db15204c820b6e8d8d04d29db168c890bc8a6c1e31b9316c9680174e128515a00256b775a1a8ccca9c6936f1b4c2298c03032cda4dd8eca1145828d31466bf56bfcf0c6a8b4a1b2fb27de7a57fae7430048d7590734b2f05b6443ad60d89606802409d2fa4c6767ad42bffae01a8ef1364418362e133fa7b2770af64a68ad50ad8d2bd5cebb99ceb13368fb31a6e7503e753f8638e21a96af1b6498c18578ba89b98d70fa482ad137d28fe701b4b77baa25d5e84c81b26ee9bddf8cbb51a071c60dd57714de379cd4bc14932809ba18524a0a18e4133665cfc46e2c4fcfbc28e0a0957e5513a7307c422b87a6182d0b6a074b4d
    # c = 0x6a2f2e401a54eeb5dab1e6d5d80e92a6ca189049e22844c825012b8f0578f95b269b19644c7c8af3d544840d380ed75fdf86844aa8976622fa0501eaec0e5a1a5ab09d3d1037e55501c4e270060470c9f4019ced6c4e67673843daf2fd71c64f3dd8939ae322f2b79d283b3382052d076ebe9bb50b0042f1f7dd7beadf0f5686926ade9fc8370283ead781a21896e7a878d99e77c3bb1f470401062c0e0327fd85da1cf12901635f1df310e8f8c7d87aff5a01dbbecd739cd8f36462060d0eb237af8d613e2d9cebb67d612bcfc353ef2cd44b7ac85e471287eb04ae9b388b66ea8eb32429ae96dba5da8206894fa8c58a7440a127fceb5717a2eaa3c29f25f7
    
    N = getNumber("Enter N (number base): ")
    e = getNumber("Enter e (number base): ")
    c = getNumber("Enter c (number base): ")
    if c is None or e is None or N is None:
        bug(3)
        return
    
    cf_expansion = get_cf_expansion(e,N)
    print(cf_expansion)

    for i in range(len(cf_expansion)):
        print("Iteration " + str(i))
        guess_kdg_expansion = cf_expansion[:i]
        if i % 2 == 0:
            guess_kdg_expansion.append(cf_expansion[i]+1)
        else:
            guess_kdg_expansion.append(cf_expansion[i])
        ni, di = convergents(guess_kdg_expansion)
        guess_k = ni[i]
        guess_dg = di[i]
        guess_edg = e*guess_dg
        guess_phi = guess_edg//guess_k
        guess_g = guess_edg % guess_k
        if (N - guess_phi + 1) % 2 == 1:
            continue
        guess_p_plus_q_by_2 = (N - guess_phi + 1)//2
        guess_p_minus_q_by_2_sq = guess_p_plus_q_by_2**2 - N
        if is_square( guess_p_minus_q_by_2_sq):
            print("D: " + str(guess_dg//guess_g))
            print(long_to_bytes(pow(c,guess_dg//guess_g,N)))
            break

def attack2():
    # Example
    # n = 0x665166804cd78e8197073f65f58bca14e019982245fcc7cad74535e948a4e0258b2e919bf3720968a00e5240c5e1d6b8831d8fec300d969fccec6cce11dde826d3fbe0837194f2dc64194c78379440671563c6c75267f0286d779e6d91d3e9037c642a860a894d8c45b7ed564d341501cedf260d3019234f2964ccc6c56b6de8a4f66667e9672a03f6c29d95100cdf5cb363d66f2131823a953621680300ab3a2eb51c12999b6d4249dde499055584925399f3a8c7a4a5a21f095878e80bbc772f785d2cbf70a87c6b854eb566e1e1beb7d4ac6eb46023b3dc7fdf34529a40f5fc5797f9c15c54ed4cb018c072168e9c30ca3602e00ea4047d2e5686c6eb37b9
    # e = 0x2c998e57bc651fe4807443dbb3e794711ca22b473d7792a64b7a326538dc528a17c79c72e425bf29937e47b2d6f6330ee5c13bfd8564b50e49132d47befd0ee2e85f4bfe2c9452d62ef838d487c099b3d7c80f14e362b3d97ca4774f1e4e851d38a4a834b077ded3d40cd20ddc45d57581beaa7b4d299da9dec8a1f361c808637238fa368e07c7d08f5654c7b2f8a90d47857e9b9c0a81a46769f6307d5a4442707afb017959d9a681fa1dc8d97565e55f02df34b04a3d0a0bf98b7798d7084db4b3f6696fa139f83ada3dc70d0b4c57bf49f530dec938096071f9c4498fdef9641dfbfe516c985b27d1748cc6ce1a4beb1381fb165a3d14f61032e0f76f095d
    # ct = 0x503d5dd3bf3d76918b868c0789c81b4a384184ddadef81142eabdcb78656632e54c9cb22ac2c41178607aa41adebdf89cd24ec1876365994f54f2b8fc492636b59382eb5094c46b5818cf8d9b42aed7e8051d7ca1537202d20ef945876e94f502e048ad71c7ad89200341f8071dc73c2cc1c7688494cad0110fca4854ee6a1ba999005a650062a5d55063693e8b018b08c4591946a3fc961dae2ba0c046f0848fbe5206d56767aae8812d55ee9decc1587cf5905887846cd3ecc6fc069e40d36b29ee48229c0c79eceab9a95b11d15421b8585a2576a63b9f09c56a4ca1729680410da237ac5b05850604e2af1f4ede9cf3928cbb3193a159e64482928b585ac
    # prefix = b'crypto{'

    n = getNumber("Enter n (number base): ")
    e = getNumber("Enter e (number base): ")
    ct = getNumber("Enter ct (number base): ")
    prefix = input("Enter flag format: ").encode()
    if ct is None or e is None or n is None or len(prefix) == 0:
        bug(3)
        return
    
    def wiener_variant(e, n):
        q0 = 1

        cf = continued_fraction_periodic(e,n)
        denoms = [q.q for q in list(continued_fraction_convergents(cf))]
        
        print('[+] Extracted denominators.')

        for q1 in denoms:
            for r in range(5):
                for s in range(5):
                    d = r * q1 + s * q0
                    pt = long_to_bytes(pow(ct, d, n))

                    if prefix in pt:
                        return pt, d
                
            q0 = q1
        return None
    
    flag, d = wiener_variant(e, n)

    print('[+] Private key (d) =', d)
    print('[+] Recovered flag :', flag.decode())
    pass
if __name__ == "__main__":
    main()