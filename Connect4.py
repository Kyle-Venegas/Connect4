GRID_WIDTH = 7
GRID_HEIGHT = 6

grid = [["_" for i in range(GRID_WIDTH)] for j in range(GRID_HEIGHT)]

def who(turn):
    if turn % 2 == 0:
        return 2
    else: 
        return 1

def playerLetter(player):
    return "X" if player == 1 else "O"

def draw():
    print("\n  0    1    2    3    4    5    6")
    for row in grid:
        print(row)

def drop(col):
    col = int(col)
    for i in range(5, -1, -1):
        if grid[i][col] == "_":
            grid[i][col] = playerLetter(player)
            break
    
def checkcol(col, player):
    x = int(col)
    count = 1
    for i in range(6):
        if grid[i][x] == grid[i-1][x] == playerLetter(player):
            count += 1
    if count < 4:
        return False
    return True

def checkrow(row, player):
    y = int(row)
    count = 1
    for i in range(7):
        if grid[y][i] == grid[y][i-1] == playerLetter(player):
            count += 1
        if grid[y][i] == playerLetter(player) != grid[y][i-1]:
            count = 1
    if count < 4:
        return False
    return True

def checkslash(col, row):
    y = int(row) - 1
    count = 1
    a = int(col) + 1
    b = a + 3
    for i in range(a, b):
        if grid[y][i] == grid[y+1][i-1] == playerLetter(player):
            count += 1
            y -= 1
    if count < 4:
        return False
    return True

def checkbackslash(col, row): #first one is (6, 3)
    y = int(row) - 1
    count = 1
    a = int(col) - 1
    b = a - 3
    for i in range(a, b, -1):
        if grid[y][i] == grid[y+1][i+1] == playerLetter(player):
            count += 1
            y -= 1
    if count < 4:
        return False
    return True

def win(player):
    for i in range(7):
        if checkcol(i, player):
            return True
    for i in range(6):
        if checkrow(i, player):
            return True
    #diagonals
    row = 3
    while row <= 5:
        for i in range(0, 4):
            if checkslash(i, row):
                return True
        row += 1
    row = 3
    while row <= 5:
        for i in range(6, 2, -1):
            if checkbackslash(i, row):
                return True
        row += 1
    return False

import os

turn = 1
player = 1

while True:
    os.system("clear")
    draw()
    player = who(turn)
    col = input("\nPlayer {}\nDrop it in what column?: ".format(player))
    drop(col)
    if win(player):
        draw()
        print("\nPlayer {} wins.".format(player))
        break
    turn += 1
