from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Координаты центра:
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self) -> None:
        """Инициализирует базовые атрибуты объекта,
        такие как позиция и цвет.
        """
        self.position = SCREEN_CENTER
        self.body_color = None
        self.occupied_positions = None

    def draw(self):
        """Должен определять, как объект будет отрисовываться на экране."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко и действия c ним"""

    def __init__(self):
        """Задаёт цвет яблока и вызывает метод randomize_position."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position(self.occupied_positions)
        self.occupied_positions = None

    def randomize_position(self, occupied_positions):
        """Устанавливает случайное положение яблока на игровом поле."""
        if self.occupied_positions is None:
            self.occupied_positions = []
        while True:
            apple_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            apple_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.random_position = (apple_x, apple_y)
            if self.random_position not in self.occupied_positions:
                return self.random_position
                break

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [(self.position)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position = (new_head_x, new_head_y)
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        """Отрисовка головы змейки."""
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        """Затирание последнего сегмента."""
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
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
    """Описывает основной цикл игры."""
    pygame.init()
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        apple.draw()
        snake.draw()
        snake.move()
        handle_keys(snake)
        snake.update_direction()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)
        if snake.get_head_position() in snake.positions[2:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
        pygame.display.update()


if __name__ == '__main__':
    main()
