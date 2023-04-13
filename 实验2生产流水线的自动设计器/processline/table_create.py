from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from copy import deepcopy


def draw_nfa_table(self, val):
    colist = list(val.d.keys())
    rowlist = [str(x) for x in range(len(val.nfa))]
    self.nfa_table.setRowCount(len(val.nfa))
    self.nfa_table.setColumnCount(len(colist))
    self.nfa_table.setHorizontalHeaderLabels(colist)
    self.nfa_table.setVerticalHeaderLabels(rowlist)
    for i, row in enumerate(val.nfa):
        for j, col in enumerate(colist):
            if val.nfa[i][col]:
                item = QTableWidgetItem(str(list(set(val.nfa[i][col]))))
            else:
                item = QTableWidgetItem('')
            self.nfa_table.setItem(i, j, item)
    self.nfa_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.nfa_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)


def draw_dfa_table(self, val):
    nowrlist = list(val.nowset.keys())
    nowclist = [str(x) for x in range(len(val.dfa))]
    self.dfa_table.setRowCount(len(val.dfa))
    self.dfa_table.setColumnCount(len(nowrlist))
    newnowrlist = deepcopy(nowrlist)
    newnowrlist[0] = '状态集合'
    self.dfa_table.setHorizontalHeaderLabels(newnowrlist)
    self.dfa_table.setVerticalHeaderLabels(nowclist)
    for i, row in enumerate(val.dfa):
        for j, col in enumerate(nowrlist):
            if val.dfa[i][col]:
                item = QTableWidgetItem(str(val.dfa[i][col]))
            else:
                item = QTableWidgetItem('')
            self.dfa_table.setItem(i, j, item)
    self.dfa_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.dfa_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)


def draw_minidfa_table(self, val):
    minidfa_colist = list(val.mini_dfa_d.keys())
    minidfa_rowlist = [str(x) for x in range(len(val.mini_dfa_table))]
    self.minidfa_table.setRowCount(len(val.mini_dfa_table))
    self.minidfa_table.setColumnCount(len(minidfa_colist))
    self.minidfa_table.setHorizontalHeaderLabels(minidfa_colist)
    self.minidfa_table.setVerticalHeaderLabels(minidfa_rowlist)
    for i, row in enumerate(val.mini_dfa_table):
        for j, col in enumerate(minidfa_colist):
            if val.mini_dfa_table[i][col] is not None:
                item = QTableWidgetItem(str(val.mini_dfa_table[i][col]))
            else:
                item = QTableWidgetItem('')
            self.minidfa_table.setItem(i, j, item)
    self.minidfa_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.minidfa_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
