import subprocess
import sys
import os
import statistics

ITERATIONS = 20


TEST_CONFIG = [
    {"label": "Pequena", "size": 10000,    "filename": "dados_pequenos.txt"},
    {"label": "Média",   "size": 500000,   "filename": "dados_medios.txt"},
    {"label": "Grande",  "size": 2000000,  "filename": "dados_grandes.txt"}
]
PYTHON_SORTER = "HeapSort(Python).py"
CPP_SORTER_SRC = "HeapSort(C++).cpp"
CPP_SORTER_BIN = "heap_sort_cpp"
GENERATOR_SCRIPT = "GeradorDeDados.py"

def verificar_e_compilar_cpp():
    print("--- Verificando C++ ---")
    if os.path.exists(CPP_SORTER_BIN):
        try:
            os.remove(CPP_SORTER_BIN)
        except OSError:
            pass
    cmd = ["g++", "-std=c++20", "-O3", "-o", CPP_SORTER_BIN, CPP_SORTER_SRC]
    
    try:
        subprocess.run(cmd, check=True)
        print("Compilação C++ concluída com sucesso.\n")
        return True
    except subprocess.CalledProcessError:
        print("AVISO: Erro ao compilar o código C++. Verifique se o g++ está instalado e se o código não tem erros.")
        print("Os testes de C++ serão ignorados.\n")
        return False
    except FileNotFoundError:
        print("AVISO: Compilador 'g++' não encontrado no sistema. Os testes de C++ serão ignorados.\n")
        return False

def garantir_arquivos_dados():
    print("--- Verificando arquivos de dados ---")
    for config in TEST_CONFIG:
        if not os.path.exists(config["filename"]):
            print(f"Gerando {config['filename']} ({config['size']} elementos)...")
            try:
                with open(config["filename"], "w") as outfile:
                    subprocess.run(
                        [sys.executable, GENERATOR_SCRIPT, str(config["size"])],
                        stdout=outfile,
                        check=True
                    )
            except Exception as e:
                print(f"Erro crítico ao gerar dados: {e}")
                sys.exit(1)
        else:
            print(f"Arquivo {config['filename']} já existe.")
    print("--- Arquivos prontos ---\n")

def executar_benchmark(comando, label, linguagem):
    tempos = []
    print(f"Rodando {linguagem} [{label}]", end="", flush=True)

    for _ in range(ITERATIONS):
        try:
            resultado = subprocess.run(
                comando, 
                capture_output=True, 
                text=True, 
                check=True
            )
            output_lines = resultado.stdout.strip().split('\n')
            if output_lines:
                tempo_ms = float(output_lines[0].strip())
                tempos.append(tempo_ms)
                print(".", end="", flush=True)
        except ValueError:
            print("!", end="", flush=True) 
        except subprocess.CalledProcessError as e:
            print("X", end="", flush=True) 
    print(" Concluído.")
    
    if tempos:
        media = statistics.mean(tempos)
        desvio = statistics.stdev(tempos) if len(tempos) > 1 else 0.0
        return media, desvio
    return None, None

def main():
    if not os.path.exists(PYTHON_SORTER):
        print(f"ERRO: Não encontrei o arquivo '{PYTHON_SORTER}'.")
        print("Certifique-se de salvar este script na MESMA pasta dos arquivos do trabalho.")
        sys.exit(1)

    garantir_arquivos_dados()
    tem_cpp = verificar_e_compilar_cpp()

    print("\n" + "="*75)
    print(f"{'TAMANHO (n)':<15} {'LINGUAGEM':<12} {'MÉDIA (ms)':<15} {'DESVIO PADRÃO':<15}")
    print("="*75)

    for config in TEST_CONFIG:
        cmd_py = [sys.executable, PYTHON_SORTER, config["filename"]]
        media, desvio = executar_benchmark(cmd_py, config["label"], "Python")
        if media is not None:
            print(f"{config['size']:<15} {'Python':<12} {media:<15.4f} {desvio:<15.4f}")

        if tem_cpp and os.path.exists(CPP_SORTER_BIN):
            
            executavel = f"./{CPP_SORTER_BIN}" if sys.platform != "win32" else CPP_SORTER_BIN
            cmd_cpp = [executavel, config["filename"]]
            
            media, desvio = executar_benchmark(cmd_cpp, config["label"], "C++")
            if media is not None:
                print(f"{config['size']:<15} {'C++':<12} {media:<15.4f} {desvio:<15.4f}")
        
        print("-" * 75)

if __name__ == "__main__":
    main()