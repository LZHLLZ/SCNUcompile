from cfg_value import *
from initial import *
from simplify_cfg import *
from del_left_common_factor import *
from del_left_recursion import *
from get_first_and_follow import *
from finite_machine_create import *
from part_of_processline.fa_value import *
from part_of_processline.dfa_create import *
from part_of_processline.mini_dfa_create import *
from part_of_processline.graph_create import *

# 初始化，要记得以下格式
# vt = ['e', 'f', 'c', 'g']  # 终结符
# p = [['S', 'Be'], ['B', 'Ce'], ['B', 'Af'],  # 产生式
#      ['A', 'Ae'], ['A', 'e'], ['C', 'Cf'], ['D', 'f']]

# vn = ['A']  # 非终结符
# vt = ['a','e', 'f', 'c', 'g']
# p = [['A', 'ac'], ['A', 'aae'], ['A', 'aaf'], ['A', 'g']]
# s = 'A'  # 起始符

# vn = ['Z', 'A', 'B']
# vt = ['a', 'b']
# s = 'Z'
# p = [['Z', [['Z', 'a'], ['A', 'b'], ['B', 'a']]],
#      ['A', [['B', 'b'], ['a']]],
#      ['B', [['A', 'a'], ['b']]]]

vn =  ['S','A','B','D']
p = [['S', ['B', 'e']], ['B', ['C', 'e']], ['B', ['A', 'f']],  # 产生式
     ['A', ['A', 'f']], ['A', ['e']], ['C', ['C', 'f']], ['D', ['f']]]
s = 'S'
vt = ['e','f']

cfg = CFG(vn, vt, p, s)  # 创建上下无关文法类
merge_P(cfg.p)           # 规则左部相同则合并
simplify_cfg(cfg)        # 化简文法
#switch_structure(cfg.p) # 改变结构
left_common_factor(cfg)  # 消除左公因子
left_recursion(cfg)      # 左递归

first = dict()          # first集合
follow = dict()         # follow集合
get_first(cfg, first)
get_follow(cfg, first, follow)
fa_value = Value(cfg)   # 创建fa自动机的类
if is_regluar_grammer(cfg):     # 判断是否线性规则
    finite_machine(cfg, fa_value)  # 生成有穷自动机
    nfa2dfa(fa_value)   # NFA转为DFA
    mini_dfa(fa_value)  # DFA最小化
    draw_dfa_graph(fa_value)    # 绘制dfa图
    draw_mini_dfa_graph(fa_value)  # 绘制最小化dfa图
