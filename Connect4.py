GRID_WIDTH = 7
GRID_HEIGHT = 6
GRID_TOP_INDEX = 0
GRID_BOTTOM_INDEX = GRID_HEIGHT - 1
FIRST_COL_INDEX = 0
LAST_COL_INDEX = GRID_WIDTH - 1
MIN_DIAGONAL_ROW_INDEX = 3
MAX_SLASH_COL_INDEX = LAST_COL_INDEX - 2
MAX_BACKSLASH_COL_INDEX = FIRST_COL_INDEX + 2

class Board:

    def __init__(self):
        self.grid = [["_" for i in range(GRID_WIDTH)] for j in range(GRID_HEIGHT)]

    def draw(self):
        columns = "    ".join([str(i) for i in range(GRID_WIDTH)])
        print("\n ", columns)
        for row in self.grid:
            print(row)

    def drop(self, col, player):
        for i in range(GRID_BOTTOM_INDEX, -1, -1):
            if self.grid[i][col] == "_":
                self.grid[i][col] = player_Letter(player)
                break

    def win(self, player):
        for i in range(GRID_WIDTH):
            if self.check_col(i, player):
                return True
        for i in range(GRID_HEIGHT):
            if self.check_row(i, player):
                return True
        # Diagonals are only possible in row index 3 and above.
        row = MIN_DIAGONAL_ROW_INDEX
        while row <= GRID_BOTTOM_INDEX:
            for i in range(FIRST_COL_INDEX, MAX_SLASH_COL_INDEX):
                if self.check_slash(i, row, player):
                    return True
            row += 1
        row = MIN_DIAGONAL_ROW_INDEX
        while row <= GRID_BOTTOM_INDEX:
            for i in range(LAST_COL_INDEX, MAX_BACKSLASH_COL_INDEX, -1):
                if self.check_backslash(i, row, player):
                    return True
            row += 1
        return False

    def check_col(self, col, player):
        x = col
        counter = 1
        for i in range(GRID_BOTTOM_INDEX - 1, -1, -1):
            if self.grid[i][x] == self.grid[i+1][x] == player_Letter(player):
                counter += 1
            # Resets counter when something like 'X''X''X''O''X''X' happens.
            if self.grid[i][x] == player_Letter(player) != self.grid[i+1][x]:
                counter = 1
        return counter >= 4

    def check_row(self, row, player):
        y = row
        counter = 1
        for i in range(FIRST_COL_INDEX + 1, GRID_WIDTH):
            if self.grid[y][i] == self.grid[y][i-1] == player_Letter(player):
                counter += 1
            # Resets counter when something like 'X''X''X''O''X''X' happens.
            if self.grid[y][i] == player_Letter(player) != self.grid[y][i-1]:
                counter = 1
        return counter >= 4

    # check_slash & check_backslash checks for consecutive values starting from
    # coordinates col & row, then works its way diagonally. 
    def check_slash(self, col, row, player):
        # 'y' and 'x' are modified to represent the second element in the consecutive series. 
        y = row - 1
        x = col + 1
        counter = 1
        # 'x' sets the range to only check 3 elements elements. 
        # 'i' goes through the columns, then 'y' elevates it to the previous index, creating
        # a stair pattern going up.
        for i in range(x, x + 3):
            if self.grid[y][i] == self.grid[y+1][i-1] == player_Letter(player):
                counter += 1
                y -= 1
        return counter >= 4

    def check_backslash(self, col, row, player):
        y = row - 1
        x = col - 1
        counter = 1
        # check_backslash works the same way, but in reverse.
        for i in range(x, x - 3, -1):
            if self.grid[y][i] == self.grid[y+1][i+1] == player_Letter(player):
                counter += 1
                y -= 1
        return counter >= 4

def who(turn):
    return 2 if (turn % 2 == 0) else 1

def player_Letter(player):
    return "X" if player == 1 else "O"

import os

def play_Connect4():
    turn = 1
    player = 1
    game = Board()
    while True:
        os.system("clear")
        game.draw()
        player = who(turn)
        col = int(input("\nPlayer {}\nDrop it in what column?: ".format(player)))
        game.drop(col, player)
        if game.win(player):
            game.draw()
            print("\nPlayer {} wins.".format(player))
            break
        turn += 1

if __name__ == '__main__':
    play_Connect4()
