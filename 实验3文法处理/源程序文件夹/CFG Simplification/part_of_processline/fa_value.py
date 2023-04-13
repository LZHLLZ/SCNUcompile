#   定义用到的
class Value:
    def __init__(self, cfg):
        self.fadict = {} # 存放fa字典
        self.nfa = []  # 存放nfa表
        self.dfa = []  # 存放dfa表
        self.nowset = {'now': set()}  # 存放当前状态集合
        self.nowlist = []  # 存放所有状态集合
        self.letter = cfg.vt  # 记录表达式中的字母

        for alp in cfg.vt:
            self.fadict[alp] = []
            self.nowset[alp] = set()
        self.fadict['#'] = []
        self.mini_dfa_table = []  # 最小化dfa表
        self.mini_dfa_d = dict()  # 最小化dfa字典

        for alp in self.letter:  # 初始化字典
            self.mini_dfa_d[alp] = None

        self.notfinal = []  # 记录非终态
        self.final = []  # 记录终态
        self.finish_split = []  # 已完成分割的最小化dfa集合