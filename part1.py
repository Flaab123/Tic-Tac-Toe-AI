import re

def table_print(table):
    """Checks if the user input already exists as a term or definition"""
    print('-'*9)
    for y in table:
        line = '| '
        for x in y:
            line += x+' '
        line += '|'
        print(line)
    print('-'*9)

def init_table(size):
    table = [' ']*size
    table = [ [line]*size for line in table]
    return table

def fill_table(table,size):
    user_input = input()
    temp_table = [item for line in table for item in line]
    for i,x in enumerate(user_input):
        if x != '_':
            temp_table[i] = x
    temp_table = [temp_table[size*i : size*(i+1)] for i in range(size)]
    return temp_table

def fill_coordinate(table):
    print("Enter the coordinates:")
    fill_done = 'n'
    while fill_done == 'n':
        user_input = input()
        coords = user_input.split()
        if not re.match(r"[1-3] [1-3]",user_input):
            print("You should enter numbers!")
        elif table[int(coords[0])-1][int(coords[1])-1] != ' ':
            print("This cell is occupied! Choose another one!")
        elif table.count('X') > table.count('O'):
            table[int(coords[0])-1][int(coords[1])-1] = 'O'
            fill_done = 'y'
        else:
            table[int(coords[0])-1][int(coords[1])-1] = 'X'
            fill_done = 'y'
    table_print(table)
    return table

tic_tac_table = init_table(3)
print("Enter the cells:")
filled_table = fill_table(tic_tac_table,3)
table_print(filled_table)
filled_table2 = fill_coordinate(filled_table)
