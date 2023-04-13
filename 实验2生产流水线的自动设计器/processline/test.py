from copy import deepcopy
from prettytable import PrettyTable
from graphviz import Digraph
import sys


# <----------------------- nfa表 -------------------------->

def star(s):  # 处理闭包*
    nfa.append(deepcopy(d))
    record1 = len(nfa) - 1
    # nfa[record1]['#'].append(record1 + 1)
    if len(s) > 1:  # 长字符串处理
        transnfa(s)
    else:
        single(s)  # 处理单个字符
    record2 = len(nfa) - 1
    nfa[record2]['#'].append(record1 + 1)
    nfa.append(deepcopy(d))
    nfa[record2]['#'].append(record2 + 1)
    nfa[record1]['#'].append(record2 + 1)


def plus(s):  # 处理正闭包+
    nfa.append(deepcopy(d))
    record1 = len(nfa) - 1
    # nfa[record1]['#'].append(record1 + 1)
    if len(s) > 1:
        transnfa(s)
    else:
        single(s)
    record2 = len(nfa) - 1
    nfa[record2]['#'].append(record1 + 1)
    nfa.append(deepcopy(d))
    nfa[record2]['#'].append(record2 + 1)


def selectable(s):  # 处理可选 ?
    record1 = len(nfa)
    if len(s) > 1:
        transnfa(s)
    else:
        single(s)
    nfa[record1]['#'].append(len(nfa) - 1)

def link():
    nfa[-1]['#'].append(len(nfa))

def choose(s):  # 处理选择字符|，|将字符串分为两个部分
    last = s[:s.find('|')]
    next = s[s.find('|') + 1:]
    nfa.append(deepcopy(d))
    record1 = len(nfa) - 1
    if record1 != 0:
        nfa[record1 - 1]['#'].append(record1)
    nfa[record1]['#'].append(record1 + 1)
    transnfa(last)
    record2 = len(nfa) - 1
    nfa[record1]['#'].append(record2 + 1)
    transnfa(next)
    nfa.append(deepcopy(d))
    nfa[record2]['#'].append(len(nfa) - 1)
    nfa[len(nfa) - 2]['#'].append(len(nfa) - 1)


def single(s):  # 处理单字符
    nfa.append(deepcopy(d))
    nfa.append(deepcopy(d))
    nfa[-2][s].append(len(nfa) - 1)


def pure(s):  # 字符串中没有|和（）的情况
    if len(s) == 0:
        return
    if len(s) == 1:
        single(s)
        return
    for i in range(len(s) - 1):
        if s[i].isalpha() and s[i + 1].isalpha():
            single(s[i])
        if s[i + 1] == '*':
            star(s[i])
        if s[i + 1] == '+':
            plus(s[i])
        if s[i + 1] == '?':
            selectable(s[i])
        if s[i + 1] == '.':
            single(s[i])
            link()

    if s[len(s) - 1].isalpha():
        single(s[len(s) - 1])


def findrbacket(s):  # 根据'('找到对应')'的位置
    count = 1
    for i in range(s.find('(') + 1, len(s)):
        if s[i] == '(':
            count += 1
        if s[i] == ')':
            count -= 1
            if count == 0:
                return i


def transnfa(s):  # 开始处理正则表达式
    lbacket = s.find('(')
    rbacket = s.find(')')
    if lbacket > 0:
        rbacket = findrbacket(s)
    # 先对 | 和 （） 处理
    if s.find('|') != -1 and ((s.find('|') < lbacket) or (s.find('|') > rbacket)):
        choose(s)
    elif lbacket != -1:
        last = s[:lbacket]
        newstr = s[lbacket + 1:rbacket]
        next1 = s[rbacket + 1:]
        next2 = s[rbacket + 2:]
        pure(last)
        if rbacket == len(s) - 1:  # 括号为字符串结束的情况
            transnfa(newstr)
        if rbacket < len(s) - 1:  # 括号后有特殊字符的情况
            if s[rbacket + 1] == '*':
                star(newstr)
            elif s[rbacket + 1] == '+':
                plus(newstr)
            elif s[rbacket + 1] == '?':
                selectable(newstr)
            elif s[rbacket + 1] == '.':
                transnfa(newstr)
                link()
            else:
                transnfa(newstr)
                transnfa(next1)
                return
        transnfa(next2)
    else:
        pure(s)


