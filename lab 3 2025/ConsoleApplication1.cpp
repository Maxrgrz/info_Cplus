#include <iostream>
#include <vector>
#include <cassert>
#include <algorithm> // для std::max

using namespace std;

// Поразрядная сортировка (Radix Sort)
void countingSort(vector<int>& arr, int exp) {
    vector<int> output(arr.size());
    int count[10] = { 0 };

    for (int i = 0; i < arr.size(); i++)
        count[(arr[i] / exp) % 10]++;

    for (int i = 1; i < 10; i++)
        count[i] += count[i - 1];

    for (int i = arr.size() - 1; i >= 0; i--) {
        output[count[(arr[i] / exp) % 10] - 1] = arr[i];
        count[(arr[i] / exp) % 10]--;
    }

    for (int i = 0; i < arr.size(); i++)
        arr[i] = output[i];
}

void radixSort(vector<int>& arr) {
    if (arr.empty()) return;
    int maxEl = *max_element(arr.begin(), arr.end());
    for (int exp = 1; maxEl / exp > 0; exp *= 10)
        countingSort(arr, exp);
}

// Сортировка расческой (Comb Sort)
void combSort(vector<int>& arr) {
    int n = arr.size();
    int gap = n;
    bool swapped = true;

    while (gap > 1 || swapped) {
        gap = max(1, int(gap / 1.3));
        swapped = false;

        for (int i = 0; i + gap < n; i++) {
            if (arr[i] > arr[i + gap]) {
                swap(arr[i], arr[i + gap]);
                swapped = true;
            }
        }
    }
}

// Быстрая сортировка (Quick Sort)
int partition(vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);

        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

// Юнит-тесты
void testSortingAlgorithms() {
    // Базовый тест
    vector<int> original = { 170, 45, 75, 90, 802, 24, 2, 66 };
    vector<int> expected = { 2, 24, 45, 66, 75, 90, 170, 802 };

    // Тест Radix Sort
    vector<int> test1 = original;
    radixSort(test1);
    assert(test1 == expected);

    // Тест Comb Sort
    vector<int> test2 = original;
    combSort(test2);
    assert(test2 == expected);

    // Тест Quick Sort
    vector<int> test3 = original;
    quickSort(test3, 0, test3.size() - 1);
    assert(test3 == expected);

    // Тест отсортированного массива
    vector<int> sorted = { 1, 2, 3, 4, 5 };
    vector<int> sortedExpected = sorted;

    vector<int> test4 = sorted;
    radixSort(test4);
    assert(test4 == sortedExpected);

    vector<int> test5 = sorted;
    combSort(test5);
    assert(test5 == sortedExpected);

    vector<int> test6 = sorted;
    quickSort(test6, 0, test6.size() - 1);
    assert(test6 == sortedExpected);

    // Тест массива с одинаковыми элементами
    vector<int> sameElements = { 5, 5, 5, 5, 5 };
    vector<int> sameExpected = sameElements;

    vector<int> test7 = sameElements;
    radixSort(test7);
    assert(test7 == sameExpected);

    vector<int> test8 = sameElements;
    combSort(test8);
    assert(test8 == sameExpected);

    vector<int> test9 = sameElements;
    quickSort(test9, 0, test9.size() - 1);
    assert(test9 == sameExpected);

    // Тест массива из одного элемента
    vector<int> single = { 42 };
    vector<int> singleExpected = single;

    vector<int> test10 = single;
    radixSort(test10);
    assert(test10 == singleExpected);

    vector<int> test11 = single;
    combSort(test11);
    assert(test11 == singleExpected);

    vector<int> test12 = single;
    quickSort(test12, 0, test12.size() - 1);
    assert(test12 == singleExpected);

    // Тест пустого массива
    vector<int> empty = {};
    vector<int> emptyExpected = {};

    vector<int> test13 = empty;
    radixSort(test13);
    assert(test13 == emptyExpected);

    vector<int> test14 = empty;
    combSort(test14);
    assert(test14 == emptyExpected);

    vector<int> test15 = empty;
    quickSort(test15, 0, test15.size() - 1);
    assert(test15 == emptyExpected);

    // Тест с отрицательными числами (Radix Sort не поддерживает)
    vector<int> negatives = { -5, -1, -3, -2, -4 };
    vector<int> negativesExpected = { -5, -4, -3, -2, -1 };

    vector<int> test16 = negatives;
    combSort(test16);
    assert(test16 == negativesExpected);

    vector<int> test17 = negatives;
    quickSort(test17, 0, test17.size() - 1);
    assert(test17 == negativesExpected);

    cout << "Все тесты прошли успешно!" << endl;
}

int main() {
    testSortingAlgorithms();
    return 0;
}
