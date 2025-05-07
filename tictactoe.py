class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9  # tablero 3x3 plano

    def available_moves(self):
        return [i for i in range(9) if self.board[i] == ' ']

    def make_move(self, index, player):
        if self.board[index] == ' ':
            self.board[index] = player
            return True
        return False

    def check_winner(self):
        combos = [(0,1,2), (3,4,5), (6,7,8),
                  (0,3,6), (1,4,7), (2,5,8),
                  (0,4,8), (2,4,6)]
        for i,j,k in combos:
            if self.board[i] == self.board[j] == self.board[k] and self.board[i] != ' ':
                return self.board[i]
        if ' ' not in self.board:
            return 'Draw'
        return None

    def is_terminal(self):
        return self.check_winner() is not None

    def utility(self):
        winner = self.check_winner()
        if winner == 'X':
            return 1
        elif winner == 'O':
            return -1
        else:
            return 0  # empate

    def heuristic(self):
        # Simple heurística: +10 por 2X alineadas, -10 por 2O alineadas
        score = 0
        lines = [(0,1,2), (3,4,5), (6,7,8),
                 (0,3,6), (1,4,7), (2,5,8),
                 (0,4,8), (2,4,6)]
        for i,j,k in lines:
            line = [self.board[i], self.board[j], self.board[k]]
            if line.count('X') == 2 and line.count(' ') == 1:
                score += 10
            elif line.count('O') == 2 and line.count(' ') == 1:
                score -= 10
        return score
    
    def print_board(self):
        """Imprime el tablero en formato legible"""
        for i in range(0, 9, 3):
            print(f"{self.board[i]} | {self.board[i+1]} | {self.board[i+2]}")
            if i < 6:
                print("-" * 9)