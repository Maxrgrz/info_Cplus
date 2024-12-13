#include <SFML/Graphics.hpp>
#include <functional> 
#include <cmath>
#include <string>

// Функция для отрисовки графика
void drawGraphY(sf::RenderWindow& window, std::function<float(float)> func, float xMin, float xMax, float scaleX, float scaleY, sf::Color color) {
    sf::VertexArray graph(sf::LinesStrip);

    for (float x = xMin; x <= xMax; x += 0.1f) {
        float y = func(x); // Вычисление значения функции

        // Преобразование координат в экранные
        float screenX = 400 + x * scaleX;
        float screenY = 300 - y * scaleY;

        // Добавление точки в массив
        graph.append(sf::Vertex(sf::Vector2f(screenX, screenY), color));
    }

    window.draw(graph);
}

void drawGraphX(sf::RenderWindow& window, std::function<float(float)> func, float xMin, float xMax, float scaleX, float scaleY, sf::Color color) {
    sf::VertexArray graph(sf::LinesStrip);

    for (float y = xMin; y <= xMax; y += 0.1f) {
        float x = func(y); // Вычисление значения функции

        // Преобразование координат в экранные
        float screenX = 400 + x * scaleX;
        float screenY = 300 - y * scaleY;

        // Добавление точки в массив
        graph.append(sf::Vertex(sf::Vector2f(screenX, screenY), color));
    }

    window.draw(graph);
}

int main() {

    // Создание окна
    sf::RenderWindow window(sf::VideoMode(800, 600), "Рисование для вывода графиков");

    // Переменная для отображения пользовательской точки
    sf::CircleShape userPoint(5); // Радиус 5 пикселей
    userPoint.setFillColor(sf::Color::Red);
    bool userPointExists = false; // Переменная для проверки существования пользовательской точки

    // 1 _ Загрузка шрифта
    sf::Font font;
    if (!font.loadFromFile("arial.ttf")) {
        return -1;
    }

    // 2 _ Текст для отображения координат точки
    sf::Text coordinatesText;
    coordinatesText.setFont(font);
    coordinatesText.setCharacterSize(20);
    coordinatesText.setFillColor(sf::Color::White);
    coordinatesText.setPosition(10, 10);

    // Ось X и Y
    sf::VertexArray xAxis(sf::Lines, 2);
    xAxis[0].position = sf::Vector2f(50, 300); // Начало оси X
    xAxis[0].color = sf::Color::White; // Цвет оси
    xAxis[1].position = sf::Vector2f(750, 300); // Конец оси X
    xAxis[1].color = sf::Color::White;

    sf::VertexArray yAxis(sf::Lines, 2);
    yAxis[0].position = sf::Vector2f(400, 50); // Начало оси Y
    yAxis[0].color = sf::Color::White; // Цвет оси
    yAxis[1].position = sf::Vector2f(400, 550); // Конец оси Y
    yAxis[1].color = sf::Color::White;

    std::string section;

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();

            // Обработка клика мыши
            if (event.type == sf::Event::MouseButtonPressed) {
                if (event.mouseButton.button == sf::Mouse::Left) {
                    // Получение позиции мыши
                    sf::Vector2i mousePos = sf::Mouse::getPosition(window);

                    // Преобразование экранных координат в математические
                    float mathX = (mousePos.x - 400) / 50.0f; // Масштаб 50 по X
                    float mathY = -(mousePos.y - 300) / 50.0f; // Масштаб 50 по Y

                    // Отображение новой точки
                    userPoint.setPosition(mousePos.x - userPoint.getRadius(), mousePos.y - userPoint.getRadius());
                    userPointExists = true; // Устанавливаем, что точка существует

                    // 3 _ Определение сектора
                    if ((mathY == mathX) || (mathX == 3)) {
                        section = "Border";
                    }
                    else if ((mathX < 3) && (mathY < mathX)) {
                        section = "1";
                    }
                    else if ((mathX > 3) && (mathY > mathX)) {
                        section = "2";
                    }
                    else if ((mathY > mathX) && (mathX < 3)) {
                        section = "3";
                    }
                    else if ((mathY < mathX) && (mathX > 3)) {
                        section = "4";
                    }

                    // Обновление текста с координатами
                    coordinatesText.setString("Coordinates: (" + std::to_string(mathX) + ", " + std::to_string(mathY) + ") Position: " + section);
                }
            }
        }

        // 4 _ Очистка экрана
        window.clear();

        // Отображение осей
        window.draw(xAxis);
        window.draw(yAxis);

        // 5 _ Отображение графиков
        drawGraphY(window, [](float x) { return -x * x + 2 * x + 10; }, -10, 10, 50, 50, sf::Color::Red); // -x*x+2*x+10x
        drawGraphX(window, [](float y) { return x * x + 2 * x - 10; }, -10, 10, 50, 50, sf::Color::Blue); // x*x+2*x-10

        // Отображение пользовательской точки, если она существует
        if (userPointExists) {
            window.draw(userPoint);
            window.draw(coordinatesText);
        }

        // Отображение нового кадра
        window.display();
    }

    return 0;
}