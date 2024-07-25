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
BORDER_COLOR = (93, 216, 228)       # Цвет границы ячейки
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
    """Базовый класс для игры"""

    def __init__(self, body_color=None, position=None):
        """Инициализирует базовые атрибуты объекта"""
        if body_color is None:
            body_color = WHITE
        if position is None:
            position = CENTER_POSITION
        self.body_color = body_color
        self.position = position

    def draw(self, surface):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс описания яблока."""

    def __init__(self, body_color=APPLE_COLOR, position=None):
        """Инициализирует атрибуты яблока"""
        super().__init__(body_color, position)
        self.randomize_position()

    def randomize_position(self, occupied_positions=None):
        """Устанавливает случайную позицию яблока"""
        if occupied_positions is None:
            occupied_positions = [(CENTER_POSITION[0] // GRID_SIZE,
                                   CENTER_POSITION[1] // GRID_SIZE)]

        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE,
                           GRID_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описания змейки."""

    def __init__(self, body_color=SNAKE_COLOR, position=None):
        """Инициализирует начальное состояние змейки"""
        super().__init__(body_color,
                         (CENTER_POSITION[0] // GRID_SIZE * GRID_SIZE,
                          CENTER_POSITION[1] // GRID_SIZE * GRID_SIZE))
        self.length = 1
        self.positions = [self.position]
        self.direction = choice(DIRECTIONS)
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки"""
        if (new_direction[0] * -1, new_direction[1] * -1) == self.direction:
            return
        self.next_direction = new_direction

    def move(self):
        """Обновляет позицию змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
        head_x, head_y = self.get_head_position()
        new_x = (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT

        new_head = (new_x, new_y)

        if new_head in self.positions:
            raise ValueError

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def grow(self):
        """Увеличивает длину змейки."""
        self.length += 1

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние и
        выбирает случайное направление
        """
        self.length = 1
        self.position = (CENTER_POSITION[0] // GRID_SIZE * GRID_SIZE,
                         CENTER_POSITION[1] // GRID_SIZE * GRID_SIZE)
        self.positions = [self.position]
        self.direction = choice(DIRECTIONS)
        self.next_direction = None
        self.last = None

    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        if self.last is not None:
            last_rect = pygame.Rect(self.last[0], self.last[1],
                                    GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для изменения направления движения змейки"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(RIGHT)


def main():
    """Основной игровой цикл"""
    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        try:
            snake.move()
        except ValueError:
            snake.reset()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(SPEED)


if __name__ == "__main__":
    main()
