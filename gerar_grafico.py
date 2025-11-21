import matplotlib.pyplot as plt
import numpy as np

tamanhos = [10000, 500000, 2000000]

py_media = [21.9416, 1839.4311, 12027.9302]
py_desvio = [0.1733, 36.7408, 358.8735]  


cpp_media = [0.6912, 48.7736, 253.0781]  

cpp_desvio = [0.1841, 0.5261, 16.2405] 

plt.figure(figsize=(12, 7))
plt.errorbar(tamanhos, py_media, yerr=py_desvio, 
             fmt='-o', linewidth=2, capsize=5, 
             color='#1f77b4', label='Python (Interpretado)')
plt.errorbar(tamanhos, cpp_media, yerr=cpp_desvio, 
             fmt='--s', linewidth=2, capsize=5, 
             color='#d62728', label='C++ (Compilado)')

plt.xlabel('Tamanho da Entrada ($n$)', fontsize=12, fontweight='bold')
plt.ylabel('Tempo de Execução (ms) - Escala Log', fontsize=12, fontweight='bold')
plt.title('Análise de Desempenho: Heap Sort (Python vs C++)', fontsize=14)
plt.yscale('log')

def anotar_pontos(xs, ys, cor, offset_y):
    for x, y in zip(xs, ys):
        if y > 0:
            plt.annotate(f'{y:.1f}ms', 
                        (x, y), 
                        textcoords="offset points", 
                        xytext=(0, offset_y), 
                        ha='center', fontsize=9, color=cor, fontweight='bold')

anotar_pontos(tamanhos, py_media, '#1f77b4', 10)  
anotar_pontos(tamanhos, cpp_media, '#d62728', -15) 

plt.grid(True, which="both", ls="--", alpha=0.4)
plt.legend(fontsize=11, loc='upper left')
plt.xticks(tamanhos, labels=[f'{n:,}'.replace(',', '.') for n in tamanhos]) 
plt.tight_layout()
plt.savefig('grafico_robusto_heapsort.png', dpi=300) 
print("Gráfico salvo como 'grafico_robusto_heapsort.png'")
plt.show()