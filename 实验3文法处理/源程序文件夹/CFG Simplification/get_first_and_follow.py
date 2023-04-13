from initial import get_sentens
from cfg_value import *



def find_first(cfg, left_ch, ch_first, used_ch):
    for senten in get_sentens(cfg.p, left_ch):
        if senten[0] in used_ch:  # 防止无限递归
            return False
        if senten[0] not in cfg.vn:
            ch_first.add(senten[0])
        else:
            used_ch.add(senten[0])
            if not find_first(cfg, senten[0], ch_first, used_ch):
                continue


def get_first(cfg, first):
    for production in cfg.p:  # 自底向上减少推导
        if production[0] not in cfg.vn:  # 只处理非终结符
            continue
        if production[0] not in first:  # 未加入的加入
            first[production[0]] = set()
        for senten in production[1]:
            if senten[0] not in cfg.vn:  # 终结符加入集合
                first[production[0]].add(senten[0])
            else:
                if senten[0] in first:  # 已经在first集合中
                    first[production[0]].update(first[senten[0]])
                    continue
                # 不在first集合中
                used_ch = set()
                find_first(cfg, production[0], first[production[0]], used_ch)


def find_follow(cfg, ch, first, ch_follow, used_ch):
    if ch == cfg.s:  # 起始符添加空串
        ch_follow.add('#')
    for production in cfg.p:
        for senten in production[1]:
            if senten.count(ch):
                if senten.index(ch) == len(senten) - 1:
                    if ch != production[0] and production[0] not in used_ch:  # bug
                        used_ch.add(production[0])
                        find_follow(cfg, production[0], first, ch_follow, used_ch)
                elif senten[senten.index(ch) + 1] in cfg.vn:
                    # 添加非空first集合
                    ch_follow.update(first[senten[senten.index(ch) + 1]] - {'#'})
                else:  # 添加终结符
                    ch_follow.add(senten[senten.index(ch) + 1])


def get_follow(cfg, first, follow):
    for ch in cfg.vn:
        follow[ch] = set()
        for production in cfg.p:
            for senten in production[1]:
                if senten.count(ch):  # 句型中有目标字符
                    # 非终结符后面没有任何符号的情况
                    if senten.index(ch) == len(senten) - 1:
                        # follow[ch].add(production[0])   # 后续follow集合加入
                        if ch != production[0]:
                            used_ch = set()
                            find_follow(cfg, production[0], first, follow[ch], used_ch)
                    elif senten[senten.index(ch) + 1] in cfg.vn:
                        # 添加非空first集合
                        follow[ch].update(first[senten[senten.index(ch) + 1]] - {'#'})
                    else:  # 添加终结符
                        follow[ch].add(senten[senten.index(ch) + 1])

        if ch == cfg.s:  # 起始符添加空串
            follow[ch].add('#')


vn = ['S', 'A', 'B', 'C', 'D', 'E', 'F']
vt = ['a', 'b', 'c', 'd', 'e']
s = 'S'
p = [['S', [['A', 'a'], ['B', 'a']]],
     ['A', [['C', 'b']]],
     ['B', [['D', 'C']]],
     ['C', [['E', 'd']]],
     ['D', [['F', 'e']]],
     ['E', [['f', 'e']]],
     ['F', [['f', 'd']]],
     ['G', [['G']]]]