#   transnfa(s)

# <------------------------- dfa表 ---------------------------->

def nfa2dfa():
    # 处理初态
    dfa.append(deepcopy(nowset))
    temp = list()
    dfa[0]['now'].add(0)
    dfa[0]['now'].update(nfa[0]['#'])
    temp += list(nfa[0]['#'])
    while temp:
        for i in nfa[temp.pop()]['#']:
            if i not in dfa[0]['now']:  # 防止递归
                temp.append(i)
                dfa[0]['now'].add(i)

    nowlist.append(dfa[0]['now'])
    if len(nfa) - 1 in dfa[0]['now']:
        final.append(dfa[0]['now'])

    num = 0  # 记录dfa行序号
    # 处理剩余状态
    while num != len(dfa):  # 说明dfa长度不再增加
        for i in dfa[num]['now']:
            for alp in letter:
                dfa[num][alp].update(nfa[i][alp])
        for alp in letter:
            temp = list(deepcopy(dfa[num][alp]))
            while temp:
                for i in nfa[temp.pop()]['#']:
                    if i not in dfa[num][alp]:  # 防止递归
                        temp.append(i)
                        dfa[num][alp].add(i)
            if dfa[num][alp] and dfa[num][alp] not in nowlist:
                nowlist.append(dfa[num][alp])
                d1 = deepcopy(nowset)
                d1['now'] = deepcopy(dfa[num][alp])
                dfa.append(deepcopy(d1))
                if len(nfa) - 1 in dfa[num][alp]:
                    final.append(dfa[num][alp])

        num += 1
    for i in nowlist:
        if i not in final:
            notfinal.append(i)


#   nfa2dfa()

# <------------------------- 最小化dfa表 --------------------------->

def mini_dfa():
    classfy = []
    used = []
    # 将非终态集合分类
    for i in range(1, len(dfa)):
        if i in used:
            continue
        label = [i]
        used.append(i)
        flag = True
        for j in range(i + 1, len(dfa)):
            if j in used:
                continue
            for alp in letter:
                if dfa[i][alp] != dfa[j][alp]:
                    flag = False
                    break
            if flag:
                label.append(j)
                used.append(j)
        classfy.append(label)

    classfy.insert(0, [0])  # 向前插入第0类
    for i in range(len(classfy)):  # 先分配好所有的点
        mini_dfa_table.append(deepcopy(mini_dfa_d))
    for i in range(len(dfa)):
        for alp in letter:
            if dfa[i][alp] in nowlist:
                idx = nowlist.index(dfa[i][alp])
                classidx = None  # 记录指向的类别
                nowidx = None  # 记录当前的类别
                for j in range(len(classfy)):
                    if idx in classfy[j]:
                        classidx = j
                    if i in classfy[j]:
                        nowidx = j
                mini_dfa_table[nowidx][alp] = classidx


