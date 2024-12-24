#include "pch.h"
#include "Header.h"
using namespace std;

int* sumArrays(int* arr1, int* arr2, const int size) {
    int* result = new int[size];
    for (int i = 0; i < size; ++i) {
        result[i] = arr1[i] + arr2[i];
    }
    return result;
}