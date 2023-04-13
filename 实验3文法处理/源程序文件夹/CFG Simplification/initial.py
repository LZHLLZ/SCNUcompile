# 合并规则
def merge_P(p):
    P = []
    used = []
    for i in range(len(p)):
        merge = []
        if p[i][0] not in used and (p[i][1] not in merge):
            if isinstance(p[i][1][0], str):
                merge.append(p[i][1])
            else:
                merge.extend(p[i][1])
            for j in p[i + 1:]:
                if j[0] == p[i][0] and (j[1] not in merge):
                    if isinstance(j[1][0], str):
                        merge.append(j[1])
                    else:
                        merge.extend(j[1])
            P.append([p[i][0], merge])
            # P.append([p[i][0],'|'.join(merge)])
            used.append(p[i][0])

    p.clear()
    p.extend(P[:])


# 分割产生式再合并
def split_production(production):  # str --> [[]]
    newproduction = []
    product = "".join(production.split())  # 去除多余空格
    split_product = product.split('->')
    sentens = split_product[1].split('|')
    for senten in sentens:
        newproduction.append([split_product[0], list(senten)])
    return newproduction


s = split_production('A -> abd|bvf|jkl')


def get_vn_vt(p):
    vn = []
    vt = []
    for production in p:
        if not production[0].isupper():
            print('文法错误')
            return False
        if production[0] not in vn:
            vn.append(production[0])
        for ch in production[1]:
            if ch.isupper():
                if ch not in vn:
                    vn.append(ch)
            else:
                if ch not in vt:
                    vt.append(ch)
    return vn, vt


def get_sentens(P, ch):  # 由非终结符获取规则
    for production in P:
        if production[0] == ch:
            return production[1]


def perform(p):     # 打印文法
    lines = []
    for production in p:
        sentens = []
        for senten in production[1]:
            sentens.append(''.join(senten))
        #print(production[0], '->', '|'.join(sentens))
        line = production[0]+' -> '+'|'.join(sentens)
        lines.append(line)
    return lines


p = [['S', ['B', 'e']], ['B', ['C', 'e']], ['B', ['A', 'f']],  # 产生式
     ['A', ['A', 'f']], ['A', ['e']], ['C', ['C', 'f']], ['D', ['f']]]

vn, vt = get_vn_vt(p)
merge_P(p)
perform(p)
