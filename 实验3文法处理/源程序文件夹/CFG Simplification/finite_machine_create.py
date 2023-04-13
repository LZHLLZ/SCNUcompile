from graphviz import Digraph
from copy import deepcopy
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt

def is_regluar_grammer(cfg):
    print(cfg.p)
    for production in cfg.p:
        for senten in production[1]:
            if len(senten) > 2:
                print('非线性规则')
                return False
            elif len(senten) == 2:
                if cfg.left == None:
                    if senten[0] in cfg.vn:
                        cfg.left = True
                    else:
                        cfg.left = False
                if cfg.left == True:  # 左线性，形如Aa,a
                    if senten[0] not in cfg.vn or senten[1] in cfg.vn:
                        print('产生式必须同时为左或右线性规则并且符合格式')
                        print('处理到该规则出错:')
                        print(production[0], '->', senten)
                        return False
                elif cfg.left == False:  # 右线性, 形如aA, a
                    if senten[0] in cfg.vn or senten[1] not in cfg.vn:
                        print('产生式必须同时为左或右线性规则并且符合格式')
                        print('处理到该规则出错:')
                        print(production[0], '->', senten)
                        return False
            else:
                if senten[0] in cfg.vn:
                    print('产生式必须同时为左或右线性规则并且符合格式')
                    print('处理到该规则出错:')
                    print(production[0], '->', senten)
                    return False
    if cfg.left == None:   # 规则右部全为终结符的情况
        cfg.left = False
    return True


def finite_machine(cfg, fa_value):
    f = Digraph('有穷自动机', format='png')
    f.attr(rankdir='LR')
    f.attr('node', shape='doublecircle')
    if cfg.left:
        f.node(cfg.s)  # 开始节点画双圆
    else:  # 右线性规则添加结束节点
        f.node('End')

    f.attr('node', shape='circle')
    alplist = []
    if cfg.left:
        f.node('Start')  # 左线性规则添加开始节点
        addlist = deepcopy(fa_value.fadict)
        fa_value.nfa.append(addlist)
        alplist.append('Start')

    for i in range(len(cfg.p)):
        addlist = deepcopy(fa_value.fadict)
        fa_value.nfa.append(addlist)
        alplist.append(cfg.p[i][0])

    if cfg.left == False:
        addlist = deepcopy(fa_value.fadict)
        fa_value.nfa.append(addlist)
    end = len(cfg.p)
    for production in cfg.p:
        for senten in production[1]:
            # 对于左线性规则，形如Q->a的每个规则，引一条从开始状态S到状态Q的弧，其标记为a;
            # 对于左线性规则，形如Q -> Ra的规则引一条从状态R到Q的弧，
            # 其标记为a。其中R为非终结符号，a为终结符号;
            # 右线性规则相反
            if cfg.left == True:
                if len(senten) == 1:
                    f.edge('Start', production[0], label=senten[0])
                    fa_value.nfa[0][senten[0]].append(alplist.index(production[0]))
                if len(senten) == 2:
                    f.edge(senten[0], production[0], label=senten[1])
                    fa_value.nfa[alplist.index(senten[0])][senten[1]].append(alplist.index(production[0]))

            if cfg.left == False:
                if len(senten) == 1:
                    f.edge(production[0], 'End', label=senten[0])
                    fa_value.nfa[alplist.index(production[0])][senten[0]].append(end)
                if len(senten) == 2:
                    f.edge(production[0], senten[1], label=senten[0])
                    fa_value.nfa[alplist.index(production[0])][senten[0]].append(alplist.index(senten[1]))

    f.render('./graph/finite_machine', view=False)
