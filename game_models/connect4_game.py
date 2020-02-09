from itertools import groupby, chain

from utils import funcs

EMPTY = "🔲"
RED = "🔴"
YELLOW = "🟡"


def diagonalsPos(matrix, cols, rows):
    """Get positive diagonals, going from bottom-left to top-right."""
    for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if 0 <= i < cols and 0 <= j < rows]


def diagonalsNeg(matrix, cols, rows):
    """Get negative diagonals, going from top-left to bottom-right."""
    for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if 0 <= i < cols and 0 <= j < rows]


class Connect4Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.turn = player1
        self.board = [[EMPTY] * 6 for _ in range(7)]
        self.winner = None
        self.last_react_time = None

    def place(self, column, color):
        if self.board[column][0] != EMPTY:
            return False  # return false if column is full
        i = -1
        while self.board[column][i] != EMPTY:
            i -= 1
        self.board[column][i] = color
        if self.turn == self.player1:
            self.turn = self.player2
        else:
            self.turn = self.player1
        return True

    def getWinner(self):
        lines = (
            self.board,  # columns
            zip(*self.board),  # rows
            diagonalsPos(self.board, 7, 6),  # positive diagonals
            diagonalsNeg(self.board, 7, 6)  # negative diagonals
        )

        for line in chain(*lines):
            for color, group in groupby(line):
                if color != EMPTY and len(list(group)) >= 4:
                    if color == RED:
                        return self.player1
                    else:
                        return self.player2
        return False

    def checkDraw(self):
        result = True
        for columns in self.board:
            for item in columns:
                if item == EMPTY:
                    result = False
        return result

    def getColorFromPlayer(self, player):
        if player == self.player1:
            return RED
        else:
            return YELLOW

    def __str__(self):
        board_str = " ".join(map(lambda x: funcs.number_emojis()[x - 1], range(1, 8))) + "\n"
        for y in range(6):
            board_str += " ".join(str(self.board[x][y]) for x in range(7)) + "\n"
        return board_str
