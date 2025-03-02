import sys
def convert(a_list):   #This function converts the input file's list to integers
    for i in range(len(a_list)):
        a_list[i]=int(a_list[i])
def column_and_row_control(a_list,number_of_columns):  #This function lists the indices of numbers in rows and columns.
    for i in range(number_of_columns):
        columns.append([j for j in range(i,len(a_list),number_of_columns)])
    for i in range(0,input_size,number_of_columns):
        rows.append([j for j in range(i,i+number_of_columns)])
def row(a_list,number_of_columns): #This function lists the numbers in the rows in a list
    return [a_list[i:i + number_of_columns] for i in range (0,len(a_list),number_of_columns)]
def column(a_list,number_of_columns,col_list): #This function lists the numbers in the columns in a list
    for i in range(number_of_columns):
        element=[a_list[j] for j in range(i,len(a_list),number_of_columns)]
        col_list.insert(i,element)
def corner_points_control(number_of_columns): #This function determines the corner points of the input file
    corner_points = []
    for i in range(input_size):
        if (i in [0, number_of_columns - 1, input_size - number_of_columns, input_size - 1]):
            corner_points.append(i)
    return corner_points
def control(control_size,control_edge_points,control_corner_points,control_column,a_list):
#This function checks if there are any possible numbers that can be cleared or it ends the game.
    for i in range(control_size):
        control_neighbours = []
        if i in control_edge_points:
            if i % control_column == 0:
                control_neighbours.extend([i + 1, i - control_column, i + control_column])
            elif i % control_column == control_column - 1:
                control_neighbours.extend([i - 1, i - control_column, i + control_column])
            elif i < control_column:
                control_neighbours.extend([i - 1, i + control_column, i + 1])
            else:
                control_neighbours.extend([i - 1, i - control_column, i + 1])
        elif i in control_corner_points:
            if i == 0:
                control_neighbours.extend([i + control_column, i + 1])
            if i == control_size - 1:
                control_neighbours.extend([i - 1, i - control_column])
            if i == control_column - 1:
                control_neighbours.extend([i - 1, i + control_column])
            if i == control_size - control_column:
                control_neighbours.extend([i - control_column, i + 1])
        else:
            control_neighbours.extend([i - 1, i - control_column, i + control_column, i + 1])
        for j in control_neighbours:
            if j>-1 and j<control_size:
                if a_list[j] == a_list[i]:
                    if a_list[i]!=" ":
                        return True
                else:
                    if i == control_size-1:
                        print("\nGame Over")
                        return False
