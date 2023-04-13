from copy import deepcopy


# <------------------------- dfa表 ---------------------------->

def nfa2dfa(v):
    # 处理初态
    v.dfa.append(deepcopy(v.nowset))
    temp = list()
    v.dfa[0]['now'].add(0)
    v.dfa[0]['now'].update(v.nfa[0]['#'])
    temp += list(v.nfa[0]['#'])
    while temp:
        for i in v.nfa[temp.pop()]['#']:
            if i not in v.dfa[0]['now']:  # 防止递归
                temp.append(i)
                v.dfa[0]['now'].add(i)

    v.nowlist.append(v.dfa[0]['now'])
    if len(v.nfa) - 1 in v.dfa[0]['now']:
        v.final.append(v.dfa[0]['now'])

    num = 0  # 记录dfa行序号
    # 处理剩余状态
    while num != len(v.dfa):  # 说明dfa长度不再增加
        for i in v.dfa[num]['now']:
            for alp in v.letter:
                v.dfa[num][alp].update(v.nfa[i][alp])
        for alp in v.letter:
            temp = list(deepcopy(v.dfa[num][alp]))
            while temp:
                for i in v.nfa[temp.pop()]['#']:
                    if i not in v.dfa[num][alp]:  # 防止递归
                        temp.append(i)
                        v.dfa[num][alp].add(i)
            if v.dfa[num][alp] and v.dfa[num][alp] not in v.nowlist:
                v.nowlist.append(v.dfa[num][alp])
                d1 = deepcopy(v.nowset)
                d1['now'] = deepcopy(v.dfa[num][alp])
                v.dfa.append(deepcopy(d1))
                if len(v.nfa) - 1 in v.dfa[num][alp]:
                    v.final.append(v.dfa[num][alp])

        num += 1
    for i in v.nowlist:
        if i not in v.final:
            v.notfinal.append(i)
