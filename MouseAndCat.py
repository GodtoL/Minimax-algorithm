import random
import time

# Creación del tablero
board_size = 10
board = [["." for x in range(board_size)] for x in range(board_size)]

# Definimos las posiciones
numbers = list(range(board_size))

hideout_position = (0, 0)
main_couch_position = ((2 , 2) , (2 , 3) , (2 , 4) , (2 , 5) , (3 , 2) , (3 , 3) , (3 , 4) , (3 , 5))
couch1_position = ((4 , 7) , (5 , 7))
couch2_position = ((4 , 1) , (5 , 1))
tv_position = ((8, 3) , (8 , 4) , (8 , 5))
all_obstacles = set(main_couch_position + couch1_position + couch2_position + tv_position + (hideout_position,))

# Función para evaluar la distancia entre posiciones
def evaluate(cat_position, mouse_position, hideout_position):
    
    # Calculamos distancias
    distance_to_cat = abs(cat_position[0] - mouse_position[0]) + abs(cat_position[1] - mouse_position[1])
    distance_to_hideout = abs(hideout_position[0] - mouse_position[0]) + abs(hideout_position[1] - mouse_position[1])
    
    # Considera la distancia al gato y a la guarida
    return distance_to_cat - 0.6 * distance_to_hideout

# Función para definir las distancias entre el ratón y el escondite, y entre la del gato y el raton
def initial_positions(hideout_position , all_obstacles):
    
    mouse_initial_position = (random.choice(numbers), random.choice(numbers))
    cat_initial_position = (random.choice(numbers), random.choice(numbers))
    distance_to_cat = abs(cat_initial_position[0] - mouse_initial_position[0]) + abs(cat_initial_position[1] - mouse_initial_position[1])
    distance_to_hideout = abs(hideout_position[0] - mouse_initial_position[0]) + abs(hideout_position[1] - mouse_initial_position[1])

    while (distance_to_cat < 3 and
       distance_to_hideout < 4 and
       cat_initial_position == hideout_position and
       cat_initial_position in all_obstacles):
    
        mouse_initial_position = (random.choice(numbers), random.choice(numbers))
        cat_initial_position = (random.choice(numbers), random.choice(numbers))

        distance_to_cat = abs(cat_initial_position[0] - mouse_initial_position[0]) + abs(cat_initial_position[1] - mouse_initial_position[1])
        distance_to_hideout = abs(hideout_position[0] - mouse_initial_position[0]) + abs(hideout_position[1] - mouse_initial_position[1])
    
    
    return mouse_initial_position , cat_initial_position
    
# Función para crear la tabla
def create_table(board):

    for row in board:
        print("  ".join(row))
    print()

# Función para actualizar el tablero
def update_board(board, cat_position, mouse_position):
    
    for x in range(board_size):
        for y in range(board_size):
            board[x][y] = "."

    # Ubicamos los elementos en el tablero        
    for position in main_couch_position:
        board[position[0]][position[1]] = "S"
    
    for position in couch1_position:
        board[position[0]][position[1]] = "1"
    
    for position in couch2_position:
        board[position[0]][position[1]] = "2"
    
    for position in tv_position:
        board[position[0]][position[1]] = "T"
    
    board[cat_position[0]][cat_position[1]] = 'G'
    board[mouse_position[0]][mouse_position[1]] = 'R'
    board[hideout_position[0]][hideout_position[1]] = 'E'

    # Llamamos a la función que pasa el tablero "en limpio"
    create_table(board)

# Consigue todos los posibles movimientos del ratón
def get_possible_mouse_moves(position, board_size):

    x, y = position
    
    moves = []

    if x > 0: moves.append((x-1, y))  # arriba
    if x < board_size - 1: moves.append((x+1, y))  # abajo
    if y > 0: moves.append((x, y-1))  # izquierda
    if y < board_size - 1: moves.append((x, y+1))  # derecha
    return moves

