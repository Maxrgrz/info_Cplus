#include <iostream>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <cassert>

// Функции для проверки попадания в область
bool isInside(double x, double y) {
    return (y <= 2 - 0.5 * x) && (y >= -2 + 0.5 * x) &&
        (y >= -2 - 0.5 * x) && (y <= 2 + 0.5 * x);
}

// Функция вычисления площади методом Монте-Карло
double monteCarlo(int N) {
    int count = 0;
    double x_min = -4, x_max = 4, y_min = -4, y_max = 4;
    double area_rect = (x_max - x_min) * (y_max - y_min);

    srand(time(0));
    for (int i = 0; i < N; i++) {
        double x = x_min + (x_max - x_min) * (rand() / (double)RAND_MAX);
        double y = y_min + (y_max - y_min) * (rand() / (double)RAND_MAX);
        if (isInside(x, y)) count++;
    }

    return (count / (double)N) * area_rect;
}

// Unit-тестирование
void test() {
    double expected_value = 8.0; // Ожидаемая площадь (из расчетов)
    double epsilon = 0.5;

    assert(std::abs(monteCarlo(10000) - expected_value) < epsilon);
    assert(std::abs(monteCarlo(50000) - expected_value) < epsilon);
    assert(std::abs(monteCarlo(100000) - expected_value) < epsilon);

    std::cout << "Все тесты пройдены!" << std::endl;
}

int main() {
    int N = 100000;
    std::cout << "Приближенная площадь фигуры: " << monteCarlo(N) << std::endl;
    test();
    return 0;
}