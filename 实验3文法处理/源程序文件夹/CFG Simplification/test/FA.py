from graphviz import Digraph
from copy import deepcopy
import sys

def is_regluar_grammer(p, vn):
    global left
    for production in p:
        for senten in production[1]:
            if len(senten) > 2:
                print('非线性规则')
                return False
            elif len(senten) == 2:
                if left == None:
                    if senten[0] in vn:
                        left = True
                    else:
                        left = False
                if left == True:  # 左线性，形如Aa,a
                    if senten[0] not in vn or senten[1] in vn:
                        print('产生式必须同时为左或右线性规则')
                        return False
                elif left == False:  # 右线性, 形如aA, a
                    if senten[0] in vn or senten[1] not in vn:
                        print('产生式必须同时为左或右线性规则')
                        return False
    return True


def finite_machine(p, s, fa):
    global left
    f = Digraph('有穷自动机', format='png')
    f.attr(rankdir='LR')
    f.attr('node', shape='doublecircle')
    if left:
        f.node(s)  # 开始节点画双圆
    else:  # 右线性规则添加结束节点
        f.node('End')

    f.attr('node', shape='circle')
    alplist = []
    if left:
        f.node('Start')  # 左线性规则添加开始节点
        addlist = deepcopy(fadict)
        fa.append(addlist)
        alplist.append('Start')

    for i in range(len(p)):
        addlist = deepcopy(fadict)
        fa.append(addlist)
        alplist.append(p[i][0])

    if left == False:
        addlist = deepcopy(fadict)
        fa.append(addlist)
    end = len(p)
    for production in p:
        for senten in production[1]:
            # 对于左线性规则，形如Q->a的每个规则，引一条从开始状态S到状态Q的弧，其标记为a;
            # 对于左线性规则，形如Q -> Ra的规则引一条从状态R到Q的弧，
            # 其标记为a。其中R为非终结符号，a为终结符号;
            # 右线性规则相反
            if left == True:
                if len(senten) == 1:
                    f.edge('Start', production[0], label=senten[0])
                    fa[0][senten[0]].append(alplist.index(production[0]))
                if len(senten) == 2:
                    f.edge(senten[0], production[0], label=senten[1])
                    fa[alplist.index(senten[0])][senten[1]].append(alplist.index(production[0]))


            if left == False:
                if len(senten) == 1:
                    f.edge(production[0], 'End', label=senten[0])
                    fa[alplist.index(production[0])][senten[0]].append(end)
                if len(senten) == 2:
                    f.edge(production[0], senten[1], label=senten[0])
                    fa[alplist.index(production[0])][senten[0]].append(alplist.index(senten[1]))

    f.render('./graph/finite_machine', view=False)


# vn = ['S', 'A', 'B', 'D']
# vt = ['a', 'b']
# s = 'S'
# p = [['S', [['a', 'A'], ['b', 'B']]],
#      ['A', [['b', 'B'], ['a', 'D'], ['a']]],
#      ['B', [['a', 'A'], ['b', 'D'], ['b']]],
#      ['D', [['a', 'D'], ['b', 'D'], ['a'], ['b']]]]
vn = ['Z', 'A', 'B']
vt = ['a', 'b']
s = 'Z'
p = [['Z', [['Z', 'a'], ['A', 'b'], ['B', 'a']]],
     ['A', [['B', 'b'], ['a']]],
     ['B', [['A', 'a'], ['b']]]]

left = None  # 判断左或右线性规则
nfa = []
dfa = []  # 存放dfa表
fadict = {} # 存放fa字典
nowset = {'now': set()}  # 存放当前状态集合
nowlist = []  # 存放所有状态集合
letter = vt  # 记录表达式中的字母
for alp in vt:
    fadict[alp] = []
    nowset[alp] = set()
fadict['#'] = []
notfinal = []  # 记录非终态
final = []  # 记录终态
mini_dfa_table = []  # 最小化dfa表
mini_dfa_d = dict()  # 最小化dfa字典
for alp in letter:  # 初始化字典
    mini_dfa_d[alp] = None
finish_split = []  # 已完成分割


if is_regluar_grammer(p, vn):
    finite_machine(p, s, nfa)


