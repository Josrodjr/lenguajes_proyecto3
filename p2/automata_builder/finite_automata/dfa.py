# transitions = ['a', 'b', ...]

# state_trans = {
#     'A': {
#         'state_id': {0,1,2,3},
#         'transitions': [['A', 'a', 'B'], ['A', 'b', 'B']]
#     },
#     'B': {
#         'state_id': {1,2,3,4},
#         'transitions': [['B', 'a', 'A'], ['B', 'b', 'B']]
#     }
# }

import copy
from ..libs.tform import get_eclosure, e_closure, mov, emulate_NFA, check_completion

transitions = []

# state_trans = {
# }

# approved_ids = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def fill_transitions(tree):
    transitions = tree.automata['transitions']
    trans = []

    for transition in transitions:
        if transition[1] != 0:
            if transition[1] not in trans:
                trans.append(transition[1])

    return trans


def iter_approved_ids(true_state_trans):
    if len(true_state_trans) == 0:
        return 1
    else:
        in_list = []
        for value in true_state_trans:
            in_list.append(value)
        in_list.sort()
        return in_list[-1] + 1



def iter_approved_ids_overload(local_state_trans):
    if len(local_state_trans) == 0:
        return 1
    else:
        in_list = []
        for value in local_state_trans:
            in_list.append(value)
        in_list.sort()
        return in_list[-1] + 1


def transitions_as_state(tree, state_trans_modified):
    # local transitions
    loctrans = fill_transitions(tree)
    # copy the state because we are iterating over the object
    iter_state_trans = copy.deepcopy(state_trans_modified)
    local_state_trans = copy.deepcopy(state_trans_modified)
    for reachable_state in iter_state_trans:
        for new_state_index in range(len(iter_state_trans[reachable_state]['transitions'])):
        # for new_state in iter_state_trans[reachable_state]['transitions']:
            # compare the state to the values stored in already known states
            found_state = 0
            for r_state in iter_state_trans:
                # esto esta de mas iterando sobre elementos del id
                # for states_identifiers in iter_state_trans[r_state]['state_id']:
                # print('A: ',iter_state_trans[reachable_state]['transitions'][new_state_index])
                # print('B: ',iter_state_trans[r_state]['state_id'])
                if iter_state_trans[reachable_state]['transitions'][new_state_index] == iter_state_trans[r_state]['state_id']:
                    # found a state that compares to the one found
                    found_state = r_state
            # change the values to our local copy
            if isinstance(local_state_trans[reachable_state]['transitions'][new_state_index], set):            
                if len(local_state_trans[reachable_state]['transitions'][new_state_index]) is 0:
                    local_state_trans[reachable_state]['transitions'][new_state_index] = 0
                    continue
                else:
                    if found_state != 0:
                        # found state that shares id with state pointed at it
                        # print("esto: ", local_state_trans[reachable_state]['transitions'][new_state_index])
                        # print("esto: ", iter_state_trans[found_state]['state_id'])
                        # if found_state == local_state_trans[reachable_state]:
                        # print('esto: ',local_state_trans[reachable_state])
                        # print('esto: ',found_state)
                        # if local_state_trans[reachable_state]['transitions'][new_state_index] == iter_state_trans[found_state]['state_id']:
                        #     # just remove the value from the transitions and continue
                        #     local_state_trans[reachable_state]['transitions'][new_state_index] = 0
                        # else:
                        local_state_trans[reachable_state]['transitions'][new_state_index] = found_state
                    else:
                        # find a new id for state and create new state
                        new_name_state = iter_approved_ids_overload(local_state_trans)
                        # check completion
                        complete_state = tree.automata['start_end'][1][0]
                        completion_state = check_completion(local_state_trans[reachable_state]['transitions'][new_state_index], complete_state)
                        # generate the transitions for this state
                        loc_transitions = []
                        for transition in loctrans:
                            mov_states = mov(tree.automata, local_state_trans[reachable_state]['transitions'][new_state_index], transition)
                            loc_transitions.append(mov_states)
                        # perform eclosure on the set to generate new node in tree
                        e_transitions = []
                        for transition in loc_transitions:
                            new_eclosure = set()
                            for value_transition in transition:
                                e_clos_values = get_eclosure(tree, value_transition)
                                for new_value in e_clos_values:
                                    new_eclosure.add(new_value)
                            e_transitions.append(new_eclosure)        
                        # insert the value to the local state trans
                        local_state_trans[new_name_state] = {
                            'state_id': local_state_trans[reachable_state]['transitions'][new_state_index],
                            'transitions': e_transitions,
                            'completion_state': completion_state
                        }
                        # remove the value from the previous tuple
                        local_state_trans[reachable_state]['transitions'][new_state_index] = new_name_state
    return local_state_trans


