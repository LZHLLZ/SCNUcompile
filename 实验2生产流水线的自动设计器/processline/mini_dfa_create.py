from copy import deepcopy
import sys


def mini_dfa(val):
    temp = []  # 待分割
    temp.append(val.notfinal)
    temp.append(val.final)
    split(temp, val)
    val.finish_split.sort(key=getmin)
    for i in range(len(val.finish_split)):  # 先分配好所有的点
        val.mini_dfa_table.append(deepcopy(val.mini_dfa_d))
    for i in range(len(val.dfa)):
        for alp in val.letter:
            classidx = None  # 记录指向的类别
            nowidx = None  # 记录当前的类别
            for j in range(len(val.finish_split)):
                if val.dfa[i][alp] in val.finish_split[j]:
                    classidx = j
                if val.dfa[i]['now'] in val.finish_split[j]:
                    nowidx = j
            val.mini_dfa_table[nowidx][alp] = classidx


def getmin(elm):  # 作为比较的key，取集合中的最小值
    m = sys.maxsize
    for i in elm:
        m = min(m, min(i))
    return m


def not_sameset(a, b, l):  # 判断俩个集合是否在同一状态
    for s in l:
        if (a in s) and (b in s):
            return False
    return True


def split(temp, val):
    while temp:  # 循环直到状态集合无法再分割
        used = []  # 记录已经分好的集合
        flag = True
        for i in range(len(temp[0])):
            samestate = []  # 保存相同状态的集合
            if temp[0][i] in used:
                continue
            samestate.append(temp[0][i])
            for j in temp[0][i + 1:]:
                if j in used:
                    continue
                for alp in val.letter:  # 对于所有字母，判断两者是否处于同一状态
                    if val.dfa[val.nowlist.index(temp[0][i])]['now'] in val.final:
                        if val.dfa[val.nowlist.index(j)]['now'] not in val.final:
                            flag = False
                    if val.dfa[val.nowlist.index(temp[0][i])]['now'] in val.notfinal:
                        if val.dfa[val.nowlist.index(j)]['now'] not in val.notfinal:
                            flag = False
                    if not_sameset(val.dfa[val.nowlist.index(temp[0][i])][alp], val.dfa[val.nowlist.index(j)][alp],
                                   temp + val.finish_split):
                        flag = False

                if flag:
                    samestate.append(j)
                    used.append(j)
                flag = True
            used.append(temp[0][i])
            if len(samestate) == len(temp[0]):
                val.finish_split.append(temp[0])
            else:
                temp.append(samestate)
        temp.pop(0)
