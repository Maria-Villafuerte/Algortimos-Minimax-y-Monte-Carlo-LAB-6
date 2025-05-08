import random
from tictactoe import TicTacToe
from minimax import minimax
import time


def play_game(k, first_player):
    game = TicTacToe()
    turn = first_player
    nodes = [0]

    while not game.is_terminal():
        if turn == 'X':
            _, move = minimax(game, 0, True, k, nodes)
            if move is not None:
                game.make_move(move, 'X')
        else:
            _, move = minimax(game, 0, False, k, nodes)
            if move is not None:
                game.make_move(move, 'O')
        turn = 'O' if turn == 'X' else 'X'
    
    return game.utility(), nodes[0]


def experiment_separado(N=1000, k=3):
    stats = {
        'X': {'wins': 0, 'draws': 0, 'losses': 0, 'nodes': 0},
        'O': {'wins': 0, 'draws': 0, 'losses': 0, 'nodes': 0}
    }

    start_time = time.time()

    for first_player in ['X', 'O']:
        for _ in range(N):
            result, nodes = play_game(k, first_player)

            stats[first_player]['nodes'] += nodes
            if result == 1:
                stats[first_player]['wins'] += 1
            elif result == 0:
                stats[first_player]['draws'] += 1
            else:
                stats[first_player]['losses'] += 1

    end_time = time.time()
    total_time = end_time - start_time

    for player in ['X', 'O']:
        print(f"\nResultados cuando comienza {player}:")
        print(f"  Partidas jugadas: {N}")
        print(f"  Victorias: {stats[player]['wins']}")
        print(f"  Empates:  {stats[player]['draws']}")
        print(f"  Derrotas: {stats[player]['losses']}")
        avg_nodes = stats[player]['nodes'] / N
        print(f"  Promedio de nodos explorados: {avg_nodes:.2f}")

    print(f"\n⏱️ Tiempo total para {2*N} juegos: {total_time:.2f} segundos")
    print(f"⏱️ Tiempo promedio por juego: {total_time/(2*N):.10f} segundos")


# Ejecutar experimento con 1000 juegos por jugador inicial
experiment_separado(N=1000, k=3)
