from random import randint

import pygame


# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)       # Цвет границы ячейки
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки
SPEED = 20

# Инициализация Pygame
pygame.init()
# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игры"""

    def __init__(self, body_color=(255, 255, 255), position=None):
        if position is None:
            position = (0, 0)
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Должен быть определен в подклассе"""
        raise NotImplementedError


class Apple(GameObject):
    """Класс описания яблока"""

    def __init__(self):
        super().__init__(APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """случайная позиция яблока на поле"""
        self.position = randint(0, GRID_WIDTH - 1), randint(0, GRID_HEIGHT - 1)

    def draw(self, surface):
        """Метод draw класса Apple"""
        rect = pygame.Rect(self.position[0] * GRID_SIZE,
                           self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        """нарисовать прямоугольную форму"""
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описания змейки"""

    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1

    def get_head_position(self):
        """возвращает позицию головы"""
        return self.positions[0]

    def update_direction(self, new_direction):
        """направление движения змейки"""
        if (new_direction[0] * -1, new_direction[1] * -1) == self.direction:
            return
        self.next_direction = new_direction

    def move(self):
        """перемещение змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
        head_x, head_y = self.get_head_position()
        new_x, new_y = head_x + self.direction[0], head_y + self.direction[1]
        new_x = (new_x + GRID_WIDTH) % GRID_WIDTH
        new_y = (new_y + GRID_HEIGHT) % GRID_HEIGHT

        new_head = (new_x, new_y)

        if new_head in self.positions:
            raise ValueError
        self.positions = [new_head] + self.positions[:-1]

    def grow(self):
        """увеличивает длину змейки"""
        self.positions.append(self.positions[-1])

    def reset(self):
        """сбрасывание в начальное состояние"""
        self.__init__()

    def draw(self, surface):
        """Метод draw класса Snake"""
        for pos in self.positions:
            rect = pygame.Rect(pos[0] * GRID_SIZE,
                               pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def handle_keys(snake):
    """изменение движения змейки клавишами"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
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
    """Главная функция для запуска игры 'Змейка'"""
    snake = Snake()
    apple = Apple()

    running = True
    while running:
        handle_keys(snake)
        try:
            snake.move()
        except ValueError:
            running = False
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(SPEED)
    pygame.quit()


# Убедимся, что функция main определена
if __name__ == "__main__":
    main()
