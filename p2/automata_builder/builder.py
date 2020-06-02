import copy

from .libs.parser import parse_input
from .tree.node import Node

from .finite_automata.automata import automata_template, create_or, create_and, create_kleene, create_plus, create_qmark

# construct the tree based on the highest priority on the first level first

operators = ' |*+?'

precedence = {
    ' ': 0,
    '|': 0,
    '*': 2,
    '+': 1,
    '?': 0
}
# not isinstance(operation_array[0], Node) or

op_type = {
    ' ': 'bin',
    '|': 'bin',
    '*': 'un',
    '+': 'un',
    '?': 'un'
}

def create_node(operation_array):
    # construct of this node
    # created_node = Node(0,0,0)
    
    while len(operation_array) > 1:

        # run the entire list eliminating parenthesis
        for i in range(len(operation_array)):
            if isinstance(operation_array[i], list):
                new_node = create_node(operation_array[i])
                operation_array[i] = new_node
                # print(operation_array)
        
        # if everything is on the same level (no parenthesis exist)
        ocurrences = 0
        for value in operation_array:
            if isinstance(value, list):
                ocurrences += 1

        # nth loop after everything is either node or same level
        if ocurrences == 0:
            current_ops = []
            # get all the operands in this level
            for i in range(len(operation_array)):
                if not isinstance(operation_array[i], Node):
                    if operation_array[i] in operators:
                        current_ops.append([operation_array[i], i])

            # select the hightest precedence one and build the tree from it
            highest = current_ops[0]
            for value in current_ops[::-1]:
                if precedence[value[0]] >= precedence[highest[0]]:
                    highest = value

            # check if its bin or un
            curr_type = op_type[highest[0]]

            if curr_type == 'bin':
                # get next and previous value and build node
                l_value = copy.deepcopy(operation_array[highest[1]-1])
                r_value = copy.deepcopy(operation_array[highest[1]+1])

                # current spot in the list
                spot = highest[1]-1

                # pop from original array the values of both operands and the operator
                operation_array.pop(highest[1]+1)
                operation_array.pop(highest[1])
                operation_array.pop(highest[1]-1)


                node = Node(l_value, r_value, 0)
                node.add_operation(highest[0])

                operation_array.insert(spot, node)


            if curr_type == 'un':
                # get previous vaue and build node
                r_value = operation_array[highest[1]-1]

                # current spot in the list
                spot = highest[1]-1

                operation_array.pop(highest[1])
                operation_array.pop(highest[1]-1)

                node = Node(0, r_value, 0)
                node.add_operation(highest[0])

                operation_array.insert(spot, node)

    return operation_array[0]

def name_parents(tree, parent):

    if isinstance(tree.left, Node):
        # repeat this same method for the left side
        tree.parent = parent
        name_parents(tree.left, tree)
    else:
        # just name the last node and do not loop
        tree.parent = parent
        
    if isinstance(tree.right, Node):
        # repeat this same method for the right side
        tree.parent = parent
        name_parents(tree.right, tree)
    else:
        # just name the last node and do not loop
        tree.parent = parent


def get_highest(movement_list):
    curr_highest = 0
    for movement in movement_list:
        if movement[0] > curr_highest:
            curr_highest = movement[0]
        if movement[2] > curr_highest:
            curr_highest = movement[2] 

    return curr_highest


