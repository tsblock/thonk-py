class TictactoeGame():
    cross = "❌"
    circle = "⭕"
    empty = "🔲"

    def __init__(self, player1, player2):
        self.board = [[self.empty] * 3, [self.empty] * 3, [self.empty] * 3]
        self.player1 = player1
        self.player2 = player2
        self.turn = player1  # first turn is the player who starts it oof
        self.winner = None

    def __getitem__(self, index):
        return self.board[index // 3][index % 3]

    def place(self, turn, index):
        self[index] = self.get_player_symbol(turn)
        if turn == self.player1:
            turn = self.player2  # player1 done so it's player2's turn
        else:
            turn = self.player1  # vice versa

    def get_player_symbol(self, player):
        if player == self.player1:
            return self.cross
        else:
            return self.circle

    @staticmethod
    def _check_line(iterable, player):
        return all(map(lambda piece: piece == player, iterable))  # check the whole line is placed by the player

    def check_for_win(self):
        for player in [self.cross, self.circle]:
            for row in self.board:
                if self._check_line(row, player):
                    self.winner = self.get_player_symbol(player)
                    return True

            for column in zip(*self.board):
                if self._check_line(column, player):
                    self.winner = self.get_player_symbol(player)
                    return True

            diagonals = [
                [self[0], self[4], self[8]],
                [self[2], self[4], self[8]]
            ]
            for diagonal in diagonals:
                if self._check_line(diagonal, player):
                    self.winner = self.get_player_symbol(player)
                    return True

        return False

    def __str__(self):
        return "\n------------\n".join(' | '.join(row) for row in self.board)
