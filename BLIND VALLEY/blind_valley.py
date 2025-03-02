import sys


def all_lines_check(row_num, alist, input):
    # This function reads all lines from "input" and adds them to "alist".
    for i in range(row_num):
        alist.append(input.readline().split())


""" 
    board: A list with all game rows listed like [['L', 'R', 'L', 'R'],['U', 'U', 'L', 'R'] ...]
    limitation: The restrictions are listed in this argument like,
    [['2', '-1', '-1'], ['-1', '-1', '2'], ['-1', '2', '-1', '-1'], ['-1', '-1', '-1', '0']]
"""


def control_row(board, limitation, i):
    # This function checks if a row satisfies the restrictions when it is full.
    if int(limitation[0][i]) != -1:  # i means column index ("i+1" th row).
        if int(board[i].count("H")) != int(limitation[0][i]):  # "0" means restrictions on the left side of the board.
            return False
    if int(limitation[1][i]) != -1:
        if int(board[i].count("B")) != int(limitation[1][i]):  # "1" means restrictions on the right side of the board.
            return False
    return True


def control_column(limitation, all_columns, j):
    # This function checks if a column satisfies the restrictions when it is full.
    if int(limitation[2][j]) != -1:  # j means column index ("j+1" th column).
        if int(all_columns[j].count("H")) != int(limitation[2][j]):  # "2" means restrictions at the top of the board.
            return False
    if int(limitation[3][j]) != -1:
        if int(all_columns[j].count("B")) != int(limitation[3][j]):  # "3" means restrictions at the bottom of the board.
            return False
    return True


def tile_control(board, number_of_column, board_size, tile_list, index_list):
    """
    This function lists tiles in the order they should be placed (into the tile_list).
    tile_list= [['L', 'R'],['L', 'R'],['U', 'D']...]
    It also adds indexes to index_list in accordance with the order of the tile_list.
    index_list= [0, 1, 2, 3, 4, 8, 5, 9, 6, 7, 10, 11] etc.
    """
    for i in range(board_size):  # board_size= number of tiles x 2
        row_index = i // number_of_column
        column_index = i % number_of_column
        if board[row_index][column_index] == 'L':
            tile_list.append([board[row_index][column_index], board[row_index][column_index+1]])
            index_list.append(i)
            index_list.append(i+1)
        elif board[row_index][column_index] == 'U':
            tile_list.append([board[row_index][column_index], board[row_index+1][column_index]])
            index_list.append(i)
            index_list.append(i+number_of_column)


def update_lines(index_list, board, board_size, tile_list, number_of_column):
    # This function updates the tile_list changes to the board via "index_match" library.
    letter_list = [letter for a_tile in tile_list for letter in a_tile]  # İt lists the elements in the tile_list directly for matching. ['L','R','U','D'...]
    index_match = dict(zip(index_list, letter_list))  # It maps letters and their indexes into the index_match library.
    temp = []
    board.clear()
    for i in range(board_size):   # It relists the board based on the data in the library.
        board.insert(i, index_match[i])
    for i in range(0, board_size, number_of_column):  # It divides the letters on the board into rows as before.
        temp.append(board[i:i+number_of_column])
    board.clear()
    board.extend(temp)


def is_the_row_full(board):  # It checks if there are any full rows and if so, adds it to the "full_row" list.
    full_row = []
    for row_index in range(len(board)):
        for letter in board[row_index]:
            if letter in ['L', 'R', 'U', 'D']:
                if len(full_row) != 0:
                    return full_row
                else:
                    return False
        full_row.append(row_index)
    return full_row


def is_the_column_full(all_columns):  # It checks if there are any full column and if so, adds it to the "full_column" list.
    full_column = []
    for column_index in range(len(all_columns)):
        for letter in all_columns[column_index]:
            if letter in ['L', 'R', 'U', 'D']:
                if len(full_column) != 0:
                    return full_column
                else:
                    return False
        full_column.append(column_index)
    return full_column


