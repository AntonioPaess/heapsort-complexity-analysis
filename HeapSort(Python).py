import sys
import time
import random

def heapify(arr, n, i):
    largest = i 
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

def load_data(filepath):
    try:
        with open(filepath, 'r') as f:
            data = [int(line.strip()) for line in f]
        return data
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filepath}' não encontrado.", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        print(f"Erro: Arquivo '{filepath}' contém dados inválidos.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python heap_sort.py <caminho_para_arquivo_de_dados>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    data = load_data(filepath)
    data_to_sort = list(data)
    start_time = time.perf_counter()
    heap_sort(data_to_sort)
    end_time = time.perf_counter()

    elapsed_time_ms = (end_time - start_time) * 1000

    print(f"{elapsed_time_ms:.4f}")
    print("Ordenado:", all(data_to_sort[i] <= data_to_sort[i+1] for i in range(len(data_to_sort)-1)))
