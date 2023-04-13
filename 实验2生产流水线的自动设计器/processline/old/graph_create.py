from graphviz import Digraph


def draw_nfa_graph(val):
    f = Digraph('nfa表', format='png')
    f.attr(rankdir='LR')
    f.attr('node', shape='doublecircle')
    f.node(str(len(val.nfa) - 1))
    f.attr('node', shape='circle')
    for i in range(len(val.nfa) - 1):
        for alp in list(val.d.keys()):
            if val.nfa[i][alp]:
                for j in val.nfa[i][alp]:
                    if alp == '#':
                        f.edge(str(i), str(j), label=chr(949))  # epsilon
                    else:
                        f.edge(str(i), str(j), label=alp)
    f.render('./graph/nfa', view=False)


def draw_dfa_graph(val):
    f = Digraph('dfa表', format='png')
    f.attr(rankdir='LR')
    f.attr('node', shape='doublecircle')
    for i in val.final:
        f.node(str(val.nowlist.index(i)))
    f.attr('node', shape='circle')
    for i in range(len(val.dfa)):
        for alp in val.letter:
            if val.dfa[i][alp]:
                f.edge(str(i), str(val.nowlist.index(val.dfa[i][alp])), label=alp)
    f.render('./graph/dfa', view=False)


def draw_mini_dfa_graph(val):
    f = Digraph('mini_dfa表', format='png')
    f.attr(rankdir='LR')
    f.attr('node', shape='doublecircle')
    for i in range(len(val.mini_dfa_table)):
        if val.nowlist[i] in val.final:
            f.node(str(i))

    f.attr('node', shape='circle')
    for i in range(len(val.mini_dfa_table)):
        for alp in val.letter:
            if val.mini_dfa_table[i][alp]:
                f.edge(str(i), str(val.mini_dfa_table[i][alp]), label=alp)
    f.render('./graph/mini_dfa', view=False)
