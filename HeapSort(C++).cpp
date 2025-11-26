#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <chrono> 
#include <iomanip>

/**
 * @brief 
 * @param 
 * @param 
 * @param 
 */
void heapify(std::vector<int>& arr, int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    if (left < n && arr[left] > arr[largest]) {
        largest = left;
    }
    if (right < n && arr[right] > arr[largest]) {
        largest = right;
    }
    if (largest != i) {
        std::swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}

/**
 * @brief
 * @param
 */
void heapSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(arr, n, i);
    }
    for (int i = n - 1; i > 0; i--) {
        std::swap(arr[0], arr[i]);
        heapify(arr, i, 0);
    }
}

/**
 * @brief
 * @param
 * @return
 */
std::vector<int> load_data(const std::string& filepath) {
    std::vector<int> data;
    std::ifstream file(filepath);
    
    if (!file.is_open()) {
        std::cerr << "Erro: Arquivo '" << filepath << "' não encontrado." << std::endl;
        exit(1);
    }

    int number;
    while (file >> number) {
        data.push_back(number);
    }

    file.close();
    return data;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Uso: ./heap_sort <caminho_para_arquivo_de_dados>" << std::endl;
        return 1;
    }

    std::string filepath = argv[1];
    std::vector<int> data = load_data(filepath);
    auto start = std::chrono::high_resolution_clock::now();
    heapSort(data);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> elapsed_ms = end - start;
    std::cout << std::fixed << std::setprecision(4) << elapsed_ms.count() << std::endl;
    bool sorted = true;
    for (size_t i = 0; i < data.size() - 1; ++i) {
        if (data[i] > data[i+1]) {
            sorted = false;
            break;
        }
    }
    std::cout << "Ordenado: " << (sorted ? "Sim" : "Não") << std::endl;

    return 0;
}