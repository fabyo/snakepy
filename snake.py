import pygame
import random
import sys

# =========================
# CONFIG
# =========================
WIDTH = 800
HEIGHT = 600
GRID = 20

INITIAL_FPS = 6
MAX_FPS = 25

# =========================
# CORES
# =========================
BG = (18, 18, 18)

SNAKE = (0, 255, 120)
HEAD = (0, 200, 255)

FOOD = (255, 70, 70)

TEXT = (240, 240, 240)

GRID_COLOR = (30, 30, 30)

# =========================
# INIT
# =========================
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 28)
big_font = pygame.font.SysFont("consolas", 52)

# =========================
# FUNÇÕES
# =========================
def random_food():
    x = random.randint(0, (WIDTH // GRID) - 1) * GRID
    y = random.randint(0, (HEIGHT // GRID) - 1) * GRID

    return [x, y]


def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def reset_game():

    snake = [
        [200, 200],
        [180, 200],
        [160, 200]
    ]

    direction = "RIGHT"

    food = random_food()

    score = 0

    return snake, direction, food, score


# =========================
# GAME STATE
# =========================
snake, direction, food, score = reset_game()

running = True
game_over = False

# =========================
# LOOP PRINCIPAL
# =========================
while running:

    # =====================
    # VELOCIDADE DINÂMICA
    # =====================
    current_fps = min(
        INITIAL_FPS + (score * 0.5),
        MAX_FPS
    )

    clock.tick(current_fps)

    # =====================
    # EVENTOS
    # =====================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # RESTART
            if game_over and event.key == pygame.K_r:

                snake, direction, food, score = reset_game()

                game_over = False

            # MOVIMENTO
            if not game_over:

                if event.key in [pygame.K_UP, pygame.K_w]:

                    if direction != "DOWN":
                        direction = "UP"

                elif event.key in [pygame.K_DOWN, pygame.K_s]:

                    if direction != "UP":
                        direction = "DOWN"

                elif event.key in [pygame.K_LEFT, pygame.K_a]:

                    if direction != "RIGHT":
                        direction = "LEFT"

                elif event.key in [pygame.K_RIGHT, pygame.K_d]:

                    if direction != "LEFT":
                        direction = "RIGHT"

    # =====================
    # UPDATE
    # =====================
    if not game_over:

        head = snake[0].copy()

        # MOVIMENTO
        if direction == "UP":
            head[1] -= GRID

        elif direction == "DOWN":
            head[1] += GRID

        elif direction == "LEFT":
            head[0] -= GRID

        elif direction == "RIGHT":
            head[0] += GRID

        # COLISÃO PAREDE
        if (
            head[0] < 0 or
            head[0] >= WIDTH or
            head[1] < 0 or
            head[1] >= HEIGHT
        ):
            game_over = True

        # COLISÃO COM O CORPO
        if head in snake:
            game_over = True

        snake.insert(0, head)

        # COMIDA
        if head == food:

            score += 1

            while True:

                food = random_food()

                if food not in snake:
                    break

        else:
            snake.pop()

    # =====================
    # RENDER
    # =====================
    screen.fill(BG)

    # GRID
    for x in range(0, WIDTH, GRID):

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (x, 0),
            (x, HEIGHT)
        )

    for y in range(0, HEIGHT, GRID):

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (0, y),
            (WIDTH, y)
        )

    # COMIDA
    pygame.draw.rect(
        screen,
        FOOD,
        (food[0], food[1], GRID, GRID),
        border_radius=6
    )

    # COBRA
    for index, segment in enumerate(snake):

        color = HEAD if index == 0 else SNAKE

        pygame.draw.rect(
            screen,
            color,
            (segment[0], segment[1], GRID, GRID),
            border_radius=5
        )

    # SCORE
    draw_text(
        f"Score: {score}",
        font,
        TEXT,
        15,
        10
    )

    # VELOCIDADE
    draw_text(
        f"Velocidade: {int(current_fps)}",
        font,
        TEXT,
        15,
        45
    )

    # GAME OVER
    if game_over:

        overlay = pygame.Surface((WIDTH, HEIGHT))

        overlay.set_alpha(180)

        overlay.fill((0, 0, 0))

        screen.blit(overlay, (0, 0))

        game_over_text = big_font.render(
            "GAME OVER",
            True,
            (255, 80, 80)
        )

        restart_text = font.render(
            "Pressione R para reiniciar",
            True,
            TEXT
        )

        screen.blit(
            game_over_text,
            (
                WIDTH // 2 - game_over_text.get_width() // 2,
                HEIGHT // 2 - 80
            )
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 - restart_text.get_width() // 2,
                HEIGHT // 2
            )
        )

    pygame.display.flip()

# =========================
# EXIT
# =========================
pygame.quit()

sys.exit()