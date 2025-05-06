import random
from tictactoe import TicTacToe
from minimax import minimax

def random_move(game, player):
    move = random.choice(game.available_moves())
    game.make_move(move, player)


def play_game(k):
    game = TicTacToe()
    turn = random.choice(['X', 'O'])
    nodes = [0]

    while not game.is_terminal():
        if turn == 'X':
            _, move = minimax(game, 0, True, k, nodes)
            if move is not None:
                game.make_move(move, 'X')
        else:
            random_move(game, 'O')
        turn = 'O' if turn == 'X' else 'X'

    return game.utility(), nodes[0]


def experiment(N=1000, k=3):
    wins = draws = losses = 0
    total_nodes = 0
    for _ in range(N):
        result, nodes = play_game(k)
        if result == 1:
            wins += 1
        elif result == 0:
            draws += 1
        else:
            losses += 1
        total_nodes += nodes

    print(f"Resultados tras {N} partidas:")
    print(f"Victorias: {wins}")
    print(f"Empates:  {draws}")
    print(f"Derrotas: {losses}")
    print(f"Promedio de nodos explorados: {total_nodes / N:.2f}")

# Ejecutar experimento
experiment(N=1000, k=3)