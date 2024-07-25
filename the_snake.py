from random import randint, choice
import pygame


# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Рассчитаем центр экрана
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)  # Цвет границы ячейки
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Константы для цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Скорость движения змейки
SPEED = 10

# Инициализация Pygame
pygame.init()
# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игры."""

    def __init__(self, body_color=WHITE):
        """Инициализирует базовые атрибуты объекта."""
        center_x = SCREEN_WIDTH // 2 // GRID_SIZE * GRID_SIZE
        center_y = SCREEN_HEIGHT // 2 // GRID_SIZE * GRID_SIZE
        self.position = (center_x, center_y)
        self.body_color = body_color

    def draw(self, surface):
        """Абстрактный метод для отрисовки объекта."""
        raise NotImplementedError(
            "Метод draw должен быть реализован в дочернем классе")


class Apple(GameObject):
    """Класс описания яблока."""

    def __init__(self):
        """Инициализирует атрибуты яблока."""
        super().__init__(body_color=APPLE_COLOR)
        # изначально позиция змейки неизвестна, передаем данные
        self.randomize_position([])

    def randomize_position(self, occupied_positions):
        """Устанавливает случайную позицию яблока."""
        while (new_position := (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )) in occupied_positions:
            continue

        self.position = new_position

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE,
                           GRID_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описания змейки."""

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def reset(self):
        """Сбрасывает состояние змейки к первоначальному."""
        center_x = SCREEN_WIDTH // 2 // GRID_SIZE * GRID_SIZE
        center_y = SCREEN_HEIGHT // 2 // GRID_SIZE * GRID_SIZE
        self.position = (center_x, center_y)
        self.length = 1
        self.positions = [self.position]
        # Змейка начинает движение в случайном направлении
        self.direction = choice(DIRECTIONS)
        self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Обновляет позицию змейки."""
        if self.next_direction:

            if (self.next_direction[0] * -1,
               self.next_direction[1] * -1) != self.direction:
                self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.get_head_position()
        new_x = (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        # Проверяем столкновение с собой
        if new_head in self.positions:
            self.reset()
        else:
            # Обновляем позиции змейки
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()

    def grow(self):
        """Увеличивает длину змейки."""
        self.length += 1

    def draw(self, surface):
        """Отрисовывает змейку на игровой поверхности."""
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def update_direction(self, direction):
        """Обновляет направление движения змейки."""
        self.next_direction = direction


def handle_keys():
    """Обрабатывает события клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)
    return True


def main():
    """Используем глобальные переменные"""
    global snake, apple
    snake = Snake()
    apple = Apple()

    running = True
    while running:
        running = handle_keys()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(SPEED)

    pygame.quit()


if __name__ == "__main__":
    main()
