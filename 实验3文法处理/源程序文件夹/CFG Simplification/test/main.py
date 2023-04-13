from copy import deepcopy

# from cfg import *

# 初始化，要记得以下格式
# vn = ['A']  # 非终结符
# vt = ['e', 'f', 'c', 'g']  # 终结符
# p = [['A', 'ac'], ['A', 'aae'], ['A', 'aaaf'], ['A', 'g']]
# s = 'A'  # 起始符
vn = ['S', 'B', 'A', 'C', 'D']
p = [['S', 'Be'], ['B', 'Ce'], ['B', 'Af'],  # 产生式
     ['A', 'Ae'], ['A', 'e'], ['C', 'Cf'], ['D', 'f']]
vt = ['e', 'f']
s = 'S'


# 合并规则
def merge_P(p):
    P = []
    used = []
    for i in range(len(p)):
        merge = []
        if p[i][0] not in used and (p[i][1] not in merge):
            merge.append(p[i][1])
            for j in p[i + 1:]:
                if j[0] == p[i][0] and (j[1] not in merge):
                    merge.append(j[1])
            P.append([p[i][0], merge])
            # P.append([p[i][0],'|'.join(merge)])
            used.append(p[i][0])

    p.clear()
    p.extend(P[:])


merge_P(p)


def get_sentens(P, ch):  # 由非终结符获取规则
    for production in P:
        if production[0] == ch:
            return production[1]


def if_senten_tofinal(senten, used_ch):  # 判断一个规则能否推出终结符
    for ch in senten:
        if ch in used_ch:  # 阻止循环
            return False
        if ch in vn:  # 若某个字符无法推到终结符返回False
            if not is_tofinal(ch, set()):
                return False
    return True


def is_tofinal(ch, used_ch):  # 判断一个非终结字符的能否推出终结符
    if ch in used_ch:  # 阻止循环
        return False
    used_ch.add(ch)
    for senten in get_sentens(p, ch):  # 判断每个规则，若某个规则能推出终结符返回True
        if if_senten_tofinal(senten, used_ch):
            return True
    return False


def delete_ch(P, ch):  # 删除与终结字符有关的规则
    temp = []
    for production in P:
        sentens = []
        if production[0] != ch:
            for senten in production[1]:
                if not senten.count(ch):
                    sentens.append(senten)
            if sentens:
                temp.append([production[0], sentens])

    P.clear()
    P.extend(temp[:])
    vn.remove(ch)


# 化简文法
def simplify_cfg(p):
    # 先删除有害规则
    P = []
    for production in p:
        sentens = []
        for senten in production[1]:
            if production[0] != senten:
                sentens.append(senten)
        if sentens:
            P.append([production[0], sentens])
    p.clear()
    p.extend(P[:])
    # 删除多余规则
    # 1.判断左边非终结符能推出终结符
    for production in p:
        used_ch = set()
        if not is_tofinal(production[0], used_ch):
            delete_ch(P, production[0])
    p.clear()
    p.extend(P[:])
    # 2.判断非终结符是否在某句型出现
    exist = []  # 判断句型中存在的终结符
    for production in p:
        for senten in production[1]:
            for ch in senten:
                if ch in vn:
                    exist.append(ch)
    dele = set(vn) - set(exist)
    dele.remove(s)  # 起始符不要删
    for i in dele:
        delete_ch(p, i)

    # 删除不存在的终结符
    exist = []
    for production in p:
        for senten in production[1]:
            for ch in senten:
                if ch in vt:
                    exist.append(ch)
    dele = set(vt) - set(exist)
    for i in dele:
        vt.remove(i)


simplify_cfg(p)


# %%

def mfun2(strs):  # 寻找列表的最长公共子串
    l = []
    for i in strs:  # 列表转化为字符串
        l.append(''.join(i))
    ans = ''  # 定义空字符串，准备用来存放最长公共子串
    for i in zip(*l):  # *l 将列表解包成几个字符串元素
        if len(set(i)) == 1:  # 判断zip后的元素的集合的长度，如果=1，
            ans += i[0]  # 说明几个字母相等，追加到最长公共子串中
        else:  # 否则就是不相等。
            break
    return ans


def switch_structure(p):  # 改变p的存储结构
    P = []
    for production in p:
        sentens = []
        for senten in production[1]:
            sentens.append(list(senten))
        P.append([production[0], sentens])

    p.clear()
    p.extend(P[:])


