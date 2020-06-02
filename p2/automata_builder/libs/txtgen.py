import json

def get_estados(tree):
    transitions = tree.automata['transitions']
    states = set()

    for transition in transitions:
        states.add(transition[0])
        states.add(transition[2])
    
    return list(states)

def get_simbolos(tree):
    transitions = tree.automata['transitions']
    symbols = set()

    for transition in transitions:
        if transition[1] != 0:
            symbols.add(transition[1])
    
    return list(symbols)

def get_inicio(tree):
    start_end = tree.automata['start_end']
    return start_end[0][0]

def get_aceptacion(tree):
    start_end = tree.automata['start_end']
    return start_end[1][0]

def get_transiciones_importantes(tree):
    transitions = tree.automata['transitions']
    trans = []

    for transition in transitions:
        if transition[1] != 0:
            temp = [transition[0], transition[1], transition[2]]
            trans.append(temp)
    return trans

def get_params_for_txt(tree):
    # ESTADOS = {0, 1,... n}
    # SIMBOLOS = {a, b, c,... z}
    # INICIO = {0}
    # ACEPTACION = {0, 1,... n}
    # TRANSICION = (0, a, 1)-(0, e, 2)-... (3, b, n)
    complete_params = {
        'estados': get_estados(tree),
        'simbolos': get_simbolos(tree),
        'inicio': get_inicio(tree),
        'aceptacion': get_aceptacion(tree),
        'transiciones': get_transiciones_importantes(tree)
        }
    return complete_params


def dict_to_txt(dict, name):
    with open('./graphs/' + str(name) + '.txt', 'w') as file:
        file.write(json.dumps(dict))
    return 0