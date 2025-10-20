def getString(s: str)-> str:
    data = input(s)
    return data

def getNumber(s: str, b: int)-> int:
    data = input(s)
    return int(data,b)

def display_menu(arr: list, s:  str):
    print(f'=============={s}==============')
    for i in range(len(arr)):
        print(f'{i+1}. {arr[i]}')
    print(f'=============={s}==============')
    