def control_neighbor(board_lines, column_number):  # This function checks if there are any letters that do not comply with the contiguity rules.
    for sub_list in board_lines:  # It checks for errors located side by side.
        for i in range(column_number):
            if i + 1 < column_number:  # (If there is a column on the right side.)
                if sub_list[i] == sub_list[i + 1]:
                    if sub_list[i] not in ["N", 'L', 'U', 'D', 'R']:  # (If it is different from these elements:["N", 'L', 'U', 'D', 'R'].)
                        return False
            if i - 1 > -1:  # (If there is a column on the left side.)
                if sub_list[i] == sub_list[i - 1]:
                    if sub_list[i] not in ["N", 'L', 'U', 'D', 'R']:
                        return False

    for n in range(len(board_lines)):  # It checks for errors located on top of each other.
        for k in range(column_number):  # "len(board_lines)"  means number of row on board game.
            if n + 1 < len(board_lines):  # (If there is a row below.)
                if board_lines[n][k] == board_lines[n + 1][k]:
                    if board_lines[n][k] not in ["N", 'L', 'U', 'D', 'R']:
                        return False
            if n - 1 > -1:  # (If there is a row above.)
                if board_lines[n][k] == board_lines[n - 1][k]:
                    if board_lines[n][k] not in ["N", 'L', 'U', 'D', 'R']:
                        return False

    return True  # If there is no error.


def valley_solution_with_backtracking(i, tile_list, board, number_of_column, all_columns, limitation, answer_list, index_list, board_size, output):
    #  This function reaches the solution of the valley through backtracking algorithm.
    options = [["H", "B"], ["B", "H"], ["N", "N"]]  # (possible tiles)
    if type(is_the_row_full(board)) == list:
        for row_index in is_the_row_full(board):
            if control_row(board, limitation, row_index) == True:
                pass
            else:
                return
    """ It checks restrictions for all full rows.
        If it is suitable continue placement
        If it is not suitable, it  steps back via "return".  """

    if type(is_the_column_full(all_columns)) == list:
        for col_index in is_the_column_full(all_columns):
            if control_column(limitation, all_columns, col_index) == True:
                pass
            else:
                return
    """ It checks restrictions for all full columns.
        If it is suitable, continue placement
        If it is not suitable, it  steps back via "return".  """

    if ['L', 'R'] not in tile_list and ['U', 'D'] not in tile_list:  # Are all tiles full?
        answer_list.append(board)
        for a_row in board[:-1]:
            output.write(f"{' '.join(a_row)}\n")
        output.write(f"{' '.join(board[-1])}")
        output.close()
        exit()
    """
     If all tiles are full and comply with the restrictions,it writes the answer into output file and finishes program.
    """

    for option in options:
        del tile_list[i]   # "i" represents tile index.It deletes the tile and prepares the new one to be placed.
        tile_list.insert(i, option)   # It places the  option from possible tiles.
        update_lines(index_list, board, board_size, tile_list, number_of_column)    # It updates the board based on tiles.
        all_columns = [[line[i] for line in board] for i in range(number_of_column)]   # It updates the information of the columns.
        if control_neighbor(board, number_of_column) == False:
            continue      # If it does not comply with the contiguity rule, it goes back and tries another option.
        i += 1     # If the all contiguity situation is suitable, it passes to the next tile.
        valley_solution_with_backtracking(i, tile_list, board, number_of_column, all_columns, limitation, answer_list, index_list, board_size, output)
        i -= 1     # If the board does not comply with the restrictions, it will step back.
        tile_list[i] = ['L', 'R'][:]      # It undoes placement.
        update_lines(index_list, board, board_size, tile_list, number_of_column)
        all_columns = [[line[i] for line in board] for i in range(number_of_column)]


def main():
    input_file = open(sys.argv[1], "r")
    output_file = open(sys.argv[2], "w")
    row_number = len(input_file.readlines())
    input_file.close()
    input_file = open(sys.argv[1], "r")
    all_lines, tiles, game_index_list, answer = [], [], [], []
    all_lines_check(row_number, all_lines, input_file)  # It adds all rows into "all_lines".
    column_number = len(all_lines[4])
    game_size = column_number * (row_number - 4)  # (board size like 5x6)
    restrictions = all_lines[0:4]
    board_lines = all_lines[4:row_number]
    columns = [[line[i] for line in board_lines] for i in range(column_number)]  # It lists all columns into "columns".
    tile_control(board_lines, column_number, game_size, tiles, game_index_list)  # It determines tiles.
    output_file.flush()
    # "0" represents the first tile.
    valley_solution_with_backtracking(0, tiles, board_lines, column_number, columns, restrictions, answer, game_index_list, game_size, output_file)
    input_file.close()
    if len(answer) == 0:
        output_file.write("No solution!")
    output_file.close()


if __name__ == "__main__":
    main()