def game(game_number_of_column,game_column_list,game_row_list,point,game_number_of_rows,game_list,game_size,game_edge_points,game_corner_points):
    x=0
    y=0
    x, y = input("\nPlease enter a row and a column number: ").split()
    game_position = (int(x) - 1) * game_number_of_column + int(y) - 1
    same_game_neighbours = []
    game_neighbours = []
    same_game_neighbours.append(game_position)
    if game_position>-1 and game_position<game_size and int(y)<=game_number_of_column and int(x)<=game_number_of_rows and int(x)>0 and int(y)>0:
        for i in same_game_neighbours:
            # This piece of code lists the neighbors of the selected number based on its position.
            if i in game_edge_points:
                if i % game_number_of_column == 0:
                    game_neighbours.extend([i + 1, i - game_number_of_column, i + game_number_of_column])
                elif i % game_number_of_column == game_number_of_column - 1:
                    game_neighbours.extend([i - 1, i - game_number_of_column, i + game_number_of_column])
                elif i < game_number_of_column:
                    game_neighbours.extend([i - 1, i + game_number_of_column, i + 1])
                else:
                    game_neighbours.extend([i - 1, i - game_number_of_column, i + 1])
            if i in game_corner_points:
                if i == 0:
                    game_neighbours.extend([i + game_number_of_column, i + 1])
                elif i == game_size - 1:
                    game_neighbours.extend([i - 1, i - game_number_of_column])
                elif i == game_number_of_column - 1:
                    game_neighbours.extend([i - 1, i + game_number_of_column])
                elif i == game_size - game_number_of_column:
                    game_neighbours.extend([i - game_number_of_column, i + 1])
            else:
                game_neighbours.extend([i - 1, i - game_number_of_column, i + game_number_of_column, i + 1])
            for j in game_neighbours:
                if j > -1 and j < game_size:
                    if game_list[j] == game_list[game_position]:
                        if j not in same_game_neighbours:
                            same_game_neighbours.append(j)
        if len(same_game_neighbours) == 1:
            print("\nNo movement happened try again")
            for k in range(1):
                print(f"\n{' '.join(map(str, game_row_list[k]))}")
            for g in range(1, game_number_of_rows):
                print(f"{' '.join(map(str, game_row_list[g]))}")
            print("\nYour score is:", point)
        else:
            number = game_list[game_position]
            for l in same_game_neighbours:   #This code deletes the selected point along with its same neighbors.
                game_list[l] = " "
            for shift in range(game_number_of_rows):
                for element in range(game_size):
                    if (element + game_number_of_column) > -1 and (element + game_number_of_column) < game_size:
                        if game_list[element + game_number_of_column] == " ":
                            temp = game_list[element]
                            game_list[element + game_number_of_column] = temp
                            game_list[element] = " "
            column(game_list,game_number_of_column,game_column_list)
            game_row_list = row(game_list,game_number_of_column)
            point = point + len(same_game_neighbours) * number
            for n in range(game_number_of_column-1,-1,-1): #This code deletes a column if it is completely empty.
                step = 0
                for m in game_column_list[n]:
                    if m == " ":
                        step += 1
                        if step == game_number_of_rows:
                            for l in range(n + (game_number_of_rows - 1) * game_number_of_column, n - game_number_of_column,-game_number_of_column):
                                del game_list[l]
                            game_number_of_column -= 1
            if game_number_of_column==0 or game_number_of_rows==0:
                print("\nYour score is:", point)
                print("\nGame Over")
                exit()
            column(game_list, game_number_of_column, game_column_list)
            game_row_list = row(game_list, game_number_of_column)
            for z in range(game_number_of_rows-1,-1,-1):  #This code deletes a row if it is completely empty.
                step2 = 0
                for h in game_row_list[z]:
                    if h == " ":
                        step2 += 1
                        if step2 == game_number_of_column:
                            for d in range(z*6+number_of_columns-1,z*6-1,-1):
                                del game_list[d]
                            game_number_of_rows -= 1
            if game_number_of_column==0 or game_number_of_rows==0:
                print("\nYour score is:", point)
                print("\nGame Over")
                exit()
            column(game_list,game_number_of_column,game_column_list)
            game_row_list = row(game_list,game_number_of_column)
            for s in range(1):
                print(f"\n{' '.join(map(str, game_row_list[s]))}")
            for c in range(1, game_number_of_rows):
                print(f"{' '.join(map(str, game_row_list[c]))}")
            print("\nYour score is:", point)
    else:
        print("\nPlease enter a correct size!")
    return game_number_of_column,game_list,point
input_file=open(sys.argv[1],"r")
one_line=input_file.readline().split()
input_file=open(sys.argv[1],"r")
text_document=input_file.read()        #These codes are the preparation codes for the game.
text_document=text_document.split()
convert(text_document)
number_of_columns=len(one_line)
input_size=len(text_document)
number_of_rows=input_size//number_of_columns
columns=[]
rows=[]
score=0
column_and_row_control(text_document,number_of_columns)
corner_points=corner_points_control(number_of_columns)
edge_points=list(set(columns[number_of_columns-1]+columns[0]+rows[0]+rows[number_of_rows-1])-set(corner_points))
row_list=row(text_document,number_of_columns)
column_list=[]
column(text_document,number_of_columns,column_list)
for index in range(number_of_rows):
    print(f"{' '.join(map(str,row_list[index]))}")
print("\nYour score is:",score)
while control(input_size,edge_points,corner_points,number_of_columns,text_document)==True:
    number_of_columns,text_document,score=game(number_of_columns,column_list,row_list,score,number_of_rows,text_document,input_size,edge_points,corner_points)
    row_list = row(text_document, number_of_columns)
    column(text_document, number_of_columns, column_list)
    input_size = len(text_document)
    number_of_rows = input_size // number_of_columns
    column_and_row_control(text_document, number_of_columns)
    corner_points = corner_points_control(number_of_columns)
    edge_points = list(set(columns[number_of_columns - 1] + columns[0] + rows[0] + rows[number_of_rows - 1]) - set(corner_points))