import random
import os
from copy import deepcopy

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

    def win(self, player, passed_grid):
        for i in range(GRID_WIDTH):
            if self.check_col(i, player, passed_grid):
                return True
        for i in range(GRID_HEIGHT):
            if self.check_row(i, player, passed_grid):
                return True
        # Diagonals are only possible in row index 3 and above.
        row = MIN_DIAGONAL_ROW_INDEX
        while row <= GRID_BOTTOM_INDEX:
            for i in range(FIRST_COL_INDEX, MAX_SLASH_COL_INDEX):
                if self.check_slash(i, row, player, passed_grid):
                    return True
            row += 1
        row = MIN_DIAGONAL_ROW_INDEX
        while row <= GRID_BOTTOM_INDEX:
            for i in range(LAST_COL_INDEX, MAX_BACKSLASH_COL_INDEX, -1):
                if self.check_backslash(i, row, player, passed_grid):
                    return True
            row += 1
        return False

    def check_col(self, col, player, passed_grid):
        x = col
        counter = 1
        for i in range(GRID_BOTTOM_INDEX - 1, -1, -1):
            if passed_grid[i][x] == passed_grid[i+1][x] == player_Letter(player):
                counter += 1
            # Resets counter when something like 'X''X''X''O''X''X' happens.
            if passed_grid[i][x] == player_Letter(player) != passed_grid[i+1][x]:
                counter = 1
        return counter >= 4

    def check_row(self, row, player, passed_grid):
        y = row
        counter = 1
        for i in range(FIRST_COL_INDEX + 1, GRID_WIDTH):
            if passed_grid[y][i] == passed_grid[y][i-1] == player_Letter(player):
                counter += 1
            # Resets counter when something like 'X''X''X''O''X''X' happens.
            if passed_grid[y][i] == player_Letter(player) != passed_grid[y][i-1]:
                counter = 1
        return counter >= 4

    # check_slash & check_backslash checks for consecutive values starting from
    # coordinates col & row, then works its way diagonally. 
    def check_slash(self, col, row, player, passed_grid):
        # 'y' and 'x' are modified to represent the second element in the consecutive series. 
        y = row - 1
        x = col + 1
        counter = 1
        # 'x' sets the range to only check 3 elements elements. 
        # 'i' goes through the columns, then 'y' elevates it to the previous index, creating
        # a stair pattern going up.
        for i in range(x, x + 3):
            if passed_grid[y][i] == passed_grid[y+1][i-1] == player_Letter(player):
                counter += 1
                y -= 1
        return counter >= 4

    def check_backslash(self, col, row, player, passed_grid):
        y = row - 1
        x = col - 1
        counter = 1
        # check_backslash works the same way, but in reverse.
        for i in range(x, x - 3, -1):
            if passed_grid[y][i] == passed_grid[y+1][i+1] == player_Letter(player):
                counter += 1
                y -= 1
        return counter >= 4

def who(turn):
    return 2 if (turn % 2 == 0) else 1

def player_Letter(player):
    return "X" if player == 1 else "O"

class AI:
    board = deepcopy(game.grid)

    def ai_game_drop(self, col, piece):
        for i in range(GRID_BOTTOM_INDEX, -1, -1):
            if self.board[i][col] == "_":
                self.board[i][col] = piece
                break

    def check_location(self):
        slots = []
        for i in range(GRID_WIDTH):
            if game.grid[0][i] == '_':
                slots.append(i)
        return slots

    def ai_drop(self, col, piece):
        for i in range(GRID_BOTTOM_INDEX, -1, -1):
            if self.board[i][col] == "_":
                self.board[i][col] = piece
                break

    def score_position(self, piece):
        score = 0

        #center column
        center_array = [self.board[i][GRID_WIDTH//2] for i in range(GRID_HEIGHT)]
        center_count = center_array.count(piece)
        score += center_count * 3
        
        #horizontal
        for r in range(GRID_HEIGHT):
            row_array = [self.board[r][i] for i in range(GRID_WIDTH)]
            for c in range(GRID_WIDTH - 3):
                section = row_array[c:c+4]
                score += self.evaluate(section, piece)

        #vertical
        for c in range(GRID_WIDTH):
            col_array = [self.board[i][c] for i in range(GRID_HEIGHT)]
            for r in range(GRID_HEIGHT - 3):
                section = col_array[r:r+4]
                score += self.evaluate(section, piece)

        #left diagonal
        for r in range(GRID_HEIGHT - 3):
            for c in range(GRID_WIDTH - 3):
                section = [self.board[r+i][c+i] for i in range(4)]
                score += self.evaluate(section, piece)

        #right diagonal
        for r in range(GRID_HEIGHT - 3):
            for c in range(GRID_WIDTH - 1, 2, -1):
                section = [self.board[r+i][c-i] for i in range(4)]
                score += self.evaluate(section, piece)

        return score

    def evaluate(self, array, piece):
        score = 0
        opponent_piece = 'X'
        if piece == 'X':
            opponent_piece = 'O'

        if array.count(piece) == 4:
            score += 10000
        elif array.count(piece) == 3 and array.count('_') == 1:
            score += 50
        elif array.count(piece) == 2 and array.count('_') == 2:
            score += 2

        if array.count(opponent_piece) == 3 and array.count('_') == 1:
            score -= 1000
        elif array.count(opponent_piece) == 2 and array.count('_') == 2:
            score -= 25

        return score

    def best_move(self, piece):
        locations = self.check_location()
        score = -10000
        best_col = random.choice(locations)
        for col in locations:
            self.board = deepcopy(game.grid)
            self.ai_drop(col, 'O')
            new_score = self.score_position('O')
            if new_score > score:
                score = new_score
                best_col = col

        return best_col

    def minimax(self, alpha, beta, maximizing, loop):
        locations = self.check_location()
        if loop == 0 or game.win(2, self.board) or game.win (1, self.board):
            if loop == 0:
                return (self.best_move('O'), self.score_position('O'))

        if maximizing:
            value = -1000000000
            column = random.choice(locations)
            for col in locations:
                self.board = deepcopy(game.grid)
                self.ai_drop(col, 'O')
                col, score = self.minimax(alpha, beta, False, loop - 1)
                if score > value:
                    value = score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value
        else:
            value = 1000000000
            column = random.choice(locations)
            for col in locations:
                self.board = deepcopy(game.grid)
                self.ai_drop(col, 'X')
                col, score = self.minimax(alpha, beta, True, loop - 1)
                if score < value:
                    value = score
                    column = col
                beta = min(alpha, value)
                if alpha >= beta:
                    break
            return column, value
            
ai = AI()
game = Board()

def play_Connect4():
    turn = 1
    player = 1
    while True:
       #os.system("clear")
        game.draw()
        player = who(turn)

        if player == 1:
            locations = ai.check_location()
            col = int(input("\nPlayer {}\nDrop it in what column?: ".format(player)))
            if col not in locations:
                continue
            
        else:
            col, minimax_score = ai.minimax(-1000000000, 1000000000, True, 5)
            print(col)
            #col = ai.best_move('O')

        game.drop(col, player)

        if game.win(player, game.grid):
            game.draw()
            print("\nPlayer {} wins.".format(player))
            break
        turn += 1

if __name__ == '__main__':
    play_Connect4()
