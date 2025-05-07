import random
from tictactoe import TicTacToe
from minimax import minimax


def play_game(k, first_player):
    game = TicTacToe()
    turn = first_player  # ahora controlamos quién comienza
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
        'X': {'wins': 0, 'draws': 0, 'losses': 0, 'nodes': 0, 'count': 0},
        'O': {'wins': 0, 'draws': 0, 'losses': 0, 'nodes': 0, 'count': 0}
    }

    for _ in range(N):
        first_player = random.choice(['X', 'O'])
        result, nodes = play_game(k, first_player)

        stats[first_player]['count'] += 1
        stats[first_player]['nodes'] += nodes
        if result == 1:
            stats[first_player]['wins'] += 1
        elif result == 0:
            stats[first_player]['draws'] += 1
        else:
            stats[first_player]['losses'] += 1

    for player in ['X', 'O']:
        print(f"\nResultados cuando comienza {player}:")
        print(f"  Partidas jugadas: {stats[player]['count']}")
        print(f"  Victorias: {stats[player]['wins']}")
        print(f"  Empates:  {stats[player]['draws']}")
        print(f"  Derrotas: {stats[player]['losses']}")
        if stats[player]['count'] > 0:
            avg_nodes = stats[player]['nodes'] / stats[player]['count']
            print(f"  Promedio de nodos explorados: {avg_nodes:.2f}")

# Ejecutar experimento separado
experiment_separado(N=1000, k=3)
