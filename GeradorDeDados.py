import sys
import random

def gerar_dados(n, max_val=1000000):
    for _ in range(n):
        print(random.randint(0, max_val))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python gerador_dados.py <numero_de_elementos>", file=sys.stderr)
        sys.exit(1)
    
    try:
        n = int(sys.argv[1])
        if n <= 0:
            raise ValueError()
    except ValueError:
        print("Erro: O número de elementos deve ser um inteiro positivo.", file=sys.stderr)
        sys.exit(1)

    gerar_dados(n)
