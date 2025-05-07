import copy
import time

from tictactoe import TicTacToe

def minimax_alpha_beta(game, depth, maximizing, k, alpha, beta, node_counter):
    """
    Implementación de minimax con alpha-beta pruning para optimizar la búsqueda.
    
    Args:
        game: Objeto del juego TicTacToe
        depth: Profundidad actual en el árbol de búsqueda
        maximizing: Booleano que indica si es turno del jugador maximizador (X)
        k: Profundidad máxima de búsqueda
        alpha: Mejor valor para el maximizador hasta el momento
        beta: Mejor valor para el minimizador hasta el momento
        node_counter: Contador de nodos explorados [contador]
    
    Returns:
        (valor de evaluación, mejor movimiento)
    """
    node_counter[0] += 1

    # Caso base: nodo terminal o profundidad máxima alcanzada
    if game.is_terminal() or depth == k:
        return game.utility() if game.is_terminal() else game.heuristic(), None

    best_move = None
    
    if maximizing:
        # Jugador maximizador (X)
        max_eval = float('-inf')
        for move in game.available_moves():
            new_game = copy.deepcopy(game)
            new_game.make_move(move, 'X')
            eval, _ = minimax_alpha_beta(new_game, depth+1, False, k, alpha, beta, node_counter)
            
            if eval > max_eval:
                max_eval = eval
                best_move = move
                
            # Actualizar alpha
            alpha = max(alpha, eval)
            
            # Poda beta: si alpha >= beta, podemos podar el resto de ramas
            if alpha >= beta:
                break
                
        return max_eval, best_move
    else:
        # Jugador minimizador (O)
        min_eval = float('inf')
        for move in game.available_moves():
            new_game = copy.deepcopy(game)
            new_game.make_move(move, 'O')
            eval, _ = minimax_alpha_beta(new_game, depth+1, True, k, alpha, beta, node_counter)
            
            if eval < min_eval:
                min_eval = eval
                best_move = move
                
            # Actualizar beta
            beta = min(beta, eval)
            
            # Poda alpha: si beta <= alpha, podamos el resto de ramas
            if beta <= alpha:
                break
                
        return min_eval, best_move

def get_best_move_alpha_beta(game, player, k):
    """
    Obtiene el mejor movimiento usando minimax con alpha-beta pruning
    
    Args:
        game: Estado actual del juego
        player: Jugador actual ('X' o 'O')
        k: Profundidad máxima de búsqueda
    
    Returns:
        (mejor movimiento, número de nodos explorados)
    """
    node_counter = [0]  # Lista para poder modificar el contador desde las funciones
    
    # Inicializamos alpha y beta con sus valores extremos
    alpha = float('-inf')
    beta = float('inf')
    
    # Determinamos si es turno del maximizador o minimizador basado en el jugador actual
    is_maximizing = player == 'X'
    
    _, best_move = minimax_alpha_beta(game, 0, is_maximizing, k, alpha, beta, node_counter)
    
    return best_move, node_counter[0]

def play_sample_game(k=3):
    """
    Juega un juego de ejemplo usando alpha-beta pruning
    """
    print("Iniciando juego de muestra con alpha-beta pruning (k={})".format(k))
    game = TicTacToe()
    turn = 1
    current_player = 'X'  # X comienza primero
    
    while not game.is_terminal():
        print(f"\nTurno {turn} - Jugador: {current_player}")
        game.print_board()
        
        # Obtener mejor movimiento con alpha-beta pruning
        move, nodes = get_best_move_alpha_beta(game, current_player, k)
        print(f"Movimiento elegido: {move} (explorados {nodes} nodos)")
        
        # Ejecutar movimiento
        game.make_move(move, current_player)
        
        # Cambiar jugador
        current_player = 'O' if current_player == 'X' else 'X'
        turn += 1
    
    # Mostrar estado final
    print("\nJuego terminado!")
    game.print_board()
    winner = game.check_winner()
    if winner == 'Draw':
        print("Resultado: Empate")
    else:
        print(f"Ganador: Jugador {winner}")

def run_experiments(n_experiments=1000, k=2, startPlayer = 'X'):
    """
    Ejecuta experimentos para comparar minimax original vs alpha-beta pruning
    
    Args:
        n_experiments: Número de experimentos a realizar
        k: Profundidad máxima de búsqueda
    
    Returns:
        Estadísticas de los experimentos
    """
    pruning_nodes_total = 0
    total_time = 0  # <-- acumulador de tiempo
    results_pruning = {"X_wins": 0, "O_wins": 0, "draws": 0}
    
    for i in range(n_experiments):
        # Experimento con alpha-beta pruning
        game_pruning = TicTacToe()
        pruning_nodes_game = 0
        current_player = startPlayer

        start_time = time.time()  # << comienzo del reloj
        
        while not game_pruning.is_terminal():
            move, nodes = get_best_move_alpha_beta(game_pruning, current_player, k)
            pruning_nodes_game += nodes
            game_pruning.make_move(move, current_player)
            current_player = 'O' if current_player == 'X' else 'X'
            
        end_time = time.time()  # << fin del reloj
        total_time += (end_time - start_time)  # acumulamos el tiempo del juego

        # Registrar resultado
        winner = game_pruning.check_winner()
        if winner == 'X':
            results_pruning["X_wins"] += 1
        elif winner == 'O':
            results_pruning["O_wins"] += 1
        else:
            results_pruning["draws"] += 1
            
        pruning_nodes_total += pruning_nodes_game
    
    # Calcular estadísticas
    stats = {
        "pruning": {
            "results": results_pruning,
            "avg_nodes_per_game": pruning_nodes_total / n_experiments,
            "avg_time_per_game": total_time / n_experiments
        }
    }
    
    # Imprimir resultados
    print("\n===== RESULTADOS DE LOS EXPERIMENTOS =====")
    print(f"Número de experimentos: {n_experiments}")
    print(f"Profundidad de búsqueda (k): {k}")
    print(f"Jugador inicial: {startPlayer}")
    
    print("\nMinimax con Alpha-Beta Pruning:")
    print(f"  - Victorias X: {results_pruning['X_wins']}")
    print(f"  - Empates: {results_pruning['draws']}")
    print(f"  - Victorias O: {results_pruning['O_wins']}")
    print(f"  - Nodos explorados (promedio por juego): {stats['pruning']['avg_nodes_per_game']:.2f}")
    print(f"  - Tiempo promedio de ejecución: {stats['pruning']['avg_time_per_game']:.4f} segundos")
    
    return stats

# Ejecutar experimento con prunning
# Ejecutar experimentos para comparar minimax vs alpha-beta
print("\n\nIniciando experimentos...")

# Ajuste de parámetros
profundidad = 1
startPlayer = 'O'

# Ejecutar experimentos y obtener estadísticas
stats = run_experiments(k=profundidad, startPlayer=startPlayer)