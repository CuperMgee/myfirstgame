import pygame
import sys

pygame.init()

# 1. Параметры сетки и экрана
CELL_SIZE = 30       # Размер одной ячейки в пикселях
CELLS_X = 20         # Количество ячеек по ширине
CELLS_Y = 20         # Количество ячеек по высоте

WIDTH = CELLS_X * CELL_SIZE   # 600 px
HEIGHT = CELLS_Y * CELL_SIZE  # 600 px

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake — Урок 1: Движение по сетке")
clock = pygame.time.Clock()
FPS = 60

# Цвета
COLOR_BG = (22, 27, 34)
COLOR_GRID = (35, 43, 54)
COLOR_HEAD = (46, 204, 113)
COLOR_GLASS = (0, 0, 0)
COLOR_GLASS2 = (255, 255, 255)

# 2. Позиция головы змейки (хранится в координатах сетки, а не в пикселях)
snake_x = CELLS_X // 2
snake_y = CELLS_Y // 2

# Вектор направления (куда сейчас смотрит голова):
# (1, 0) - вправо, (-1, 0) - влево, (0, -1) - вверх, (0, 1) - вниз
direction_x = 1
direction_y = 0

# 3. Таймер такта движения змейки
# Создаем собственное событие, срабатывающее каждые 150 мс (~6.6 шагов в секунду)
STEP_EVENT = pygame.USEREVENT + 1
STEP_DELAY_MS = 150
pygame.time.set_timer(STEP_EVENT, STEP_DELAY_MS)

running = True
while running:
    # --- ЭТАП 1: Обработка событий ввода и таймера ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Одиночные нажатия: меняем вектор направления.
            # Защита от разворота на 180°: если двигаемся вправо, нажать "влево" нельзя
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction_y == 0:
                direction_x = 0
                direction_y = -1
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction_y == 0:
                direction_x = 0
                direction_y = 1
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction_x == 0:
                direction_x = -1
                direction_y = 0
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction_x == 0:
                direction_x = 1
                direction_y = 0
            if event.key == pygame.K_e or event.key == pygame.K_PLUS:
                STEP_DELAY_MS -= 20
                if STEP_DELAY_MS < 50:
                    STEP_DELAY_MS = 50
                pygame.time.set_timer(STEP_EVENT, STEP_DELAY_MS)

            if event.key == pygame.K_q or event.key == pygame.K_MINUS:
                STEP_DELAY_MS += 20
                pygame.time.set_timer(STEP_EVENT, STEP_DELAY_MS)

        # Такт времени: перемещаем голову ровно на 1 клетку вперед
        elif event.type == STEP_EVENT:
            snake_x += direction_x
            snake_y += direction_y

            # Временная проверка выхода за экран (зацикливание)
            snake_x %= CELLS_X
            snake_y %= CELLS_Y

    # --- ЭТАП 2: Отрисовка кадра ---
    screen.fill(COLOR_BG)

    # Рисуем сетку, чтобы студенты видели структуру ячеек
    for col in range(CELLS_X):
        x = col * CELL_SIZE
        pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, HEIGHT))
    for row in range(CELLS_Y):
        y = row * CELL_SIZE
        pygame.draw.line(screen, COLOR_GRID, (0, y), (WIDTH, y))

    # Перевод координат сетки в пиксели для отрисовки
    pixel_x = snake_x * CELL_SIZE
    pixel_y = snake_y * CELL_SIZE

    # Рисуем голову змейки с небольшим внутренним отступом (padding=2 px)
    head_rect = pygame.Rect(pixel_x + 2, pixel_y + 2, CELL_SIZE - 4, CELL_SIZE - 4)
    pygame.draw.rect(screen, COLOR_HEAD, head_rect, border_radius=5)

    if direction_x == 1:
        x1 = pixel_x + 20
        y1 = pixel_y + 10
        x2 = pixel_x + 20
        y2 = pixel_y + 20

    elif direction_x == -1:
        x1 = pixel_x + 10
        y1 = pixel_y + 10
        x2 = pixel_x + 10
        y2 = pixel_y + 20

    elif direction_y == -1:
        x1 = pixel_x + 10
        y1 = pixel_y + 10
        x2 = pixel_x + 20
        y2 = pixel_y + 10

    else:
        x1 = pixel_x + 10
        y1 = pixel_y + 20
        x2 = pixel_x + 20
        y2 = pixel_y + 20

    pygame.draw.circle(screen, (COLOR_GLASS2), (x1, y1), 4)
    pygame.draw.circle(screen, (COLOR_GLASS2), (x2, y2), 4)

    pygame.draw.circle(screen, (COLOR_GLASS), (x1, y1), 2)
    pygame.draw.circle(screen, (COLOR_GLASS), (x2, y2), 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()