import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
    'figure.titlesize': 14
})

tamanhos = np.array([10000, 500000, 2000000])
py_media = np.array([21.9416, 1839.4311, 12027.9302])
cpp_media = np.array([0.6912, 48.7736, 253.0781])
py_desvio = np.array([0.1733, 36.7408, 358.8735])
cpp_desvio = np.array([0.1841, 0.5261, 16.2405])

def calcular_teorico(n_reais, tempos_reais):
    """Gera a curva teórica k * n * log(n) ajustada."""
    n_safe = np.array(n_reais, dtype=float)
    complexidade = n_safe * np.log2(n_safe)
    k = np.mean(tempos_reais / complexidade)
    n_suave = np.linspace(min(n_reais), max(n_reais), 200)
    curva_teorica = k * (n_suave * np.log2(n_suave))
    return n_suave, curva_teorica

def calcular_media_movel(dados, janela=2):
    """Calcula média móvel simples."""
    if len(dados) < janela:
        return dados
    return np.convolve(dados, np.ones(janela)/janela, mode='valid')

def anotar_valores(ax, xs, ys, desvios, cor_texto='black', offset=15):
    """
    Anota Média ± Desvio Padrão com uma caixa de fundo para leitura perfeita.
    """
    for x, y, desvio in zip(xs, ys, desvios):
        if y < 10:
            texto = f"{y:.2f} \u00B1 {desvio:.2f}"
        else:
            texto = f"{y:.1f} \u00B1 {desvio:.1f}"
            
        ax.annotate(texto, 
                    (x, y), 
                    xytext=(0, offset), 
                    textcoords='offset points',
                    ha='center', va='bottom',
                    color=cor_texto,
                    fontweight='bold',
                    fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9))

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 7))
fig.suptitle('Análise de Desempenho Heap Sort: Teoria vs Prática', fontweight='bold', y=0.98)
ax1.plot(tamanhos, py_media, 'o-', color='#1f77b4', linewidth=2, label='Python (Média)')
ax1.plot(tamanhos, cpp_media, 's-', color='#d62728', linewidth=2, label='C++ (Média)')
mm_py = calcular_media_movel(py_media)
ax1.plot(tamanhos[len(tamanhos)-len(mm_py):], mm_py, '--', color='navy', linewidth=2, alpha=0.7, label='Média Móvel (Py)')

mm_cpp = calcular_media_movel(cpp_media)
ax1.plot(tamanhos[len(tamanhos)-len(mm_cpp):], mm_cpp, '--', color='darkred', linewidth=2, alpha=0.7, label='Média Móvel (C++)')

ax1.set_title('Comparativo de Velocidade (Log)', fontweight='bold')
ax1.set_xlabel('Tamanho da Entrada (n)')
ax1.set_ylabel('Tempo (ms) - Escala Logarítmica')
ax1.set_yscale('log')
ax1.legend(loc='upper left', frameon=True)
ax1.grid(True, which="both", linestyle='--', alpha=0.4)

for x, y in zip(tamanhos, py_media):
    ax1.annotate(f"{y:.0f}", (x, y), xytext=(0, 5), textcoords="offset points", ha='center', color='#1f77b4', fontweight='bold')
for x, y in zip(tamanhos, cpp_media):
    ax1.annotate(f"{y:.1f}", (x, y), xytext=(0, -15), textcoords="offset points", ha='center', color='#d62728', fontweight='bold')
ax2.errorbar(tamanhos, py_media, yerr=py_desvio, fmt='o-', color='#1f77b4', ecolor='black', capsize=5, label='Prático (Curva Medida)', linewidth=2)
n_teo, tempo_teo = calcular_teorico(tamanhos, py_media)
ax2.plot(n_teo, tempo_teo, color='black', linestyle=':', linewidth=2, label=r'Teórico $\Theta(n \log n)$')

anotar_valores(ax2, tamanhos, py_media, py_desvio, cor_texto='#1f77b4')

ax2.set_title('Python: Prática vs Teoria', fontweight='bold', color='#1f77b4')
ax2.set_xlabel('Tamanho da Entrada (n)')
ax2.set_ylabel('Tempo (ms)')
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.4)
ax2.set_ylim(top=max(py_media)*1.15) 
ax3.errorbar(tamanhos, cpp_media, yerr=cpp_desvio, fmt='s-', color='#d62728', ecolor='black', capsize=5, label='Prático (Curva Medida)', linewidth=2)
n_teo_cpp, tempo_teo_cpp = calcular_teorico(tamanhos, cpp_media)
ax3.plot(n_teo_cpp, tempo_teo_cpp, color='black', linestyle=':', linewidth=2, label=r'Teórico $\Theta(n \log n)$')

anotar_valores(ax3, tamanhos, cpp_media, cpp_desvio, cor_texto='#d62728')

ax3.set_title('C++: Prática vs Teoria', fontweight='bold', color='#d62728')
ax3.set_xlabel('Tamanho da Entrada (n)')
ax3.set_ylabel('Tempo (ms)')
ax3.legend()
ax3.grid(True, linestyle='--', alpha=0.4)
ax3.set_ylim(top=max(cpp_media)*1.15)

plt.tight_layout(pad=3.0)
plt.savefig('grafico_analise_completa.png', dpi=300, bbox_inches='tight')
print("Gráfico gerado: 'grafico_analise_completa.png'")
plt.show()