# Consigue todos los posibles movimientos del gato
def get_possible_cat_moves(position, board_size):
  
    x, y = position
    moves = []

    # Un movimiento
    if x > 0: moves.append((x-1, y))  # arriba
    if x < board_size - 1: moves.append((x+1, y))  #abajo
    if y > 0: moves.append((x, y-1)) # izquierda
    if y < board_size - 1: moves.append((x, y+1)) # derecha

    # Doble movimiento
    if x > 1: moves.append((x-2, y))  # dos veces arriba
    if x < board_size - 2: moves.append((x+2, y))  # dos veces abajo
    if y > 1: moves.append((x, y-2))   # dos veces izquierda
    if y < board_size - 2: moves.append((x, y+2))  # dos veces derecha

    # Filtramos los movimientos
    moves = [move for move in moves if move not in all_obstacles]

    return moves

# Función Minimax
def minimax(cat_position, mouse_position, depth, is_cat_turn, board_size, hideout_position):

    # El caso base
    if depth == 0 or cat_position == mouse_position or mouse_position == hideout_position:
        return evaluate(cat_position, mouse_position, hideout_position)
    
    # El turno del gato
    if is_cat_turn:

        best_value = float('inf')

        for move in get_possible_cat_moves(cat_position, board_size):

            value = minimax(move, mouse_position, depth-1, False, board_size, hideout_position)

            best_value = min(best_value, value)
        return best_value
    else:

        best_value = float('-inf')
  
        for move in get_possible_mouse_moves(mouse_position, board_size):
       
            value = minimax(cat_position, move, depth-1, True, board_size, hideout_position)

            best_value = max(best_value, value)
        return best_value

# Mover el ratón 
def move_mouse_intelligently(cat_position, mouse_position, board_size):

    best_move = None
    best_value = float('-inf')

    for move in get_possible_mouse_moves(mouse_position, board_size):

        value = minimax(cat_position, move, 5, True, board_size, hideout_position)

        if value > best_value:
            best_value = value
            best_move = move
    return best_move

# Mover el gato inteligentemente
def move_cat_intelligently(cat_position, mouse_position, board_size):

    best_move = None
    best_value = float('inf')

    for move in get_possible_cat_moves(cat_position, board_size):

        value = minimax(move, mouse_position, 5, False, board_size, hideout_position)

        if value < best_value:
            best_value = value
            best_move = move
    return best_move

mouse_position , cat_position = initial_positions(hideout_position , all_obstacles)


# Tiempo de espera por cada turno
time_to_sleep = 1

All_moves = []
End = False

# Bucle principal del juego
while True:

    update_board(board, cat_position, mouse_position)
    
    # Turno del ratón
    mouse_position = move_mouse_intelligently(cat_position, mouse_position, board_size)
    update_board(board, cat_position, mouse_position)
    All_moves.append(mouse_position)

    if cat_position == mouse_position:
        print("El gato atrapó al ratón!")
        break

    if mouse_position == hideout_position:
        print("El ratón logró escapar!")
        break

    # Se espera time_to_sleep para el siguiente turno
    time.sleep(time_to_sleep)

    # Turno del gato
    cat_position = move_cat_intelligently(cat_position, mouse_position, board_size)
    update_board(board, cat_position, mouse_position)
    All_moves.append(mouse_position)

    if cat_position == mouse_position:
        print("El gato atrapó al ratón!")
        break

    if mouse_position == hideout_position:
        print("El ratón logró escapar!")
        break

    # Impedir bucle infinito
    if len(All_moves) > 10:
        All_moves.pop(0)
        filt = {}
        for mov in All_moves:
            if mov in filt:
                filt[mov] += 1

            else: 
                filt[mov] = 1

            if filt[mov] > 5:
                print("Empate")
                End = True
                break
    if End:
        break          
            
            
    time.sleep(time_to_sleep)