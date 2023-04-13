from copy import deepcopy


# <----------------------- nfa表 -------------------------->
def transnfa(val, s):  # 开始处理正则表达式
    lbacket = s.find('(')
    rbacket = s.find(')')
    if lbacket > 0:
        rbacket = findrbacket(s)
    # 先对 | 和 （） 处理
    if s.find('|') != -1 and ((s.find('|') < lbacket) or (s.find('|') > rbacket)):
        choose(val, s)
    elif lbacket != -1:
        last = s[:lbacket]
        newstr = s[lbacket + 1:rbacket]
        next1 = s[rbacket + 1:]
        next2 = s[rbacket + 2:]
        pure(val, last)
        if rbacket == len(s) - 1:  # 括号为字符串结束的情况
            transnfa(val, newstr)
        if rbacket < len(s) - 1:  # 括号后有特殊字符的情况
            if s[rbacket + 1] == '*':
                star(val, newstr)
            elif s[rbacket + 1] == '+':
                plus(val, newstr)
            elif s[rbacket + 1] == '?':
                selectable(val, newstr)
            else:
                transnfa(val, newstr)
                transnfa(val, next1)
                return
        transnfa(val, next2)
    else:
        pure(val, s)


def star(val, s):  # 处理闭包*
    val.nfa.append(deepcopy(val.d))
    record1 = len(val.nfa) - 1
    if len(val.nfa) > 1 and not val.inchoose:
        val.nfa[-2]['#'].append(record1)
    if val.inchoose:
        val.inchoose = False
    # nfa[record1]['#'].append(record1 + 1)
    if len(s) > 1:  # 长字符串处理
        transnfa(val, s)
    else:
        single(val, s)  # 处理单个字符
    record2 = len(val.nfa) - 1
    val.nfa[record2]['#'].append(record1 + 1)
    val.nfa.append(deepcopy(val.d))
    val.nfa[record2]['#'].append(record2 + 1)
    val.nfa[record1]['#'].append(record2 + 1)


def plus(val, s):  # 处理正闭包+
    val.nfa.append(deepcopy(val.d))
    record1 = len(val.nfa) - 1
    if len(val.nfa) > 1 and not val.inchoose:
        val.nfa[-2]['#'].append(record1)
    if val.inchoose:
        val.inchoose = False
    # nfa[record1]['#'].append(record1 + 1)
    if len(s) > 1:
        transnfa(val, s)
    else:
        single(val, s)
    record2 = len(val.nfa) - 1
    val.nfa[record2]['#'].append(record1 + 1)
    val.nfa.append(deepcopy(val.d))
    val.nfa[record2]['#'].append(record2 + 1)


def selectable(val, s):  # 处理可选 ?
    record1 = len(val.nfa)
    if len(val.nfa) > 1 and not val.inchoose:
        val.nfa[-1]['#'].append(record1)
    if len(s) > 1:
        transnfa(val, s)
    else:
        single(val, s)
    val.nfa[record1]['#'].append(len(val.nfa) - 1)


def choose(val, s):  # 处理选择字符|，|将字符串分为两个部分
    last = s[:s.find('|')]
    next = s[s.find('|') + 1:]
    val.nfa.append(deepcopy(val.d))
    record1 = len(val.nfa) - 1
    if record1 != 0 and (not val.inchoose):
        val.nfa[record1 - 1]['#'].append(record1)
    val.nfa[record1]['#'].append(record1+1)
    transnfa(val, last)     # 先处理前面的部分
    record2 = len(val.nfa) - 1
    val.nfa[record1]['#'].append(record2 + 1)
    val.inchoose = True
    transnfa(val, next)     # 再处理后面的部分
    val.nfa.append(deepcopy(val.d))
    val.nfa[record2]['#'].append(len(val.nfa) - 1)
    val.nfa[len(val.nfa) - 2]['#'].append(len(val.nfa) - 1)


def single(val, s):  # 处理单字符
    val.nfa.append(deepcopy(val.d))
    if len(val.nfa) > 1 and not val.inchoose:
        if len(val.nfa) - 1 not in val.nfa[-2]['#']:
            val.nfa[-2]['#'].append(len(val.nfa) - 1)
    if val.inchoose:
        val.inchoose = False
    val.nfa.append(deepcopy(val.d))
    val.nfa[-2][s].append(len(val.nfa) - 1)


def pure(val, s):  # 字符串中没有|和（）的情况
    if len(s) == 0:
        return
    if len(s) == 1:
        single(val, s)
        return
    for i in range(len(s) - 1):
        if s[i].isalpha() and s[i + 1].isalpha():
            single(val, s[i])
        if s[i + 1] == '*':
            star(val, s[i])
        if s[i + 1] == '+':
            plus(val, s[i])
        if s[i + 1] == '?':
            selectable(val, s[i])

    if s[len(s) - 1].isalpha():
        single(val, s[len(s) - 1])


def findrbacket(s):  # 根据'('找到对应')'的位置
    count = 1
    for i in range(s.find('(') + 1, len(s)):
        if s[i] == '(':
            count += 1
        if s[i] == ')':
            count -= 1
            if count == 0:
                return i
