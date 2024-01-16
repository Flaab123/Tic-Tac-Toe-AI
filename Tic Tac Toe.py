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

def enter_move(index,table,sign):
    size = len(table)
    temp_table = [item for line in table for item in line]
    temp_table[index] = sign
    table = [temp_table[size*i : size*(i+1)] for i in range(size)]
    return table

def undo_move(index,table):
    size = len(table)
    temp_table = [item for line in table for item in line]
    temp_table[index] = ' '
    table = [temp_table[size*i : size*(i+1)] for i in range(size)]
    return table

def fill_coordinate_AI_easy(table,sign):
    print('Making move level "easy"')
    size = len(table)
    temp_table = [item for line in table for item in line]
    elements = []
    for i,x in enumerate(temp_table):
        if x == ' ':
            elements.append(i)
    move = random.choice(elements)
    temp_table[move] = sign
    table = [temp_table[size*i : size*(i+1)] for i in range(size)]
    table_print(table)
    return table

def check_winning_move(table,sign):
    index = -1
    if sign == 'X':
        opp_sign = 'O'
    else:
        opp_sign = 'X'
    for i in range(len(table)): 
        elements = table[i] # horizontal check
        if opp_sign in elements:
            pass
        elif len([x for x in elements if x == sign]) == 2:
            index = elements.index(' ') + i*len(table)
            break
        elements = [element[i] for element in table] # vertical check
        if opp_sign in elements:
            pass
        elif len([x for x in elements if x == sign]) == 2:
            index = elements.index(' ')*len(table) + i
            break
        if i == 0: # diagonal check
            elements = []
            winners = [0, 4, 8]
            for i in range(len(table)):
                elements.append(table[i][i])
            if opp_sign in elements:
                pass
            elif len([x for x in elements if x == sign]) == 2:
                index = winners[elements.index(' ')]
                break
            # other diagonal    
            elements = []
            winners = [2, 4, 6]
            for i in range(len(table)):
                elements.append(table[i][len(table)-1-i])
            if opp_sign in elements:
                pass
            elif len([x for x in elements if x == sign]) == 2:
                index = winners[elements.index(' ')]
                break  
    return index

def fill_coordinate_AI_medium(table,sign):
    print('Making move level "medium"')
    if sign == 'X':
        opp_sign = 'O'
    else:
        opp_sign = 'X'
    size = len(table)
    temp_table = [item for line in table for item in line]
    potential_win_move = check_winning_move(table,sign)
    if potential_win_move == -1:
        potential_block_move = check_winning_move(table,opp_sign)
        if potential_block_move == -1:
            elements = []
            for i,x in enumerate(temp_table):
                if x == ' ':
                    elements.append(i)
            move = random.choice(elements)
        else:
            move = potential_block_move
    else:
        move = potential_win_move
    temp_table[move] = sign
    table = [temp_table[size*i : size*(i+1)] for i in range(size)]
    table_print(table)
    return table

def fill_coordinate_AI_hard(table,sign):
    moves = []
    bestScore = -100
    bestMove = None
    org_sign = sign
    for i,x in enumerate([item for line in table for item in line]):
        if x == ' ':
            moves.append(i)
    for move in moves:
        temp_table = enter_move(move,table,sign)
        score = minimax(False,temp_table,sign,org_sign)
        if score > bestScore:
            bestScore = score
            bestMove = move
    table = enter_move(bestMove,table,sign)
    table_print(table)
    return table

def minimax(MaxTurn,table,sign,original_sign):
    done, winner = check_win(table,to_print=False)
    if sign == 'X':
        opp_sign = 'O'
    else:
        opp_sign = 'X'
    if done:
        if winner == original_sign:
            return 1
        elif winner == None:
            return 0
        else:
            return -1 
    scores = []
    moves = []
    for i,x in enumerate([item for line in table for item in line]):
        if x == ' ':
            moves.append(i)
    for move in moves:
        temp_table = enter_move(move,table,opp_sign)
        scores.append(minimax(not MaxTurn,temp_table,opp_sign,original_sign))
        temp_table = undo_move(move,table)
    return max(scores) if MaxTurn else min(scores)

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

def check_win(table,to_print=True):
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
        # print("Game not finished")
    elif winner == None and empty_elements == 0:
        done = True
        # print("Draw")
    else:
        done = True
        if to_print == True:
            print(f"{winner} wins")
    return done, winner

def play_game(player1,player2):
    done = False
    tic_tac_table = init_table(3)
    table_print(tic_tac_table)
    while not done:
        if player1 == 'user':
            tic_tac_table = fill_coordinate(tic_tac_table)
        elif player1 == 'easy':
            tic_tac_table = fill_coordinate_AI_easy(tic_tac_table,sign='X')
        elif player1 == 'medium':
            tic_tac_table = fill_coordinate_AI_medium(tic_tac_table,sign='X')
        elif player1 == 'hard':
            tic_tac_table = fill_coordinate_AI_hard(tic_tac_table,sign='X')
        done, winner = check_win(tic_tac_table)
        if done:
            break
        if player2 == 'user':
            tic_tac_table = fill_coordinate(tic_tac_table)
        elif player2 == 'easy':
            tic_tac_table = fill_coordinate_AI_easy(tic_tac_table,sign='O')
        elif player2 == 'medium':
            tic_tac_table = fill_coordinate_AI_medium(tic_tac_table,sign='O')
        elif player2 == 'hard':
            tic_tac_table = fill_coordinate_AI_hard(tic_tac_table,sign='O')
        done, winner = check_win(tic_tac_table)

exit_game = False
eligible_players = ("user","easy","medium","hard")
eligible_commands = ("start","exit")
while not exit_game:
    print("Input command:")
    selected_players = input()
    if selected_players == 'exit':
        exit_game = True
        break
    selected_players = selected_players.split()
    if len(selected_players) != 3:
        print("Bad parameters!")
    elif selected_players[0] not in eligible_commands \
        or selected_players[1] not in eligible_players \
        or selected_players[2] not in eligible_players:
        print("Bad parameters!") 
    else:
        play_game(selected_players[1],selected_players[2])       
