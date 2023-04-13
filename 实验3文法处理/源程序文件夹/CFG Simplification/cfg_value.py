class CFG:
    def __init__(self, VN, VT, P, S):
        self.vn = VN  # 非终结符集合
        self.vt = VT  # 终结符集合
        self.p = P  # 规则，产生式的集合
        self.s = S  # 开始符号
        self.left = None  # 判断左或右线性规则
