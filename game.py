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
GRID_SIZE = 400  # Tamaño fijo de la cuadrícula
TOP_MARGIN = 40
BOTTOM_MARGIN = 50
WIDTH = GRID_SIZE
HEIGHT = GRID_SIZE + TOP_MARGIN + BOTTOM_MARGIN  # Ajusta la ventana para márgenes
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = GRID_SIZE // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

# Dimensiones de la ventana de juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
icono = pygame.image.load("assets/penguin.svg")
pygame.display.set_icon(icono)
pygame.display.set_caption("Tres en ralla - Andy")
screen.fill(BLACK)

# Tamaño del tablero de juego
board = np.zeros((BOARD_ROWS, BOARD_COLS))


# Menú de selección de dificultad
def select_dificulty():
    font = pygame.font.SysFont(None, 45)
    colores_dificultad = {
        "1 - Fácil": (0, 200, 0),        # Verde
        "2 - Normal": (255, 215, 0),     # Amarillo
        "3 - Difícil": (255, 140, 0),    # Naranja
        "4 - Imposible": (220, 0, 0),    # Rojo
    }
    screen.fill(BLACK)
    opciones = [
        "Selecciona dificultad:",
        "1 - Fácil",
        "2 - Normal",
        "3 - Difícil",
        "4 - Imposible",
    ]
    # Centrado vertical
    total_height = len(opciones) * 45
    start_y = (HEIGHT - total_height) // 2
    for i, texto in enumerate(opciones):
        color = WHITE if i == 0 else colores_dificultad.get(texto, WHITE)
        img = font.render(texto, True, color)
        img_rect = img.get_rect()
        img_rect.x = 40
        img_rect.y = start_y + i * 45
        screen.blit(img, img_rect)
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
            screen,
            color,
            (0, TOP_MARGIN + SQUARE_SIZE * i),
            (WIDTH, TOP_MARGIN + SQUARE_SIZE * i),
            LINE_WIDTH,
        )
        pygame.draw.line(
            screen,
            color,
            (SQUARE_SIZE * i, TOP_MARGIN),
            (SQUARE_SIZE * i, TOP_MARGIN + GRID_SIZE),
            LINE_WIDTH,
        )


# Función para dibujar las distintas figuras de juego
def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            center_x = int(col * SQUARE_SIZE + SQUARE_SIZE // 2)
            center_y = int(TOP_MARGIN + row * SQUARE_SIZE + SQUARE_SIZE // 2)
            if board[row][col] == 1:
                pygame.draw.circle(
                    screen,
                    color,
                    (center_x, center_y),
                    CIRCLE_RADIUS,
                    CIRCLE_WIDTH,
                )
            elif board[row][col] == 2:
                pygame.draw.line(
                    screen,
                    color,
                    (
                        col * SQUARE_SIZE + SQUARE_SIZE // 4,
                        TOP_MARGIN + row * SQUARE_SIZE + SQUARE_SIZE // 4,
                    ),
                    (
                        col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                        TOP_MARGIN + row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                    ),
                    CROSS_WIDTH,
                )
                pygame.draw.line(
                    screen,
                    color,
                    (
                        col * SQUARE_SIZE + SQUARE_SIZE // 4,
                        TOP_MARGIN + row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                    ),
                    (
                        col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4,
                        TOP_MARGIN + row * SQUARE_SIZE + SQUARE_SIZE // 4,
                    ),
                    CROSS_WIDTH,
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
            empty = [
                (row, col)
                for row in range(BOARD_ROWS)
                for col in range(BOARD_COLS)
                if board[row][col] == 0
            ]
            if empty:
                move = random.choice(empty)
                mark_square(move[0], move[1], 2)
                return True
            return False
    elif dificultad == "normal":
        # 40% aleatorio, 60% perfecto
        if random.random() < 0.4:
            empty = [
                (row, col)
                for row in range(BOARD_ROWS)
                for col in range(BOARD_COLS)
                if board[row][col] == 0
            ]
            if empty:
                move = random.choice(empty)
                mark_square(move[0], move[1], 2)
                return True
            return False
    elif dificultad == "dificil":
        # 10% aleatorio, 90% perfecto
        if random.random() < 0.1:
            empty = [
                (row, col)
                for row in range(BOARD_ROWS)
                for col in range(BOARD_COLS)
                if board[row][col] == 0
            ]
            if empty:
                move = random.choice(empty)
                mark_square(move[0], move[1], 2)
                return True
            return False
    # Imposible: juega perfecto
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


# Contadores de victorias
victorias_jugador = 0
victorias_ia = 0
empates = 0


# Función que muestra las victorias de cada jugador en la parte superiro de la pantalla
def mostrar_contadores():
    font = pygame.font.SysFont(None, 28)
    texto = f"Jugador: {victorias_jugador}  |  IA: {victorias_ia}  |  Empates: {empates}"
    img = font.render(texto, True, WHITE)
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, TOP_MARGIN))
    img_rect = img.get_rect(center=(WIDTH // 2, TOP_MARGIN // 2 + 5))
    screen.blit(img, img_rect)


# Función que muestra los controles y la dificultad actual
def mostrar_atajos(dificultad):
    font = pygame.font.SysFont(None, 25)
    colores_dificultad = {
        "facil": (0, 200, 0),        # Verde
        "normal": (255, 215, 0),     # Amarillo
        "dificil": (255, 140, 0),    # Naranja
        "imposible": (220, 0, 0),    # Rojo
    }
    color = colores_dificultad.get(dificultad, GRAY)
    texto_dificultad = f"Dificultad actual: {dificultad.capitalize()}"
    img_dificultad = font.render(texto_dificultad, True, color)
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - BOTTOM_MARGIN, WIDTH, BOTTOM_MARGIN))
    screen.blit(img_dificultad, (10, HEIGHT - BOTTOM_MARGIN + 5))
    # Mostrar atajos debajo
    texto_atajos = "ESC: Volver atrás    R: Reiniciar"
    img_atajos = font.render(texto_atajos, True, GRAY)
    screen.blit(img_atajos, (10, HEIGHT - BOTTOM_MARGIN + 27))

# Función para reiniciar la partida
def restart_game():
    screen.fill(BLACK)
    draw_lines()
    mostrar_contadores()
    mostrar_atajos(dificultad)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0


# Preparación de la partida
dificultad = select_dificulty()
screen.fill(BLACK)
draw_lines()
mostrar_contadores()
mostrar_atajos(dificultad)

player = 1
game_over = False

# Bucle del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == 1:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = (event.pos[1] - TOP_MARGIN) // SQUARE_SIZE
            if 0 <= mouseY < BOARD_ROWS and 0 <= mouseX < BOARD_COLS and TOP_MARGIN <= event.pos[1] < TOP_MARGIN + GRID_SIZE:
                if avaliable_square(mouseY, mouseX):
                    mark_square(mouseY, mouseX, player)
                    if check_win(player):
                        game_over = True
                        victorias_jugador += 1
                    else:
                        player = 2

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1

            if event.key == pygame.K_ESCAPE:
                dificultad = select_dificulty()
                restart_game()
                game_over = False
                player = 1

    if not game_over and player == 2:
        pygame.time.wait(100)
        if best_move(dificultad):
            if check_win(2):
                game_over = True
                victorias_ia += 1
            else:
                player = 1

        if not game_over and is_board_full():
            empates += 1
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
        mostrar_contadores()
        mostrar_atajos(dificultad)

    pygame.display.update()