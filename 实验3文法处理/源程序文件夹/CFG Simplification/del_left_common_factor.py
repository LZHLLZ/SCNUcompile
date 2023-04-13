from get_first_and_follow import *


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


def recursion(left_ch, cfg, count, s, l, countlist):
    for senten in get_sentens(cfg.p, left_ch):
        if senten[0] in cfg.vn:
            recursion(senten[0], cfg, count + 1, ''.join(senten[1:]) + s, l, countlist)
        else:
            countlist.append(count)
            l.append(''.join(senten) + s)


# 消除间接左公因子
def left_common_factor_indirect(cfg):
    P = []
    for i, production in enumerate(cfg.p):
        count = 0
        countlist = []
        sentens = []
        for j, senten1 in enumerate(production[1]):
            s = ""  # 递增的字符串
            l = []  # 接受递归的字符串
            if senten1[0] in cfg.vn:
                recursion(senten1[0], cfg, count, s, l, countlist)
                for recur_list in l:
                    sentens.append(list(recur_list) + senten1[1:])
            else:
                sentens.append(senten1)
        if sum(countlist) > 4:  # 大于四次推导报错
            return False
        P.append([production[0], sentens])
    cfg.p.clear()
    cfg.p.extend(P[:])
    return True


# 消除左公因子
def left_common_factor(cfg):
    P = []
    for i, production in enumerate(cfg.p):
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
                    if senten3[len(samestr):]:
                        newsentens.append(senten3[len(samestr):])
                    else:
                        newsentens.append(['#'])
                if [production[0] + str(i), newsentens] not in newproduction:  # 规则不要重复
                    newproduction.append([production[0] + str(i), newsentens])
                cfg.vn.append(production[0] + str(i))
            else:
                notmerged.append(l.pop())

        sentens += notmerged
        P.append([production[0], sentens])  # 合并后的规则
        P.extend(newproduction)  # 加入新规则
    if len(cfg.p) != len(P):
        cfg.p.clear()
        cfg.p.extend(P[:])
        left_common_factor(cfg)  # 递归处理直到没有相同前缀


vn = ['S', 'A', 'B', 'C', 'D', 'E', 'F']
vt = ['a', 'b', 'c', 'd', 'e']
s = 'S'
p = [['S', [['A', 'a'], ['B', 'a']]],
     ['A', [['C', 'b']]],
     ['B', [['D', 'c']]],
     ['C', [['E', 'd']]],
     ['D', [['F', 'e']]],
     ['E', [['f', 'e']]],
     ['F', [['f', 'd']]]]

cfg = CFG(vn, vt, p, s)
left_common_factor_indirect(cfg)
