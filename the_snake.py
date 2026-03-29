from random import randint

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

# Цвет фона — чёрный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    '''
    Основной клас.
    '''
    
    def __init__(self, position=(0, 0), body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        pass

class Apple(GameObject):
    '''Описываем яблоко'''
    
    body_color = APPLE_COLOR

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        '''Генерирует случайную позицию для яблока.'''
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    '''Описываем змейку'''
    
    body_color = SNAKE_COLOR

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        # Начальная позиция змейки (центр поля)
        center = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)
        self.positions = [center]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None  # Последний сегмент для удаления

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, ate_food=False):
        '''Получаем текущее положение головы и смещаем на клетку в нужном направлении'''
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE)

        # Проверка выхода за границы
        if (new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or
            new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT):
            return False

        # Проверка столкновения с собой
        if new_head in self.positions:
            return False

        # Сохраняем последний сегмент для удаления при отрисовке
        self.last = self.positions[-1]

        # Добавляем новую голову
        self.positions.insert(0, new_head)

        # Если не съели еду, удаляем хвост
        if not ate_food:
            self.positions.pop()

        return True

    def get_head_position(self):
        '''Возвращаем позицию головы'''
        return self.positions[0]

    def reset(self):
        '''При активации сбрасываем настройки в начало'''
        center = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)
        self.positions = [center]
        self.direction = RIGHT
        self.next_direction = None

    def draw(self):
        # Затираем последний сегмент
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        # Отрисовка сегментов змейки
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(snake):
    '''Проверка нажатия клавиш'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        # Обновление направления
        snake.update_direction()

        # Проверяем, съела ли змейка яблоко
        ate_food = snake.get_head_position() == apple.position

        # Перемещение змейки
        if not snake.move(ate_food):
            # Игра окончена — перезапускаем
            snake.reset()
            apple.randomize_position()

        # Если змейка съела яблоко, генерируем новое
        if ate_food:
            apple.randomize_position()
            # Убедимся, что яблоко не появилось на змейке
            while apple.position in snake.positions:
                apple.randomize_position()

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
