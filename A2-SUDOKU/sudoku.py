import sys
def row_list(a_list):   #This function lists the numbers in the row where the cell is located
    return [a_list[i:i + 9] for i in range (0,len(a_list),9)]
def col_list(a_list):   #This function lists the numbers in the column where the cell is located
    column = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(9):
        element=[a_list[j] for j in range(i,len(a_list),9)]
        column[i]=element
    return column
def block_control(i):       #This function allows us to find out which 9x9 block the cell is in.
    if i<=20 and i%9 in[0,1,2]:
        return 0
    elif i<=23 and i%9 in[3,4,5]:
        return 1
    elif i<=26 and i%9 in[6,7,8]:
        return 2
    elif i<=47 and i%9 in[0,1,2]:
        return 3
    elif i<=50 and i%9 in[3,4,5]:
        return 4
    elif i<=53 and i%9 in[6,7,8]:
        return 5
    elif i<=74 and i%9 in[0,1,2]:
        return 6
    elif i<=77 and i%9 in[3,4,5]:
        return 7
    elif i<=80 and i%9 in[6,7,8]:
        return 8
def square(a_list):  #This function lists the numbers in the block where the cell is located
    block = []
    for i in range(0,81,27):
        for i in range(i,i+9,3):
            for i in range(i,i+3):
                x=[a_list[j] for j in range(i,(i+27),9)]
                block.extend(x)
    return [block[k:k + 9] for k in range(0, len(block), 9)]
def convert(a_list):  #This function converts the string type input we receive from the terminal into a integer list.
    for i in range(len(a_list)):
        a_list[i]=int(a_list[i])
def control(a_list,step,output_file):   #This function checks the possibilities of a cell and if there is one possibility it places it and prints the step by step.
    numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    i=0
    for i in range(len(a_list)):
        block_number=block_control(i)
        row = row_list(a_list)      #List the columns, rows, and blocks in the list.
        block_list = square(a_list)
        column=col_list(a_list)
        if (a_list[i] == 0):   #We find which column and row the cell is in
            col_number = i % 9
            if (i > 8):
                row_number = int((i - col_number) / 9)
            else:
                row_number = 0
            union = set(row[row_number] + column[col_number] + block_list[block_number])
            remain = numbers - union  # "remain"  is the set of possible numbers.
            if (len(remain) == 1):
                temp = list(remain)[0]
                a_list[i] = temp
                row = row_list(a_list)         #If the number of possible numbers is one, update the lists.
                block_list = square(a_list)
                column=col_list(a_list)
                output_file.write("------------------\nStep {} - {} @ R{}C{}\n------------------\n".format(step,temp,row_number+1,col_number+1))
                for j in range(9):
                    output_file.write(f"{' '.join(map(str, row[j]))}\n")
                break
def solution_loop(a_list,output_file): #It starts the  control loop over, step by step, until there are no 0 left.
    step=1
    while 0 in a_list:
        control(a_list,step,output_file)
        step+=1
    output_file.write("------------------")
def main():
    input_file=open(sys.argv[1],"r")
    output_file=open(sys.argv[2],"w")
    text_document=input_file.read()
    input_file.close()
    text_document=text_document.split()
    convert(text_document)
    output_file.flush()
    solution_loop(text_document,output_file)
    output_file.close()
if __name__== "__main__":
    main()