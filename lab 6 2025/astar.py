import pygame
import random
from queue import PriorityQueue

# Инициализация Pygame
pygame.init()  # Инициализируем библиотеку Pygame для работы с графикой

# Настройки окна
GRID_SIZE = 10  # Определяем размер сетки 10x10
CELL_SIZE = 50  # Устанавливаем размер одной ячейки в пикселях
WINDOW_SIZE = GRID_SIZE * CELL_SIZE  # Вычисляем общий размер окна
WIN = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))  # Создаём окно с заданным размером
pygame.display.set_caption("A*")  # Устанавливаем заголовок окна

# Цвета
WHITE = (255, 255, 255)    # Цвет для пустой ячейки
BLACK = (0, 0, 0)          # Цвет для препятствий
ORANGE = (255, 165, 0)     # Цвет для начальной точки
TURQUOISE = (64, 224, 208) # Цвет для конечной точки
GREEN = (0, 255, 0)        # Цвет для ячеек в очереди (open set)
RED = (255, 0, 0)          # Цвет для посещённых ячеек (closed set)
PURPLE = (128, 0, 128)     # Цвет для итогового пути
GREY = (128, 128, 128)     # Цвет для линий сетки


# Класс ячейки
class Cell:
    def __init__(self, row, col):
        self.row = row  # Номер строки ячейки
        self.col = col  # Номер столбца ячейки
        self.x = row * CELL_SIZE  # Координата x для отрисовки
        self.y = col * CELL_SIZE  # Координата y для отрисовки
        self.color = WHITE  # Начальный цвет ячейки (пустая)
        self.neighbors = []  # Список соседних ячеек
        self.g = float("inf")  # Начальная стоимость пути от старта (бесконечность)
        self.h = 0  # Эвристическая оценка до цели
        self.f = float("inf")  # Полная оценка (g + h)
        self.came_from = None  # Родительская ячейка для восстановления пути
        self.is_barrier = False  # Флаг, обозначающий препятствие
        self.weight = 1
        self.font = pygame.font.SysFont('Arial', 12)

    def get_pos(self):
        return self.row, self.col  # Возвращает позицию ячейки (row, col)

    def make_start(self):
        self.color = ORANGE  # Устанавливает цвет как начальную точку

    def make_end(self):
        self.color = TURQUOISE  # Устанавливает цвет как конечную точку

    def make_barrier(self):
        self.color = BLACK  # Устанавливает цвет как препятствие
        self.is_barrier = True  # Помечает ячейку как препятствие

    def make_open(self):
        self.color = GREEN  # Устанавливает цвет для ячеек в очереди

    def make_closed(self):
        self.color = RED  # Устанавливает цвет для посещённых ячеек

    def make_path(self):
        self.color = PURPLE  # Устанавливает цвет для итогового пути

    def reset(self):
        self.color = WHITE  # Сбрасывает цвет в исходное состояние
        self.is_barrier = False  # Снимает флаг препятствия
        self.weight = 1

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))  # Отрисовка ячейки
        if self.weight > 1 and not self.is_barrier and self.color not in [ORANGE, TURQUOISE]:
            text = self.font.render(str(self.weight), True, BLACK)
            win.blit(text, (self.x + CELL_SIZE // 2 - 5, self.y + CELL_SIZE // 2 - 5))

    def update_neighbors(self, grid):
        self.neighbors = []  # Очищаем список соседей
        # Проверяем соседей (вверх, вниз, влево, вправо)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc  # Вычисляем координаты соседей
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and not grid[r][c].is_barrier:
                self.neighbors.append(grid[r][c])  # Добавляем допустимых соседей


# Создание сетки
def make_grid(random_map=False):
    grid = []  # Инициализируем список для сетки
    for i in range(GRID_SIZE):  # Проходим по строкам
        row = []  # Создаём строку
        for j in range(GRID_SIZE):  # Проходим по столбцам
            cell = Cell(i, j)  # Создаём ячейку
            row.append(cell)  # Добавляем ячейку в строку
        grid.append(row)  # Добавляем строку в сетку
    if random_map:
        generate_random_map(grid)
    return grid  # Возвращаем созданную сетку


# Генерация случайной карты
def generate_random_map(grid):
    for row in grid:
        for cell in row:
            if random.random() < 0.2:
                cell.make_barrier()
            elif random.random() < 0.3:
                cell.weight = random.randint(2, 5)


# Отрисовка линий сетки
def draw_grid_lines(win):
    for i in range(GRID_SIZE):  # Проходим по всем линиям
        pygame.draw.line(win, GREY, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE))  # Горизонтальные линии
        pygame.draw.line(win, GREY, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE))  # Вертикальные линии


