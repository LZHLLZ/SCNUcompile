from initial import get_sentens


def if_recursion(cfg, left_ch, production, used_ch, finished):  # cfg, P
    for senten in production:
        if senten[0] == left_ch:
            return True
        if senten[0] in used_ch:  # 阻止递归
            return True
        if senten[0] in cfg.vn:
            if senten[0] not in finished:
                return False
            used_ch.add(senten[0])
            if if_recursion(cfg, left_ch, get_sentens(cfg.p, senten[0]), used_ch, finished):
                return True
    return False


# 消除左递归
def left_recursion(cfg):
    P = []
    finished = []  # 已解决的终结符
    for i, production in enumerate(cfg.p):
        sentens = []  # 原来已改变的句型
        newsentens = []  # 新句型
        deal_sentens = []  # 要处理递归的句型:[[],[]]
        used_ch = set()
        # 判断该产生式是否有递归
        if if_recursion(cfg, production[0], production[1], used_ch, finished):
            for j, senten1 in enumerate(production[1]):  # 代入已解决的终结符
                if senten1[0] in cfg.vn and senten1[0] in finished:
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
            newsentens.append(['#'])  # 表示空串

            P.append([production[0], sentens])
            P.append([production[0] + str(i), newsentens])
            cfg.vn.append(production[0] + str(i))
        else:
            P.append(production)
        finished.append(production[0])
    cfg.p.clear()
    cfg.p.extend(P[:])