switch_structure(p)


# 消除左公因子
def left_common_factor(p):
    P = []
    for i, production in enumerate(p):
        merged = []
        sentens = []
        newproduction = []
        notmerged = []
        # l: 要进行合并的规则
        # merged: 已经合并过的规则
        # sentens: 合并后的规则
        # newproduction: 新产生的规则
        # notmerged：没有合并的规则
        for j, senten1 in enumerate(production[1]):
            l = []
            if senten1 in merged:
                continue
            l.append(senten1)
            for senten2 in production[1][j + 1:]:
                l.append(senten2)
                if not mfun2(l):  # 无法合并
                    l.pop()

            if len(l) > 1:  # 可以合并
                merged.extend(l[:])
                newsentens = []
                samestr = mfun2(l)
                samestrlist = list(samestr)
                samestrlist.append(production[0] + str(i))
                sentens.append(samestrlist)
                for senten3 in l:
                    newsentens.append(senten3[len(samestr):])
                newproduction.append([production[0] + str(i), newsentens])
                vn.append(production[0] + str(i))
            else:
                notmerged.append(l.pop())

        sentens += notmerged
        P.append([production[0], sentens])  # 合并后的规则
        P.extend(newproduction)  # 加入新规则
    if len(p) != len(P):
        p.clear()
        p.extend(P[:])
        left_common_factor(p)  # 递归处理直到没有相同前缀


# 左公
# p = [['A',[['a','c'],['a','a','d'],['a','a','a','e'],['g']]]]
# vn = ['A', 'B']  # 非终结符
# p = [['A', [['B', 'a'], ['A', 'a'], ['c']]], ['B', [['B', 'b'], ['A', 'b'], ['d']]]]
# 左递归
# vn = ['Z', 'S']  # 非终结符
# vt = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
# p = [['Z', [['Z', 'a'], ['S', 'b', 'c'], ['d', 'S']]], ['S', [['Z', 'e', 'f'], ['g', 'S', 'h']]]]
# s = 'Z'
# FA
# vn = ['Z', 'A', 'B']
# vt = ['a', 'b']
# s = 'Z'
# p = [['Z', [['Z', 'a'], ['A', 'b'], ['B', 'a']]],
#      ['A', [['B', 'b'], ['a']]],
#      ['B', [['A', 'a'], ['b']]]]

left_common_factor(p)


# %%
# 左公
# p = [['A',[['a','c'],['a','a','d'],['a','a','a','e'],['g']]]]
# vn = ['A', 'B']  # 非终结符
# p = [['A', [['B', 'a'], ['A', 'a'], ['c']]], ['B', [['B', 'b'], ['A', 'b'], ['d']]]]
# 左递归
# vn = ['Z', 'S']  # 非终结符
# vt = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
# p = [['Z', [['Z', 'a'], ['S', 'b', 'c'], ['d', 'S']]], ['S', [['Z', 'e', 'f'], ['g', 'S', 'h']]]]
# vn = ['Z', 'A', 'B']
# vt = ['a', 'b']
# s = 'Z'
# p = [['Z', [['Z', 'a'], ['A', 'b'], ['B', 'a']]],
#      ['A', [['B', 'b'], ['a']]],
#      ['B', [['A', 'a'], ['b']]]]
def if_recursion(P, left_ch, production, used_ch):
    for senten in production:
        if senten[0] == left_ch:
            return True
        if left_ch in used_ch:
            return False
        if senten[0] in vn:
            used_ch.add(left_ch)
            if if_recursion(P, senten[0], get_sentens(P, senten[0]), used_ch):
                return True
    return False


# 消除左递归
def left_recursion(p):
    P = []
    finished = []  # 已解决的终结符
    for i, production in enumerate(p):
        sentens = []  # 原来已改变的句型
        newsentens = []  # 新句型
        deal_sentens = []  # 要处理递归的句型:[[],[]]
        used_ch = set()
        # 判断该产生式是否有递归
        if if_recursion(p, production[0], production[1], used_ch):
            for j, senten1 in enumerate(production[1]):  # 代入已解决的终结符
                if senten1[0] in vn and senten1[0] in finished:
                    substitude = get_sentens(P, senten1[0])
                    for senten in substitude:
                        deal_sentens.append(senten + senten1[1:])
                else:
                    deal_sentens.append(senten1)

            for senten in deal_sentens:
                if senten[0] != production[0]:  # 非递归
                    sentens.append(senten + [production[0] + str(i)])
                else:
                    newsentens.append(senten[1:] + [production[0] + str(i)])
            newsentens.append(['@'])  # 表示空串

            P.append([production[0], sentens])
            P.append([production[0] + str(i), newsentens])
            finished.append(production[0])
            vn.append(production[0] + str(i))
        else:
            P.append(production)

    p.clear()
    p.extend(P[:])


