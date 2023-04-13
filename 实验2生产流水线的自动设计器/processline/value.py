#   定义用到的
class Value:
    def __init__(self, s):
        self.s = s
        self.d = {}  # 记录nfa字典
        self.nfa = []  # 存放nfa表
        self.inchoose = False  # 判断可选 |
        self.dfa = []  # 存放dfa表
        self.nowset = {'now': set()}  # 存放当前状态集合
        self.nowlist = []  # 存放所有状态集合
        self.letter = []  # 记录表达式中的字母

        for i in s:  # 记录非特殊字符
            if i.isalpha():
                if i not in self.letter:
                    self.letter.append(i)
                    self.d[i] = []
                    self.nowset[i] = set()
        self.d['#'] = []
        self.mini_dfa_table = []  # 最小化dfa表
        self.mini_dfa_d = dict()  # 最小化dfa字典
        for alp in self.letter:  # 初始化字典
            self.mini_dfa_d[alp] = None
        self.notfinal = []  # 记录非终态
        self.final = []  # 记录终态
        self.finish_split = []  # 已完成分割