# transform the basic node to automata
# LEFT AND RIGHT NOT TYPE NODE
def automatize_Node(current_Node):
    left = current_Node.left
    right = current_Node.right
    operand = current_Node.operation

    if isinstance(current_Node.right, Node):
        right = current_Node.right.automata
    else:
        right = current_Node.right

    if isinstance(current_Node.left, Node):
        left = current_Node.left.automata
    else:
        left = current_Node.left
    
    if isinstance(right, dict):
        if isinstance(left, dict):
            left = renumber(left, right['start_end'][1][0])
            # delta = left['start_end'][1][0] + right['start_end'][1][0] 
            delta = get_highest(left['transitions']) + 7
        else:
            # delta = right['start_end'][1][0]
            delta = get_highest(right['transitions'])
    else:
        if isinstance(left, dict):
            left = renumber(left, 7)
        delta = 7

    # check the operation so we can raise a function based of this
    # CONCAT
    if operand == ' ':
        # raise a concat function and return the automata from this
        t_transitions, t_startend = copy.deepcopy(create_and([left, right], delta))
        t_automata = copy.deepcopy(automata_template)
        t_automata['start_end'] = t_startend
        t_automata['transitions'] = t_transitions
        return t_automata
    if operand == '|':
        # return an or statement automata from this node
        t_transitions, t_startend = copy.deepcopy(create_or([left, right], delta))
        t_automata = copy.deepcopy(automata_template)
        t_automata['start_end'] = t_startend
        t_automata['transitions'] = t_transitions
        return t_automata
    if operand == '*':
        # raise kleene function and return automata generated by it
        t_transitions, t_startend = copy.deepcopy(create_kleene([left, right], delta))
        t_automata = copy.deepcopy(automata_template)
        t_automata['start_end'] = t_startend
        t_automata['transitions'] = t_transitions
        return t_automata
    if operand == '+':
        # raise a plus funcion and return automata generate by it
        t_transitions, t_startend = copy.deepcopy(create_plus([left, right], delta))
        t_automata = copy.deepcopy(automata_template)
        t_automata['start_end'] = t_startend
        t_automata['transitions'] = t_transitions
        return t_automata
    if operand == '?':
        # raise a qmark function and return automata generated by it
        t_transitions, t_startend = copy.deepcopy(create_qmark([left, right], delta))
        t_automata = copy.deepcopy(automata_template)
        t_automata['start_end'] = t_startend
        t_automata['transitions'] = t_transitions
        return t_automata


def renumber(automata_dict, top_number):
    # change the numerator of each interation
    for state in automata_dict['start_end']:
        state[0] += top_number
        state[1] += top_number

    for transition in automata_dict['transitions']:
        transition[0] += top_number
        transition[2] += top_number
    
    return(automata_dict)


def create_automata_last(tree):

    if isinstance(tree.left, Node):
        # repeat this same method for the left side
        create_automata_last(tree.left)
    else:
        # check if right side is node or not
        if not isinstance(tree.right, Node):
            tree.automata = automatize_Node(tree)
        
    if isinstance(tree.right, Node):
        # repeat this same method for the right side
        create_automata_last(tree.right)
    else:
        if not isinstance(tree.left, Node):
            tree.automata = automatize_Node(tree)

def create_automata(tree):

    if isinstance(tree.left, Node):
        if isinstance(tree.right, Node):
            if len(tree.left.automata) != 0:
                if len(tree.right.automata) != 0:
                    # create this nodes automata with the data
                    tree.automata = automatize_Node(tree)
                else:
                    # no automata in the node
                    create_automata(tree.right)
            else:
                # no automata in the node
                create_automata(tree.left)
        else:
            # left side is node right side is not
            if len(tree.left.automata) != 0:
                tree.automata = automatize_Node(tree)
            else:
                # left side node without automata
                create_automata(tree.left)
    else:
        # left side not node
        if isinstance(tree.right, Node):
            if len(tree.right.automata) != 0:
                tree.automata = automatize_Node(tree)
            else:
                # left side not tree and right side without automata
                create_automata(tree.right)
        else:
            # left is not node, right is not either
            tree.automata = automatize_Node(tree)

def fill_tree(tree):
    # do bottom one time
    create_automata_last(tree)
    while len(tree.automata) == 0:
        # do leaves one by one from bottom
        create_automata(tree)

def after_automata_cleanup(tree):
    for value in tree.automata['transitions']:
        value[1] = int(value[1])

def automata_to_print_cleanup(tree):
    for value in tree.automata['transitions']:
        if value[1] != 0:
            value[1] = chr(value[1])