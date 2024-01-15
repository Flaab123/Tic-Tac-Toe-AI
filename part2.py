import re
import random

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
    table = [[line]*size for line in table]
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
    flat_table = [item for line in table for item in line]
    while fill_done == 'n':
        user_input = input()
        coords = user_input.split()
        if not re.match(r"[\d] [\d]",user_input):
            print("You should enter numbers!")
        elif int(coords[0]) > 3 or int(coords[1]) > 3:
            print("Coordinates should be from 1 to 3!")
        elif table[int(coords[0])-1][int(coords[1])-1] != ' ':
            print("This cell is occupied! Choose another one!")
        elif flat_table.count('X') > flat_table.count('O'):
            table[int(coords[0])-1][int(coords[1])-1] = 'O'
            fill_done = 'y'
        else:
            table[int(coords[0])-1][int(coords[1])-1] = 'X'
            fill_done = 'y'
    table_print(table)
    return table

def check_win(table):
    winner = None
    for i in range(len(table)): 
        elements = list(set(table[i])) # horizontal check
        if len(elements) == 1 and elements != [' ']:
            winner = elements[0]
            break
        elements = list(set([element[i] for element in table])) # vertical check
        if len(elements) == 1 and elements != [' ']:
            winner = elements[0]
            break
        if i == 0: # diagonal check
            elements = []
            for i in range(len(table)):
                elements.append(table[i][i])
            elements = list(set(elements))
            if len(elements) == 1 and elements != [' ']:
                winner = elements[0]
            # other diagonal    
            elements = []
            for i in range(len(table)):
                elements.append(table[i][len(table)-1-i])
            elements = list(set(elements))
            if len(elements) == 1 and elements != [' ']:
                winner = elements[0]
                break
    empty_elements = sum([element.count(' ') for element in table])
    if winner == None and empty_elements != 0:
        done = False
        print("Game not finished")
    elif winner == None and empty_elements == 0:
        done = True
        print("Draw")
    else:
        done = True
        print(f"{winner} wins")
    return done

tic_tac_table = init_table(3)
print("Enter the cells:")
filled_table = fill_table(tic_tac_table,3)
table_print(filled_table)
filled_table2 = fill_coordinate(filled_table)
state = check_win(filled_table2)
