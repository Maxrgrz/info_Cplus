
#include <iostream>
#include <cmath>
#include <algorithm> // For std::max and std::min

int main() {
    float x, y;
    std::cout << "Enter values for x and y: ";
    std::cin >> x >> y;

    // Calculating R and S
    float R = (-x - std::sqrt(x * x - 4 * x * y)) / (2 * y);
    float S = std::log(std::pow(2, x)) - std::tan(std::min(x, y));

    // Finding maximum of R and S (C)
    float C = std::max(R, S);

    // Output results
    std::cout << "R = " << R << std::endl;
    std::cout << "S = " << S << std::endl;
    std::cout << "C (max(R, S)) = " << C << std::endl;

    return 0;
}
