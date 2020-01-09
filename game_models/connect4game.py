from itertools import groupby, chain

from utils import funcs

EMPTY = "🔲"
RED = "🔴"
BLUE = "🔵"


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

    def place(self, column, color):
        if self.board[0] != EMPTY:
            return False  # return false if column is full
        i = -1
        while self.board[i] != EMPTY:
            i -= 1
        self.board[i] = color
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
                    return color

    def __str__(self):
        board_str = " ".join(map(lambda x: funcs.number_emojis()[x - 1], range(1, 8))) + "\n"
        for y in range(6):
            board_str += " ".join(str(self.board[x][y]) for x in range(7)) + "\n"
        return board_str
