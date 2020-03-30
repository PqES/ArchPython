def teste1():
    a = int(input())
    if a % 2 == 0:
        return True
    return "Impar"

def teste2(variavel):
    b = int(input())
    if b % 2 == 0:
        return teste3(variavel)
    return dict()

def teste3(p1):
    return 1.1


def main():
    resultado = teste1()
    saida = teste2(2)

main()   