# def classfy(notfinal):  # -->[notfinal, final]
#     fin = []
#     notfin = []
#     for i in notfinal:
#         nowidx = nowlist.index(i)
#         for alp in letter:
#             if i and (i not in fin) and (dfa[nowidx][alp] not in notfinal):
#                 fin.append(i)
#     for i in notfinal:
#         if i not in fin:
#             notfin.append(i)
#     return [notfin, fin]
#
#
# def mini_dfa(notfinal, final):
#     classid = [notfinal, final]
#     while True:
#         l = classfy(notfinal)
#         if l[1] == []:
#             break
#         else:
#             if isinstance(final[0], set):
#                 final = [final]
#             final = [l[1]] + final
#             notfinal = l[0]
#         if l[0]:
#             if isinstance(final[0], set):
#                 final = [final]
#             classid = [l[0]] + final
#     print(classid)
#     for i in range(len(classid)):  # 先分配好所有的点
#         mini_dfa_table.append(deepcopy(mini_dfa_d))
#
#     for dfad in dfa:
#         for alp in letter:
#             if dfad[alp] in nowlist:
#                 fromidx = None
#                 toidx = None
#                 for i in range(len(classid)):
#                     if dfad['now'] in classid[i]:
#                         fromidx = i
#                     if dfad[alp] in classid[i]:
#                         toidx = i
#                 mini_dfa_table[fromidx][alp] = toidx
# def transform(s, alp):
#     nowidx = nowlist.index(s)
#     return dfa[nowidx][alp]
#
#
# def decompose(s):  # --> [[],[]]
#     for alp in letter:
#         notfin = []
#         fin = []
#         for subset in s:
#             aftertan = transform(subset, alp)
#             if aftertan in notfinal:
#                 notfin.append(subset)
#             else:
#                 fin.append(subset)
#         if notfin != [] and fin != []:
#             return [notfin, fin]  # 可再分
#     return False
#
#
# def mini_dfa(notfinal, final):
#     notfin = [deepcopy(notfinal)]
#     fin = [deepcopy(final)]
#     classid = []
#     while notfin != []:
#         l1 = notfin.pop()
#         l2 = decompose(l1)
#         if l2:
#             notfin += l2
#         else:
#             classid += [l1]
#     while fin != []:
#         l1 = fin.pop()
#         l2 = decompose(l1)
#         if l2:
#             fin += l2
#         else:
#             classid += [l1]
#     print(classid)
#     for i in range(len(classid)):  # 先分配好所有的点
#         mini_dfa_table.append(deepcopy(mini_dfa_d))
#
#     for dfad in dfa:
#         for alp in letter:
#             if dfad[alp] in nowlist:
#                 fromidx = None
#                 toidx = None
#                 for i in range(len(classid)):
#                     if dfad['now'] in classid[i]:
#                         fromidx = i
#                     if dfad[alp] in classid[i]:
#                         toidx = i
#                 mini_dfa_table[fromidx][alp] = toidx
def draw_nfa_table():
    # ----------------------画nfa表----------------------
    nfatable = PrettyTable()
    dlist = list(d.keys())
    nfatable.field_names = ["序号"] + dlist
    for i in range(len(nfa)):
        row = [i]
        for j in dlist:
            if nfa[i][j]:
                row.append(nfa[i][j])
            else:
                row.append('')
        nfatable.add_row(row)
    nfatable.title = "nfa表"
    print(nfatable)
    print()


def draw_dfa_table():
    # --------------------画dfa表----------------------
    dfatable = PrettyTable()
    nowlist = list(nowset.keys())
    newnowlist = deepcopy(nowlist)
    newnowlist[0] = "状态集合"
    dfatable.field_names = newnowlist
    for i in range(len(dfa)):
        row = []
        for j in nowlist:
            if dfa[i][j]:
                row.append(dfa[i][j])
            else:
                row.append('')
        dfatable.add_row(row)
    dfatable.title = "dfa表"
    print(dfatable)
    print()


def draw_mini_dfa_table():
    # ----------------------画mini_dfa表---------------------
    mini_dfatable = PrettyTable()
    mini_dfalist = list(mini_dfa_d.keys())
    mini_dfatable.field_names = ["序号"] + mini_dfalist
    for i in range(len(mini_dfa_table)):
        row = [i]
        for j in mini_dfalist:
            if mini_dfa_table[i][j]:
                row.append(mini_dfa_table[i][j])
            else:
                row.append('')
        mini_dfatable.add_row(row)
    mini_dfatable.title = "最小化dfa表"
    print(mini_dfatable)
    print()


