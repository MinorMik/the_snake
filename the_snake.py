from random import randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Основной класс."""

    def __init__(self, position=(0, 0), body_color=None) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Заглушка для методов дочерних классов."""


class Apple(GameObject):
    """Описывает яблоко."""

    def __init__(self) -> None:
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position([CENTER])

    def randomize_position(self, used_position) -> None:
        """Генерирует случайную позицию для яблока."""
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if position not in used_position:
                self.position = position
                return

    def draw(self) -> None:
        """Отрисовка яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описывает змейку."""

    def __init__(self) -> None:
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
        self.last = None  # Последний сегмент для удаления
        self.length = 1

    def update_direction(self, next_direction) -> None:
        """Определяем направление."""
        if next_direction:
            self.direction = next_direction

    def move(self) -> None:
        """
        Сдвигает положение головы в пределах экрана
        по заданному направлению.
        """
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        # Получаем новые координаты в границах экрана
        new_head_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        # Сохраняем координаты в начало змейки
        self.positions.insert(0, (new_head_x, new_head_y))
        # Если не съели яблоко - удаляем хвост.
        if self.length < len(self.positions):
            self.last = self.positions.pop()

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы."""
        return self.positions[0]

    def reset(self) -> None:
        """При активации сбрасывает настройки в начало."""
        self.positions = [CENTER]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self) -> None:
        """Отрисовка змейки."""
        # Затираем последний сегмент
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        # Отрисовка сегментов змейки
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(snake) -> tuple[int, int] | None:
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                return UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                return DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                return LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                return RIGHT
            else:
                return None


def main() -> None:
    """Запускает основной игровой цикл."""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        move_direction = handle_keys(snake)

        # Обновление направления
        snake.update_direction(move_direction)

        # Перемещение змейки
        snake.move()

        # Проверяем, съела ли змейка яблоко
        ate_food = snake.get_head_position() == apple.position

        # Если змейка съела яблоко, генерируем новое
        # и увеличиваем длину змейки.
        if ate_food:
            apple.randomize_position(snake.positions)
            snake.length += 1

        # Игра окончена — перезапускаем
        if (snake.length == GRID_SIZE ** 2
                or snake.get_head_position() in snake.positions[1:]):
            snake.reset()
            apple.randomize_position(snake.positions)

        # Отрисовка
        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
