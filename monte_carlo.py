import numpy as np
import random
import math
import time
from copy import deepcopy

class TicTacToe:
    def __init__(self, board=None, current_player='X'):
        self.board = np.full((3, 3), '', dtype=str) if board is None else board
        self.current_player = current_player
    
    def get_legal_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == '']
    
    def make_move(self, move):
        new_board = deepcopy(self.board)
        new_board[move] = self.current_player
        next_player = 'O' if self.current_player == 'X' else 'X'
        return TicTacToe(new_board, next_player)
    
    def get_winner(self):
        # Check rows and columns
        for i in range(3):
            if self.board[i, 0] != '' and self.board[i, 0] == self.board[i, 1] == self.board[i, 2]:
                return self.board[i, 0]
            if self.board[0, i] != '' and self.board[0, i] == self.board[1, i] == self.board[2, i]:
                return self.board[0, i]
        
        # Check diagonals
        if self.board[0, 0] != '' and self.board[0, 0] == self.board[1, 1] == self.board[2, 2]:
            return self.board[0, 0]
        if self.board[0, 2] != '' and self.board[0, 2] == self.board[1, 1] == self.board[2, 0]:
            return self.board[0, 2]
        
        return None
    
    def is_game_over(self):
        return self.get_winner() is not None or len(self.get_legal_moves()) == 0
    
    def get_result(self):
        winner = self.get_winner()
        if winner is None:
            if len(self.get_legal_moves()) == 0:
                return 0  # Empate
            return None  # Juego no terminado
        return 1 if winner == 'X' else -1

class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = state.get_legal_moves()
    
    def ucb1(self, c_param):
        if self.visits == 0:
            return float('inf')
        exploitation = self.wins / self.visits
        exploration = c_param * math.sqrt(math.log(self.parent.visits) / self.visits) if self.parent else 0
        return exploitation + exploration
    
    def select_child(self, c_param):
        return max(self.children, key=lambda child: child.ucb1(c_param))
    
    def expand(self):
        move = self.untried_moves.pop(random.randrange(len(self.untried_moves)))
        child = MCTSNode(self.state.make_move(move), self, move)
        self.children.append(child)
        return child
    
    def update(self, result):
        self.visits += 1
        if result is not None:
            self.wins += result

class MCTS:
    def __init__(self, c_param=math.sqrt(2), num_simulations=100):
        self.c_param = c_param
        self.num_simulations = num_simulations
        self.nodes_explored = 0
    
    def search(self, state):
        self.nodes_explored = 0
        root = MCTSNode(state)
        
        for _ in range(self.num_simulations):
            # Selección
            node = root
            while node.untried_moves == [] and node.children != [] and not node.state.is_game_over():
                node = node.select_child(self.c_param)
                self.nodes_explored += 1
            
            # Expansión
            if node.untried_moves != [] and not node.state.is_game_over():
                node = node.expand()
                self.nodes_explored += 1
            
            # Simulación
            state_copy = deepcopy(node.state)
            while not state_copy.is_game_over():
                move = random.choice(state_copy.get_legal_moves())
                state_copy = state_copy.make_move(move)
            
            # Retropropagación
            result = state_copy.get_result()
            while node:
                node.update(result)
                node = node.parent
        
        if not root.children:
            return random.choice(state.get_legal_moves())
        
        return max(root.children, key=lambda c: c.visits).move

def run_experiment(mcts_params, starting_player='X', num_games=1000):
    """Ejecuta experimentos con los parámetros dados y el jugador inicial especificado."""
    wins_x = 0
    wins_o = 0
    draws = 0
    total_nodes = 0
    total_time = 0
    
    for _ in range(num_games):
        game = TicTacToe(current_player=starting_player)
        mcts = MCTS(**mcts_params)
        start_time = time.time()
        
        while not game.is_game_over():
            move = mcts.search(game)
            game = game.make_move(move)
            total_nodes += mcts.nodes_explored
        
        total_time += time.time() - start_time
        
        result = game.get_result()
        if result == 1:
            wins_x += 1
        elif result == -1:
            wins_o += 1
        else:
            draws += 1
    
    return {
        'starting_player': starting_player,
        'wins_x': wins_x,
        'wins_o': wins_o,
        'draws': draws,
        'avg_nodes': total_nodes / num_games,
        'avg_time': total_time / num_games
    }

def run_experiments():
    """Ejecuta experimentos con diferentes variantes de MCTS."""
    # Definir las 6 variantes de parámetros a probar
    variants = [
        {'name': 'c = sqrt(2)', 'params': {'c_param': math.sqrt(2), 'num_simulations': 100}},
        {'name': 'c = 2.0', 'params': {'c_param': 2.0, 'num_simulations': 100}},
        {'name': 'c = 0.5', 'params': {'c_param': 0.5, 'num_simulations': 100}},
        {'name': 'c = 3.0', 'params': {'c_param': 3.0, 'num_simulations': 100}},
        {'name': 'c = 0.1', 'params': {'c_param': 0.1, 'num_simulations': 100}},
    ]
    
    results = []
    total_experiments = 2 * len(variants)  # X inicia + O inicia para cada variante
    
    print("Ejecutando experimentos...")
    for i, variant in enumerate(variants):
        # Cuando X inicia
        print(f"Progreso: {2*i+1}/{total_experiments} - {variant['name']} (X inicia)")
        x_result = run_experiment(variant['params'], 'X', 1000)
        x_result['variant'] = variant['name']
        results.append(x_result)
        
        # Cuando O inicia
        print(f"Progreso: {2*i+2}/{total_experiments} - {variant['name']} (O inicia)")
        o_result = run_experiment(variant['params'], 'O', 1000)
        o_result['variant'] = variant['name']
        results.append(o_result)
    
    print("\nTabla de Resultados:")
    print("=" * 110)
    print(f"{'Variante':<15} | {'Inicia':<6} | {'Victorias X':<15} | {'Victorias O':<15} | {'Empates':<15} | {'Tiempo (s)':<10} | {'Nodos Expl.':<10}")
    print("-" * 110)
    
    for r in results:
        print(f"{r['variant']:<15} | {r['starting_player']:<6} | {r['wins_x']} ({r['wins_x']/1000:.1%}) | "
              f"{r['wins_o']} ({r['wins_o']/1000:.1%}) | {r['draws']} ({r['draws']/1000:.1%}) | "
              f"{r['avg_time']:.4f} | {r['avg_nodes']:.1f}")
    
    return results

if __name__ == "__main__":
    results = run_experiments()