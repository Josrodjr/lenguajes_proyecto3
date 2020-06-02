import copy

from libs.parser import parse_input, remove_empty, pre_parse_input
from tree.node import Node
from builder import create_node, name_parents, create_automata_last, create_automata, after_automata_cleanup, fill_tree, automata_to_print_cleanup
# in desuse
from tree.utils import FindDeepestNode


# try the print of the tree
from libs.print_tree import print2D
# try and print the nodes
from libs.grafo import graficadora
# get non_det functions
from finite_automata.automata import automata_template, create_or, create_and, create_kleene, create_plus, create_qmark
# transformations
from libs.tform import get_eclosure, e_closure, mov, emulate_NFA
# for txt generation
from libs.txtgen import get_params_for_txt, dict_to_txt
# for gui
from libs.gui import menu
# for DFA generation
from finite_automata.dfa import fill_transitions, iter_approved_ids, generate_dfa, dfa_to_printable

# base values
# regular_expression = '(b|b)* a b b (a|b)*'
regular_expression = 'A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|test'
# regular_expression = '0 1'
w_chain = '01'
exit = 0

while (exit == 0):
    menu()
    option = int(input("Option: "))
    if option == 1:
        regular_expression = input("Insert: ")
    if option == 2:
        w_chain = input("Insert: ")
    if option == 3:
        # get the array of parsed data
        operations = parse_input(regular_expression)
        operations = remove_empty(operations)
        # pre parse input array removing the epsion and replacing with zeroes

        # TODO: NO LONGER IN USE
        # operations = pre_parse_input(operations)

        # construct the tree based on the highest priority on the first level first
        tree = create_node(operations)
        # travel tree top down to assign parent to children
        name_parents(tree, 'root')
        # print the final state of the tree
        print2D(tree)
        # generate the automata of the tree and all leaves
        fill_tree(tree)
        # after fill replace all strings with ints

        # TODO: REMOVE THIS
        # after_automata_cleanup(tree)
        # hacer la simulacion del automata para una cadena de strings
        print("NFA on expression: ", emulate_NFA(w_chain, tree))
    if option == 4:
        dict_params = get_params_for_txt(tree)
        dict_to_txt(dict_params, 'automata_struct')
        # replace all values that are ints in transitions with the values that character produces

        fill_transitions(tree)
        
        dfa_generated, transitions = generate_dfa(tree)
        # print(dfa_generated)
        # print(transitions)
        dfa_startend, dfa_transitions = dfa_to_printable(dfa_generated, transitions)



        # TODO: REMOVE THIS
        # automata_to_print_cleanup(tree)
        # print using the nod lib
        # graficadora(tree.automata['transitions'], tree.automata['start_end'])
        graficadora(dfa_transitions, dfa_startend)



    if option == 0:
        exit = 1






