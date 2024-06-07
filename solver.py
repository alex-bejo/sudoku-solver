import numpy as np

def get_neighbours(row, col):
    rowA = [0,0,0,1,1,1,2,2,2]
    rowB = [3,3,3,4,4,4,5,5,5]
    rowC = [6,6,6,7,7,7,8,8,8]
    colA = [0,1,2,0,1,2,0,1,2]
    colB = [3,4,5,3,4,5,3,4,5]
    colC = [6,7,8,6,7,8,6,7,8]
    output = [[0,0] for i in range(9)]
    if row <= 2:
        for i in range(9):
            output[i][0] = rowA[i]
    elif row <= 5:
        for i in range(9):
            output[i][0] = rowB[i]
    else:
        for i in range(9):
            output[i][0] = rowC[i]

    if col <= 2:
        for i in range(9):
            output[i][1] = colA[i]
    elif col <= 5:
        for i in range(9):
            output[i][1] = colB[i]
    else:
        for i in range(9):
            output[i][1] = colC[i]
    for neighbour in output:
        if neighbour[0] == row and neighbour[1] == col:
            output.remove(neighbour)
            break
    return output

def get_possible_values(board, row, col):
    if board[row][col] != 0:
        return [board[row][col]]
    not_possible = set()
    neighbours = get_neighbours(row, col)
    for neighbour in neighbours:
        if board[neighbour[0]][neighbour[1]] != 0:
            not_possible.add(board[neighbour[0]][neighbour[1]])
    for r in range(9):
        if board[r][col] != 0:
            not_possible.add(board[r][col])
    for c in range(9):
        if board[row][c] != 0:
            not_possible.add(board[row][c])
    
    return [i for i in range(1,10) if i not in not_possible]

def check_for_pinned(board, row, col):
    neighbours = get_neighbours(row, col)
    for possible in get_possible_values(board, row, col):
        num_neighbours = 0
        num_row = 0
        num_col = 0

        for neighbour in neighbours:
            if possible not in get_possible_values(board, neighbour[0], neighbour[1]):
                num_neighbours += 1
                if num_neighbours == 8:
                    return possible
        
        for r in range(9):
            if r == row:
                continue
            
            if possible not in get_possible_values(board, r, col):
                num_row += 1
                if num_row == 8:
                    return possible
        
        for c in range(9):
            if c == col:
                continue

            if possible not in get_possible_values(board, row, c):
                num_col += 1
                if num_col == 8:
                    return possible
    return 0

def solve(board):
    num_blanks = 0
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                num_blanks += 1
    
    while num_blanks > 0:
        made_adjustment = False
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    continue

                possible = get_possible_values(board, i, j)
                if len(possible) == 0:
                    print(f"No possible values for grid {i},{j}")
                    return board
                if len(possible) == 1:
                    board[i][j] = possible[0]
                    made_adjustment = True
                    num_blanks -= 1
                else:
                    pin = check_for_pinned(board, i, j)
                    if pin != 0:
                        board[i][j] = pin
                        made_adjustment = True
                        num_blanks -= 1
        if not made_adjustment:
            print("Needed more information")
            return board
                
    print(num_blanks)
    return board

board = [[] for i in range(9)]
print("Enter each element in the row separated by a space. If a number is blank, put a 0. Press enter and do the next row until the end.")
for i in range(9):
    board[i] = [int(i) for i in input().split(" ")]

solved = solve(board)
for row in solved:
    print(row)