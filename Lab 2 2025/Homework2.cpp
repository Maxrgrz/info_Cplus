#include <iostream>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <cassert>

using namespace std;

// Функция проверки, находится ли точка внутри фигуры
bool isInside(double x, double y) {
    return (y <= 2 - 0.5 * x && y >= -2 + 0.5 * x && y >= -2 - 0.5 * x && y <= 2 + 0.5 * x);
}

// Метод Монте-Карло для вычисления площади фигуры
double monteCarlo(int N) {
    int countInside = 0;
    double x, y;
    double xmin = -4, xmax = 4, ymin = -2, ymax = 2;
    double areaRect = (xmax - xmin) * (ymax - ymin);

    srand(time(0));
    for (int i = 0; i < N; i++) {
        x = xmin + (xmax - xmin) * (rand() / (double)RAND_MAX);
        y = ymin + (ymax - ymin) * (rand() / (double)RAND_MAX);

        if (isInside(x, y)) {
            countInside++;
        }
    }

    return areaRect * (countInside / (double)N);
}

// Unit-тест с точностью
void testMonteCarlo() {
    double expected = 16.0; // Теоретическая площадь ромба
    double tolerance = 0.5; // Допустимая ошибка

    double area1 = monteCarlo(10000);
    double area2 = monteCarlo(50000);
    double area3 = monteCarlo(100000);

    assert(fabs(area1 - expected) < tolerance && "Ошибка: при N=10 000 площадь вне допустимого отклонения");
    assert(fabs(area2 - expected) < tolerance && "Ошибка: при N=50 000 площадь вне допустимого отклонения");
    assert(fabs(area3 - expected) < tolerance && "Ошибка: при N=100 000 площадь вне допустимого отклонения");

    cout << "Все unit-тесты успешно пройдены!" << endl;
}

int main() {
    int N;
    cout << "Введите количество испытаний N: ";
    cin >> N;

    double area = monteCarlo(N);
    cout << "Приближенная площадь фигуры: " << area << endl;

    testMonteCarlo(); // Запускаем unit-тесты

    return 0;
}