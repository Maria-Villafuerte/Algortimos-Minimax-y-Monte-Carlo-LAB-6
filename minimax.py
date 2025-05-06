import copy

def minimax(game, depth, maximizing, k, node_counter):
    node_counter[0] += 1

    if game.is_terminal() or depth == k:
        return game.utility() if game.is_terminal() else game.heuristic(), None

    best_move = None
    if maximizing:
        max_eval = float('-inf')
        for move in game.available_moves():
            new_game = copy.deepcopy(game)
            new_game.make_move(move, 'X')
            eval, _ = minimax(new_game, depth+1, False, k, node_counter)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in game.available_moves():
            new_game = copy.deepcopy(game)
            new_game.make_move(move, 'O')
            eval, _ = minimax(new_game, depth+1, True, k, node_counter)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move