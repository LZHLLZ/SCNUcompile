from initial import get_sentens

def if_senten_tofinal(cfg, senten, used_ch):  # 判断一个规则能否推出终结符
    for ch in senten:
        if ch in used_ch:  # 阻止循环
            return False
        if ch in cfg.vn:  # 若某个字符无法推到终结符返回False
            if not is_tofinal(cfg, ch, used_ch):
                return False
    return True


def is_tofinal(cfg, ch, used_ch):  # 判断一个非终结字符的能否推出终结符
    if ch in used_ch:  # 阻止循环
        return False
    used_ch.add(ch)
    for senten in get_sentens(cfg.p, ch):  # 判断每个规则，若某个规则能推出终结符返回True
        if if_senten_tofinal(cfg, senten, used_ch):
            return True
    return False


def delete_ch(cfg, P, ch):  # 删除与终结字符有关的规则
    #print(ch)
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
    if ch in cfg.vn:
        cfg.vn.remove(ch)


# 化简文法
def simplify_cfg(cfg):
    # 先删除有害规则
    P = []
    for production in cfg.p:
        sentens = []
        for senten in production[1]:
            if len(senten) == 1:
                if production[0] != senten[0]:
                    sentens.append(senten)
            else:
                sentens.append(senten)
        if sentens:
            P.append([production[0], sentens])
    cfg.p.clear()
    cfg.p.extend(P[:])
    # 删除多余规则
    # 1.判断左边非终结符能推出终结符
    for production in cfg.p:
        used_ch = set()
        if not is_tofinal(cfg, production[0], used_ch):
            delete_ch(cfg, P, production[0])
    cfg.p.clear()
    cfg.p.extend(P[:])
    # 2.判断非终结符是否在某句型出现
    exist = []  # 判断句型中存在的终结符
    for production in cfg.p:
        for senten in production[1]:
            for ch in senten:
                if ch in cfg.vn:
                    exist.append(ch)
    dele = set(cfg.vn) - set(exist)
    if cfg.s in dele:
        dele.remove(cfg.s)  # 起始符不要删
    for i in dele:
        delete_ch(cfg, cfg.p, i)

    # 删除不存在的终结符
    exist = []
    for production in cfg.p:
        for senten in production[1]:
            for ch in senten:
                if ch in cfg.vt:
                    exist.append(ch)
    dele = set(cfg.vt) - set(exist)
    for i in dele:
        cfg.vt.remove(i)


# def switch_structure(p):  # 改变p的存储结构
#     P = []
#     for production in p:
#         sentens = []
#         for senten in production[1]:
#             sentens.append(list(senten))
#         P.append([production[0], sentens])
#
#     p.clear()
#     p.extend(P[:])
