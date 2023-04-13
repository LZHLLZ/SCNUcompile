from copy import deepcopy
from prettytable import PrettyTable


def draw_nfa_table(val):
    # ----------------------画nfa表----------------------
    nfatable = PrettyTable()
    dlist = list(val.d.keys())
    nfatable.field_names = ["序号"] + dlist
    for i in range(len(val.nfa)):
        row = [i]
        for j in dlist:
            if val.nfa[i][j]:
                row.append(val.nfa[i][j])
            else:
                row.append('')
        nfatable.add_row(row)
    nfatable.title = "nfa表"
    # print(nfatable)
    # print()


def draw_dfa_table(val):
    # --------------------画dfa表----------------------
    dfatable = PrettyTable()
    nowlist = list(val.nowset.keys())
    newnowlist = deepcopy(nowlist)
    newnowlist[0] = "状态集合"
    dfatable.field_names = newnowlist
    for i in range(len(val.dfa)):
        row = []
        for j in nowlist:
            if val.dfa[i][j]:
                row.append(val.dfa[i][j])
            else:
                row.append('')
        dfatable.add_row(row)
    dfatable.title = "dfa表"
    # print(dfatable)
    # print()


def draw_mini_dfa_table(val):
    # ----------------------画mini_dfa表---------------------
    mini_dfatable = PrettyTable()
    mini_dfalist = list(val.mini_dfa_d.keys())
    mini_dfatable.field_names = ["序号"] + mini_dfalist
    for i in range(len(val.mini_dfa_table)):
        row = [i]
        for j in mini_dfalist:
            if val.mini_dfa_table[i][j]:
                row.append(val.mini_dfa_table[i][j])
            else:
                row.append('')
        mini_dfatable.add_row(row)
    mini_dfatable.title = "最小化dfa表"
    # print(mini_dfatable)
    # print()