left_recursion(p)


# %%

# FA
# vn = ['Z', 'A', 'B']
# vt = ['a', 'b']
# s = 'Z'
# p = [['Z', [['Z', 'a'], ['A', 'b'], ['B', 'a']]],
#      ['A', [['B', 'b'], ['a']]],
#      ['B', [['A', 'a'], ['b']]]]

def find_first(p, left_ch, ch_first, used_ch):
    for senten in get_sentens(p, left_ch):
        if senten[0] in used_ch:  # 防止无限递归
            return False
        if senten[0] not in vn:
            ch_first.add(senten[0])
        else:
            used_ch.add(senten[0])
            if not find_first(p, senten[0], ch_first, used_ch):
                continue


def get_first(p, first):
    for production in p[::-1]:  # 自底向上减少推导
        if production[0] not in vn:  # 只处理非终结符
            continue
        if production[0] not in first:  # 未加入的加入
            first[production[0]] = set()
        for senten in production[1]:
            if senten[0] not in vn:  # 终结符加入集合
                first[production[0]].add(senten[0])
            else:
                if senten[0] in first:  # 已经在first集合中
                    first[production[0]].update(first[senten[0]])
                    continue
                # 不在first集合中
                used_ch = set()
                find_first(p, production[0], first[production[0]], used_ch)


first = dict()
get_first(p, first)
# 倒转字典
keys = list(first.keys())
values = list(first.values())
keys.reverse()
values.reverse()
first = dict(zip(keys, values))

follow = dict()


def find_follow(p, ch, first, ch_follow, vn, s):
    for production in p:
        for senten in production[1]:
            if senten.count(ch):
                if senten.index(ch) == len(senten) - 1:
                    if ch != production[0]:
                        find_follow(p, production[0], first, ch_follow, vn, s)
                elif senten[senten.index(ch) + 1] in vn:
                    # 添加非空first集合
                    ch_follow.update(first[senten[senten.index(ch) + 1]] - {'@'})
                else:  # 添加终结符
                    ch_follow.add(senten[senten.index(ch) + 1])


def get_follow(p, first, follow, vn, s):
    for ch in vn:
        follow[ch] = set()
        for production in p:
            for senten in production[1]:
                if senten.count(ch):  # 句型中有目标字符
                    # 非终结符后面没有任何符号的情况
                    if senten.index(ch) == len(senten) - 1:
                        # follow[ch].add(production[0])   # 后续follow集合加入
                        if ch != production[0]:
                            find_follow(p, production[0], first, follow[ch], vn, s)
                    elif senten[senten.index(ch) + 1] in vn:
                        # 添加非空first集合
                        follow[ch].update(first[senten[senten.index(ch) + 1]] - {'@'})
                    else:  # 添加终结符
                        follow[ch].add(senten[senten.index(ch) + 1])
        if ch == s:  # 起始符添加空串
            follow[ch].add('@')


get_follow(p, first, follow, vn, s)

#%%
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

#FA
left = None
vn = ['S', 'A', 'B', 'D']
vt = ['a', 'b']
s = 'S'
p = [['S', [['a', 'A'], ['b', 'B']]],
     ['A', [['b', 'B'], ['a', 'D'], ['a']]],
     ['B', [['a', 'A'], ['b', 'D'], ['b']]],
     ['D', [['a', 'D'], ['b', 'D'], ['a'], ['b']]]]
# vn = ['Z', 'A', 'B']
# vt = ['a', 'b']
# s = 'Z'
# p = [['Z', [['Z', 'a'], ['A', 'b'], ['B', 'a']]],
#      ['A', [['B', 'b'], ['a']]],
#      ['B', [['A', 'a'], ['b']]]]

nfa = []
dfa = []  # 存放dfa表
fadict = {}  # 存放fa字典
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

# nfa2dfa()
