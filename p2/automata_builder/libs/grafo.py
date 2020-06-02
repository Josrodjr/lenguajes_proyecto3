from graphviz import Digraph

def graficadora(transiciones, estados_finales):
    f = Digraph('graph', filename='./graphs/graph.gv')
    f.attr(rankdir='LR', size='105')
    f.attr('node', shape='doublecircle')

    for i in range(len(estados_finales)):
        f.node(str(estados_finales[i][1]))
    
    f.attr('node', shape='circle')
    for i in range(len(transiciones)):
        f.edge(str(transiciones[i][0]), str(transiciones[i][2]), label= str(transiciones[i][1]))

    f.view()


# init_end = [[2, 2]]
# transitions = [[0, 'a', 1],[1, 'b', 2]]

# graficadora(transitions, init_end)