# def auto_fill_transitions():
def remove_transition_equal_id(object_check):
    for value in object_check:
        for transition_found in range(len(object_check[value]['transitions'])):
            if object_check[value]['state_id'] == object_check[value]['transitions'][transition_found]:
                object_check[value]['transitions'][transition_found] = value
    return object_check

def find_transition_in_object(object_check):
    for value in object_check:
        for transition_found in range(len(object_check[value]['transitions'])):
            # find in the whole object if any id is same as the one in transition
            # replace at
            # object_check[value]['transitions'][transition_found]
            for second_values in object_check:
                if object_check[value]['transitions'][transition_found] == object_check[second_values]['state_id']:
                    object_check[value]['transitions'][transition_found] = second_values
    return object_check
            

def check_if_continue_loop(object_check):
    for value in object_check:
        for transition_found in range(len(object_check[value]['transitions'])):
            if isinstance(object_check[value]['transitions'][transition_found], set):
                return 0
    return 1


def generate_dfa(tree):
    # isntantiate an empty dictionary
    true_state_trans = {}


    transitions = fill_transitions(tree)
    current_value = iter_approved_ids(true_state_trans)
    #perform a epsilon on the starting state of the nfa
    init_state = tree.automata['start_end'][0][0]
    complete_state = tree.automata['start_end'][1][0]
    # eclosure of first iteration
    first_transitions = get_eclosure(tree, init_state)
    # check if it is completion state
    completion_state = check_completion(first_transitions, complete_state)
    # generate the transitions for this state
    loc_transitions = []
    for transition in transitions:
        mov_states = mov(tree.automata, first_transitions, transition)
        loc_transitions.append(mov_states)
    # perform eclosure on the set to generate new node in tree
    e_transitions = []
    for transition in loc_transitions:
        new_eclosure = set()
        for value_transition in transition:
            e_clos_values = get_eclosure(tree, value_transition)
            for new_value in e_clos_values:
                new_eclosure.add(new_value)
        e_transitions.append(new_eclosure)        
    # append the values to the state_trans
    true_state_trans[current_value] = {
            'state_id': first_transitions,
            'transitions': e_transitions,
            'completion_state': completion_state
    }
    # TODO: remove state trans
    true_state_trans = true_state_trans
    comp_status = check_if_continue_loop(true_state_trans)
    while comp_status != 1:
        true_state_trans = transitions_as_state(tree, true_state_trans)
        true_state_trans = remove_transition_equal_id(true_state_trans)
        true_state_trans = find_transition_in_object(true_state_trans)
        comp_status = check_if_continue_loop(true_state_trans)

    return (true_state_trans, transitions)


def dfa_to_printable(dfa, trans):
    n_start_end = []
    n_transitions = []

    for state in dfa:
        # if its completion state append it to the printable completion states
        if dfa[state]['completion_state'] == 1:
            n_start_end.append([state, state])
        # generate the transitions in this state based on the trans arra
        for t in range(len(trans)):
            # different from zero because it points somewhere
            if dfa[state]['transitions'][t] != 0:
                n_transitions.append([state, trans[t], dfa[state]['transitions'][t]])

    return n_start_end, n_transitions