def draw_nfa_graph():
    f = Digraph('nfa表', filename='nfa.gv')
    f.attr(rankdir='LR')
    f.attr('node', shape='doublecircle')
    f.node(str(len(nfa) - 1))
    f.attr('node', shape='circle')
    for i in range(len(nfa) - 1):
        for alp in list(d.keys()):
            if nfa[i][alp]:
                for j in nfa[i][alp]:
                    if alp == '#':
                        f.edge(str(i), str(j), label=chr(949))  # epsilon
                    else:
                        f.edge(str(i), str(j), label=alp)
    f.view()


def draw_dfa_graph():
    f = Digraph('dfa表', filename='dfa.gv')
    f.attr(rankdir='LR')
    f.attr('node', shape='doublecircle')
    for i in final:
        f.node(str(nowlist.index(i)))
    f.attr('node', shape='circle')
    for i in range(len(dfa)):
        for alp in letter:
            if dfa[i][alp]:
                f.edge(str(i), str(nowlist.index(dfa[i][alp])), label=alp)
    f.view()


def draw_mini_dfa_graph():
    f = Digraph('mini_dfa表', filename='mini_dfa.gv')
    f.attr(rankdir='LR')
    f.attr('node', shape='doublecircle')
    for i in range(len(mini_dfa_table)):
        if nowlist[i] in final:
            f.node(str(i))

    f.attr('node', shape='circle')
    for i in range(len(mini_dfa_table)):
        for alp in letter:
            if mini_dfa_table[i][alp]:
                f.edge(str(i), str(mini_dfa_table[i][alp]), label=alp)
    f.view()


def links(s):
    l = list(s)
    l1 = l[::-1]
    l2 = []
    afterlink = ''
    while l1:
        ch = l1.pop()
        if l2:
            if ch == '(' and l2 and l2[-1] != '(':
                l2.append('.')
                l2.append(ch)
                continue
            if l2[-1] == '*' or l2[-1] == '+' or l2[-1] == '?':
                l2.append('.')
                l2.append(ch)
                continue
            if ch.isalpha() and (l2[-1] == ')' or l2[-1].isalpha()):
                l2.append('.')
                l2.append(ch)
                continue
        l2.append(ch)
    for i in l2:
        afterlink += i
    return afterlink


if __name__ == '__main__':
    #    while True:
    print("生产流水线的自动规划器")
    print("1.打开文件")
    print("2.输入正则表达式")
    print("3.退出")
    number = input()
    s = ""
    if number == '1':
        path = input("请输入文件的路径\n")
        f = open(path, "r")
        s = f.read()
        f.close()
    elif number == '2':
        s = input("请输入正确的正则表达式\n")
        select = input("是否保存该正则表达式？(y/n)")
        if select == 'y':
            f = open("re.txt", 'w')
            f.write(s)
            print("文件已保存为当前目录的re.txt文件")
    else:
        sys.exit()

    d = {}  # 记录nfa字典
    nfa = []  # 存放nfa表
    inchoose = False  # 判断可选 |

    dfa = []  # 存放dfa表
    nowset = {'now': set()}  # 存放当前状态集合
    nowlist = []  # 存放所有状态集合
    letter = []  # 记录表达式中的字母

    for i in s:  # 记录非特殊字符
        if i.isalpha():
            if i not in letter:
                letter.append(i)
                d[i] = []
                nowset[i] = set()
    d['#'] = []
    mini_dfa_table = []  # 最小化dfa表
    mini_dfa_d = dict()  # 最小化dfa字典
    for alp in letter:  # 初始化字典
        mini_dfa_d[alp] = None
    notfinal = []  # 记录非终态
    final = []  # 记录终态

    s = links(s)
    #   构建表
    transnfa(s)
    nfa2dfa()
    mini_dfa()
    #   绘制表
    draw_nfa_table()
    draw_dfa_table()
    draw_mini_dfa_table()
    # #   绘制图
    # draw_nfa_graph()
    # draw_dfa_graph()
    # draw_mini_dfa_graph()
