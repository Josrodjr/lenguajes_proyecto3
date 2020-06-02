
automata_template = {
    'start_end': [],
    'transitions': []
}
    
def create_or(operators, state_number):
    current_state_numerator = state_number
    start_end = [[1, 1], [7, 7]]
    transitions = [[1, 0, 2],[2, 0, 3], [2, 0, 5], [3, 'VAL1', 4], [5, 'VAL2', 6], [4,0,7], [6,0,7]]

    # change the numerator of each interation
    for state in start_end:
        state[0] += current_state_numerator
        state[1] += current_state_numerator

    for transition in transitions:
        transition[0] += current_state_numerator
        transition[2] += current_state_numerator

    if isinstance(operators[0], dict):
        # insert the list in the or sentence
        for transition in transitions:
            if transition[1] != 0:
                # add kleene operation from base node to start
                transition[1] = 0
                # create new transition from end 
                ending = [operators[0]['start_end'][1][0], 0, transition[2]]
                # point end to new start
                transition[2] = operators[0]['start_end'][0][0]
                # concat ending
                transitions.append(ending)
                # concat rest of nodes
                for movement in operators[0]['transitions']:
                    transitions.append(movement)
                break

    else:
        # the value is a single value so insert in place of VAL
        for transition in transitions:
            if transition[1] != 0 and transition[1] not in operators:
                transition[1] =  operators[0]
                break
    if isinstance(operators[1], dict):
        # insert the list in the or sentence
        for transition in transitions:
            if transition[1] != 0:
                # add kleene operation from base node to start
                transition[1] = 0
                # create new transition from end 
                ending = [operators[1]['start_end'][1][0], 0, transition[2]]
                # point end to new start
                transition[2] = operators[1]['start_end'][0][0]
                # concat ending
                transitions.append(ending)
                # concat rest of nodes
                for movement in operators[1]['transitions']:
                    transitions.append(movement)
                break
    else:
        # the value is a single value so insert in place of VAL
        for transition in transitions:
            if transition[1] != 0 and transition[1] not in operators:
                transition[1] =  operators[1]
                break

    return(transitions, start_end)

def create_and(operators, state_number):
    current_state_numerator = state_number
    start_end = [[1, 1], [4, 4]]
    transitions = [[1, 'VAL1', 2],[2, 0, 3], [3, 'VAL2', 4]]

    # change the numerator of each interation
    for state in start_end:
        state[0] += current_state_numerator
        state[1] += current_state_numerator

    for transition in transitions:
        transition[0] += current_state_numerator
        transition[2] += current_state_numerator

    if isinstance(operators[0], dict):
        # insert the list in the or sentence
        for transition in transitions:
            if transition[1] == 'VAL1':
                #TODO: set the start of the concat to the start the dictionary carries
                transition[1] = 0
                ending = [operators[0]['start_end'][1][0], 0, transition[2]]
                # point end to new start
                transition[2] = operators[0]['start_end'][0][0]
                # concat ending
                transitions.append(ending)

                for movement in operators[0]['transitions']:
                    transitions.append(movement)
                break

    else:
        for transition in transitions:
            if transition[1] == 'VAL1':
                transition[1] =  operators[0]    

    if isinstance(operators[1], dict):
        # insert the list in the and sentence
        for transition in transitions:
            if transition[1] == 'VAL2':
                #TODO: set the start of the concat to the start the dictionary carries
                transition[1] = 0
                ending = [operators[1]['start_end'][1][0], 0, transition[2]]
                # point end to new start
                transition[2] = operators[1]['start_end'][0][0]
                # concat ending
                transitions.append(ending)

                for movement in operators[1]['transitions']:
                    transitions.append(movement)
                break
    else:
        for transition in transitions:
            if transition[1] == 'VAL2':
                transition[1] =  operators[1]    

    return(transitions, start_end)

