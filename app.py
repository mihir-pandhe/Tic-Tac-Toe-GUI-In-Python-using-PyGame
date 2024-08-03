import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)

board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]
player = 1
history = []
game_active = True


def draw_lines():
    screen.fill(BG_COLOR)
    pygame.draw.line(
        screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH
    )
    pygame.draw.line(
        screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH
    )
    pygame.draw.line(
        screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH
    )
    pygame.draw.line(
        screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH
    )


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(
                    screen,
                    CIRCLE_COLOR,
                    (
                        int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                        int(row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    ),
                    CIRCLE_RADIUS,
                    CIRCLE_WIDTH,
                )
            elif board[row][col] == 2:
                pygame.draw.line(
                    screen,
                    CROSS_COLOR,
                    (
                        col * SQUARE_SIZE + SPACE,
                        row * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                    ),
                    (
                        col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                        row * SQUARE_SIZE + SPACE,
                    ),
                    CROSS_WIDTH,
                )
                pygame.draw.line(
                    screen,
                    CROSS_COLOR,
                    (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                    (
                        col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                        row * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                    ),
                    CROSS_WIDTH,
                )


def draw_message(message, restart=False):
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    text = font.render(message, True, TEXT_COLOR)
    screen.blit(
        text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2)
    )

    if restart:
        restart_text = small_font.render(
            "Press R to Restart or Q to Quit", True, TEXT_COLOR
        )
        screen.blit(
            restart_text,
            (
                WIDTH // 2 - restart_text.get_width() // 2,
                HEIGHT // 2 + text.get_height(),
            ),
        )

    pygame.display.update()


def draw_start_screen():
    screen.fill(BG_COLOR)
    title = font.render("Tic Tac Toe", True, TEXT_COLOR)
    start_button = small_font.render("Press Enter to Start", True, TEXT_COLOR)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
    screen.blit(start_button, (WIDTH // 2 - start_button.get_width() // 2, HEIGHT // 2))
    pygame.display.update()


def draw_game_over_animation():
    for _ in range(3):
        screen.fill(BG_COLOR)
        draw_lines()
        draw_figures()
        pygame.display.update()
        pygame.time.wait(500)
        screen.fill(BG_COLOR)
        pygame.display.update()
        pygame.time.wait(500)


def mark_square(row, col, player):
    if board[row][col] == 0:
        board[row][col] = player
        history.append((row, col, player))


def undo_move():
    if history:
        row, col, player = history.pop()
        board[row][col] = 0


def available_square(row, col):
    return board[row][col] == 0


def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True


def check_win(player):
    for col in range(BOARD_COLS):
        if (
            board[0][col] == player
            and board[1][col] == player
            and board[2][col] == player
        ):
            return True
    for row in range(BOARD_ROWS):
        if (
            board[row][0] == player
            and board[row][1] == player
            and board[row][2] == player
        ):
            return True
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    return False


def reset_game():
    global player, history, game_active
    board[:] = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]
    history.clear()
    player = 1
    game_active = True


draw_start_screen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_active = True
                reset_game()
                draw_lines()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and game_active:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                draw_lines()
                draw_figures()

                if check_win(player):
                    draw_game_over_animation()
                    draw_message(f"Player {player} wins!", restart=True)
                    game_active = False
                elif is_board_full():
                    draw_message("It's a draw!", restart=True)
                    game_active = False

                player = player % 2 + 1
            else:
                draw_message("Invalid Move!")

        if not game_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                reset_game()
                draw_lines()
            elif keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

    pygame.display.update()