# Отрисовка всего
def draw(win, grid):
    win.fill(WHITE)  # Заполняем окно белым фоном
    for row in grid:  # Проходим по всем строкам
        for cell in row:  # Проходим по всем ячейкам в строке
            cell.draw(win)  # Отрисовываем каждую ячейку
    draw_grid_lines(win)  # Рисуем линии сетки
    pygame.display.update()  # Обновляем дисплей


# Манхэттенское расстояние
def h(p1, p2):
    x1, y1 = p1  # Координаты первой точки
    x2, y2 = p2  # Координаты второй точки
    return abs(x1 - x2) + abs(y1 - y2)  # Вычисляем манхэттенское расстояние


# Восстановление пути
def reconstruct_path(came_from, current, draw_func):
    while current in came_from:  # Пока есть родительская ячейка
        current = came_from[current]  # Переходим к родителю
        current.make_path()  # Помечаем ячейку как часть пути
        draw_func()  # Обновляем визуализацию


# Алгоритм A*
def a_star_algorithm(draw_func, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    open_set_hash = {start}

    start.g = 0
    start.h = h(start.get_pos(), end.get_pos())
    start.f = start.g + start.h

    came_from = {}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw_func)
            start.make_start()
            end.make_end()
            return True

        current.make_closed()

        for neighbor in current.neighbors:
            temp_g = current.g + neighbor.weight

            if temp_g < neighbor.g:
                came_from[neighbor] = current
                neighbor.g = temp_g
                neighbor.h = h(neighbor.get_pos(), end.get_pos())
                neighbor.f = neighbor.g + neighbor.h

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((neighbor.f, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw_func()

    return False


# Основная функция
def main():
    grid = make_grid()  # Создаём сетку
    obstacles = [
        (3, 0), (8, 0), (9, 0), (0, 1),
        (1, 1), (2, 1), (7, 1), (1, 2),
        (2, 2), (5, 2), (7, 2), (0, 3),
        (2, 3), (5, 3), (9, 3), (5, 4),
        (3, 5), (6, 5), (8, 5), (2, 6),
        (4, 6), (6, 6), (7, 6), (0, 7),
        (1, 7), (3, 7), (4, 7), (6, 7),
        (1, 8), (3, 8), (6, 8), (7, 8),
        (0, 9), (2, 9), (8, 9)]  # Список координат препятствий
    for row, col in obstacles:  # Проходим по всем препятствиям
        grid[row][col].make_barrier()  # Помечаем ячейки как препятствия

    # Установка начальной и конечной точек
    start = grid[0][5]  # Устанавливаем начальную точку (0, 5)
    end = grid[9][9]    # Устанавливаем конечную точку (9, 9)
    start.make_start()  # Помечаем начальную точку
    end.make_end()  # Помечаем конечную точку

    # Обновление соседей для всех ячеек
    for row in grid:  # Проходим по всем строкам
        for cell in row:  # Проходим по всем ячейкам
            cell.update_neighbors(grid)  # Обновляем список соседей

    run = True  # Флаг для работы основного цикла
    started = False  # Флаг для запуска алгоритма

    while run:  # Основной цикл программы
        draw(WIN, grid)  # Отрисовываем текущее состояние
        for event in pygame.event.get():  # Проверяем события
            if event.type == pygame.QUIT:  # Если окно закрыто
                run = False  # Завершаем цикл

            if event.type == pygame.KEYDOWN:  # Обработка нажатий клавиш
                if event.key == pygame.K_SPACE and not started:  # Нажата клавиша пробела
                    started = True  # Запускаем алгоритм
                    a_star_algorithm(lambda: draw(WIN, grid), start, end)  # Выполняем A*
                if event.key == pygame.K_r:  # Нажата клавиша R
                    grid = make_grid(random_map=True)

                    start = grid[0][0]
                    end = grid[GRID_SIZE - 1][GRID_SIZE - 1]
                    start.reset()
                    end.reset()
                    start.make_start()
                    end.make_end()
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)
                    started = False
    pygame.quit()  # Завершаем Pygame


if __name__ == "__main__":
    main()