# KLEENE FIST OF OPERATORS EMPTY SECOND IS RIGHT
def create_kleene(operators, state_number):
    current_state_numerator = state_number
    start_end = [[1, 1], [4, 4]]
    transitions = [[1,0,2],[2, 'VAL1', 3], [3,0,4],[3,0,2],[1,0,4]]

    # change the numerator of each interation
    for state in start_end:
        state[0] += current_state_numerator
        state[1] += current_state_numerator
    for transition in transitions:
        transition[0] += current_state_numerator
        transition[2] += current_state_numerator

    if isinstance(operators[1], dict):
        # insert the list in the and sentence
        for transition in transitions:
            if transition[1] == 'VAL1':
                #TODO: set the start of the concat to the start the dictionary carries
                transition[1] = 0
                # ending concat with end
                ending = [operators[1]['start_end'][1][0], 0, transition[2]]
                # point end to new start
                transition[2] = operators[1]['start_end'][0][0]
                # concat ending
                transitions.append(ending)

                for movement in operators[1]['transitions']:
                    transitions.append(movement)
                break
    else:
        for transition in transitions:
            if transition[1] == 'VAL1':
                transition[1] =  operators[1]

    return(transitions, start_end)
     
# PLUS FIST OF OPERATORS EMPTY SECOND IS RIGHT
def create_plus(operators, state_number):
    current_state_numerator = state_number
    start_end = [[1, 1], [4, 4]]
    transitions = [[1,0,2],[2, 'VAL1', 3], [3,0,4],[3,0,2]]

    # change the numerator of each interation
    for state in start_end:
        state[0] += current_state_numerator
        state[1] += current_state_numerator
    for transition in transitions:
        transition[0] += current_state_numerator
        transition[2] += current_state_numerator

    if isinstance(operators[1], dict):
        # insert the list in the and sentence
        for transition in transitions:
            if transition[1] == 'VAL1':
                #TODO: set the start of the concat to the start the dictionary carries
                transition[1] = 0
                # ending concat with end
                ending = [operators[1]['start_end'][1][0], 0, transition[2]]
                # point end to new start
                transition[2] = operators[1]['start_end'][0][0]
                # concat ending
                transitions.append(ending)

                for movement in operators[1]['transitions']:
                    transitions.append(movement)
                
                

    else:
        for transition in transitions:
            if transition[1] == 'VAL1':
                transition[1] =  operators[1]

    return(transitions, start_end)

# QMARK FIST OF OPERATORS EMPTY SECOND IS RIGHT
def create_qmark(operators, state_number):
    current_state_numerator = state_number
    start_end = [[1, 1], [7, 7]]
    transitions = [[1, 0, 2],[2, 0, 3], [2, 0, 5], [3, 'VAL1', 4], [5,0,6], [4,0,7], [6,0,7]]

    # change the numerator of each interation
    for state in start_end:
        state[0] += current_state_numerator
        state[1] += current_state_numerator

    for transition in transitions:
        transition[0] += current_state_numerator
        transition[2] += current_state_numerator

    if isinstance(operators[1], dict):
        # insert the list in the or sentence
        for transition in transitions:
            if transition[1] != 0:
                # add kleene operation from base node to start
                transition[1] = 0
                # create new transition from end 
                ending = [operators[1]['start_end'][1][0], 0, transition[2]]
                # point end to new start
                transition[2] = operators[1]['start_end'][0][0]
                # concat ending
                transitions.append(ending)
                # concat rest of nodes
                for movement in operators[1]['transitions']:
                    transitions.append(movement)
                break
    else:
        # the value is a single value so insert in place of VAL
        for transition in transitions:
            if transition[1] != 0 and transition[1] not in operators:
                transition[1] =  operators[1]
                break

    return(transitions, start_end)

# test_dict = {
#     'start_end': [[8, 8], [14, 14]],
#     'transitions': [[8, 0, 9],[9, 0, 10], [9, 0, 12], [10, 'a', 11], [12, 'b', 13], [11,0,14], [13,0,14]]
# }
# graficadora(t1['transitions'], t1['start_end'])