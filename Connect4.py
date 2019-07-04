GRID_WIDTH = 7
GRID_HEIGHT = 6
GRID_BOTTOM_INDEX = 5
INITIAL_DIAGONAL_INDEX = 3

class Board:

    def __init__(self):
        self.grid = [["_" for i in range(GRID_WIDTH)] for j in range(GRID_HEIGHT)]

    def draw(self):
        print("\n  0    1    2    3    4    5    6")
        for row in self.grid:
            print(row)

    def drop(self, col):
        col = int(col)
        for i in range(GRID_BOTTOM_INDEX, -1, -1):
            if self.grid[i][col] == "_":
                self.grid[i][col] = playerLetter(player)
                break

    def win(self, player):
        for i in range(GRID_WIDTH):
            if self.check_col(i, player):
                return True
        for i in range(GRID_HEIGHT):
            if self.check_row(i, player):
                return True
        #diagonals
        row = INITIAL_DIAGONAL_INDEX
        while row <= GRID_BOTTOM_INDEX:
            for i in range(0, 4):
                if self.check_slash(i, row):
                    return True
            row += 1
        row = INITIAL_DIAGONAL_INDEX
        while row <= GRID_BOTTOM_INDEX:
            for i in range(6, 2, -1):
                if self.check_backslash(i, row):
                    return True
            row += 1
        return False

    def check_col(self, col, player):
        x = int(col)
        counter = 1
        for i in range(GRID_HEIGHT):
            if game.grid[i][x] == game.grid[i-1][x] == playerLetter(player):
                counter += 1
        return counter == 4

    def check_row(self, row, player):
        y = int(row)
        counter = 1
        for i in range(GRID_WIDTH):
            if game.grid[y][i] == game.grid[y][i-1] == playerLetter(player):
                counter += 1
            if game.grid[y][i] == playerLetter(player) != game.grid[y][i-1]:
                counter = 1
        return counter == 4

    def check_slash(self, col, row):
        y = int(row) - 1
        counter = 1
        a = int(col) + 1
        b = a + 3
        for i in range(a, b):
            if game.grid[y][i] == game.grid[y+1][i-1] == playerLetter(player):
                counter += 1
                y -= 1
        return counter == 4

    def check_backslash(self, col, row):
        y = int(row) - 1
        counter = 1
        a = int(col) - 1
        b = a - 3
        for i in range(a, b, -1):
            if game.grid[y][i] == game.grid[y+1][i+1] == playerLetter(player):
                counter += 1
                y -= 1
        return counter == 4

def who(turn):
    return 2 if (turn % 2 == 0) else 1

def playerLetter(player):
    return "X" if player == 1 else "O"


import os

turn = 1
player = 1
game = Board()

while True:
    os.system("clear")
    game.draw()
    player = who(turn)
    col = input("\nPlayer {}\nDrop it in what column?: ".format(player))
    game.drop(col)
    if game.win(player):
        game.draw()
        print("\nPlayer {} wins.".format(player))
        break
    turn += 1
