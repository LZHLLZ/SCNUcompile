def get_sentens(P, ch):  # 由非终结符获取规则
    for production in P:
        if production[0] == ch:
            return production[1]


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


# p = [['A',[['a','c'],['a','a','d'],['a','a','a','e'],['g']]]]
# vn = ['A', 'B']  # 非终结符
# p = [['A', [['B', 'a'], ['A', 'a'], ['c']]], ['B', [['B', 'b'], ['A', 'b'], ['d']]]]

vn = ['Z', 'S']  # 非终结符
vt = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
p = [['Z', [['Z', 'a'], ['S', 'b', 'c'], ['d', 'S']]], ['S', [['Z', 'e', 'f'], ['g', 'S', 'h']]]]
s = 'Z'

# vn = ['Z', 'A', 'B']
# vt = ['a', 'b']
# s = 'Z'
# p = [['Z', [['Z', 'a'], ['A', 'b'], ['B', 'a']]],
#      ['A', [['B', 'b'], ['a']]],
#      ['B', [['A', 'a'], ['b']]]]

left_common_factor(p)


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


from graphviz import Digraph
from copy import deepcopy


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


def finite_machine(p, s):
    global left
    f = Digraph('有穷自动机', format='png')
    f.attr(rankdir='LR')
    f.attr('node', shape='doublecircle')
    if left:
        f.node(s)  # 开始节点画双圆
    else:  # 右线性规则添加结束节点
        f.node('End')

    f.attr('node', shape='circle')
    if left:
        f.node('Start')  # 左线性规则添加开始节点
    for production in p:
        for senten in production[1]:
            # 对于左线性规则，形如Q->a的每个规则，引一条从开始状态S到状态Q的弧，其标记为a;
            # 对于左线性规则，形如Q -> Ra的规则引一条从状态R到Q的弧，
            # 其标记为a。其中R为非终结符号，a为终结符号;
            # 右线性规则相反
            if left == True:
                if len(senten) == 1:
                    f.edge('Start', production[0], label=senten[0])
                if len(senten) == 2:
                    f.edge(senten[0], production[0], label=senten[1])

            if left == False:
                if len(senten) == 1:
                    f.edge(production[0], 'End', label=senten[0])
                if len(senten) == 2:
                    f.edge(production[0], senten[1], label=senten[0])
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
if is_regluar_grammer(p, vn):
    finite_machine(p, s)
