import pygame
from random import choice

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

CENTER_POSITION = (SCREEN_WIDTH // 2 // GRID_SIZE * GRID_SIZE,

                   SCREEN_HEIGHT // 2 // GRID_SIZE * GRID_SIZE)
ALL_POSITIONS = [(x * GRID_SIZE, y * GRID_SIZE)
                 for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)]
# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)  # Цвет границы ячейки
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
WHITE = (255, 255, 255)

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
        self.position = CENTER_POSITION
        self.body_color = body_color

    def draw(self, surface):
        """Должен быть определен в подклассе"""
        raise NotImplementedError


class Apple(GameObject):
    """Класс для описания яблока."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position([])  # Начальная позиция яблока

    def randomize_position(self, occupied_positions=[CENTER_POSITION]):
        """Устанавливает случайную позицию яблока."""
        available_positions = set(ALL_POSITIONS) - set(occupied_positions)
        self.position = choice(list(available_positions))

    def draw(self, surface):
        """Метод отрисовки яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для описания змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset()
        self.next_direction = None

    def reset(self):
        """Сбрасывает состояние змейки к первоначальному."""
        self.position = ((SCREEN_WIDTH // 2 // GRID_SIZE) * GRID_SIZE,
                         (SCREEN_HEIGHT // 2 // GRID_SIZE) * GRID_SIZE)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        current_head = self.get_head_position()
        new_head = (
            (current_head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (current_head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT)

        if new_head in self.positions:
            raise ValueError('Змейка врезалась в саму себя!')

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def grow(self):
        """Увеличивает длину змейки."""
        self.length += 1

    def draw(self, surface):
        """Метод отрисовки змейки."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция для запуска игры 'Змейка'"""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)

        try:
            snake.move()

        except ValueError:
            snake.reset()  # Сброс змейки в случае столкновения
        if snake.get_head_position() == apple.position:

            snake.grow()

            apple.randomize_position(snake.positions)
        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(SPEED)
    pygame.quit()


if __name__ == "__main__":
    main()  # Запуск игры
