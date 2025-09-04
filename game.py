import sys
import pygame
import numpy as np
import random

pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Proporciones y tamaños
WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

# Dimensiones de la ventana de juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
icono = pygame.image.load("assets/penguin.svg")
pygame.display.set_icon(icono)
pygame.display.set_caption("Tres en ralla vs AI")
screen.fill(BLACK)

# Tamaño del tablero de juego
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Menú de selección de dificultad
def select_dificulty():
    font = pygame.font.SysFont(None, 32)
    screen.fill(BLACK)
    opciones = [
        "Selecciona dificultad:",
        "1 - Fácil",
        "2 - Normal",
        "3 - Difícil",
        "4 - Imposible"
    ]
    for i, texto in enumerate(opciones):
        img = font.render(texto, True, WHITE)
        screen.blit(img, (40, 60 + i * 40))
    pygame.display.update()

    dificultad = None
    while dificultad is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    dificultad = "facil"
                elif event.key == pygame.K_2:
                    dificultad = "normal"
                elif event.key == pygame.K_3:
                    dificultad = "dificil"
                elif event.key == pygame.K_4:
                    dificultad = "imposible"
    return dificultad

# Función para definir las lineas del tablero
def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(
            screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH
        )
        pygame.draw.line(
            screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH
        )

# Función para dibujar las distintas figuras de juego
def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(
                    screen,
                    color,
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
                    color,
                    (
                        col * SQUARE_SIZE + SQUARE_SIZE // 4,
                        row * SQUARE_SIZE + SQUARE_SIZE // 4,
                    ),
                    (
                        col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                        row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                    ), CROSS_WIDTH
                )
                pygame.draw.line(
                    screen,
                    color,
                    (
                        col * SQUARE_SIZE + SQUARE_SIZE // 4,
                        row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                    ),
                    (
                        col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                        row * SQUARE_SIZE + SQUARE_SIZE // 4,
                    ), CROSS_WIDTH
                )

# Función para elegir posición
def mark_square(row, col, player):
    board[row][col] = player


# Función para saber si hay algún hueco vacio
def avaliable_square(row, col):
    return board[row][col] == 0


# Función para determinar si el tablero esta lleno
def is_board_full(check_board=board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True


# Función para reiniciar la partida
def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                board[row][col] = 0


# Función para determinar si alguien ha ganado
def check_win(player, check_board=board):
    for col in range(BOARD_COLS):
        if (
            check_board[0][col] == player
            and check_board[1][col] == player
            and check_board[2][col] == player
        ):
            return True

    for row in range(BOARD_ROWS):
        if (
            check_board[row][0] == player
            and check_board[row][1] == player
            and check_board[row][2] == player
        ):
            return True

    if (
        check_board[0][0] == player
        and check_board[1][1] == player
        and check_board[2][2] == player
    ):
        return True

    if (
        check_board[0][2] == player
        and check_board[1][1] == player
        and check_board[2][0] == player
    ):
        return True

    return False


# Algoritmo minimax para IA
def minimax(minimax_board, depth, is_maximazing):
    if check_win(2, minimax_board):
        return float("inf")
    elif check_win(1, minimax_board):
        return float("-inf")
    elif is_board_full(minimax_board):
        return 0
    
    if is_maximazing:
        best_score = -1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

# Función para determinar el mejor movimiento para la IA
def best_move(dificultad):
    if dificultad == "facil":
        # 70% aleatorio, 30% perfecto
        if random.random() < 0.7:
            empty = [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] == 0]
            if empty:
                move = random.choice(empty)
                mark_square(move[0], move[1], 2)
                return True
            return False
    elif dificultad == "normal":
        # 40% aleatorio, 60% perfecto
        if random.random() < 0.4:
            empty = [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] == 0]
            if empty:
                move = random.choice(empty)
                mark_square(move[0], move[1], 2)
                return True
            return False
    elif dificultad == "dificil":
        # 10% aleatorio, 90% perfecto
        if random.random() < 0.1:
            empty = [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] == 0]
            if empty:
                move = random.choice(empty)
                mark_square(move[0], move[1], 2)
                return True
            return False
    # imposible: juega perfecto
    best_score = -1000
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False
                

# Preparación de la partida
dificultad = select_dificulty()
screen.fill(BLACK)
draw_lines()

player = 1
game_over = False

# Bucle del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == 1:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE
            
            if avaliable_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True
                else:
                    player = 2  # Cambia al turno de la IA

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                dificultad = select_dificulty()
                restart_game()
                game_over = False
                player = 1
                
    # Turno de la IA (jugador 2)
    if not game_over and player == 2:
        pygame.time.wait(100)  # Pequeña pausa para que se vea la jugada
        if best_move(dificultad):
            if check_win(2):
                game_over = True
            else:
                player = 1  # Vuelve el turno al jugador

        if not game_over and is_board_full():
            game_over = True

    if not game_over:
        draw_figures()
    else:
        if check_win(1):
            draw_figures(GREEN)
            draw_lines(GREEN)
        elif check_win(2):
            draw_figures(RED)
            draw_lines(RED)
        else:
            draw_figures(GRAY)
            draw_lines(GRAY)
    
    pygame.display.update()