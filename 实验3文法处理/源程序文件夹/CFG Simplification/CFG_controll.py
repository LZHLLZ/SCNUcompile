from PyQt5.QtGui import QImage, QPixmap, QKeySequence

from CFG import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QFileDialog, QTableWidgetItem, QMessageBox, QLabel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt

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


# cfg = CFG(None, None, None, None)
# ++++++++start---------绑定槽函数显示的方法----------start------------
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        # self.statusbar.showMessage("    点击右上角“重置”清空所有输入框")
        self.statusbar.addPermanentWidget(
            QLabel("要写入新的文法请点击右上角“重置”清空所有输入框")
        )

    def check_initial(self):
        global cfg
        if cfg.p == None or cfg.vn == None or cfg.vt == None or cfg.s == None:
            QMessageBox.critical(self, "错误", "未进行初始化，请检查文法!", QMessageBox.Ok)
            return True

    def reset_clicked(self):
        global cfg
        cfg = CFG(None, None, None, None)
        self.show_vn.clear()
        self.show_vt.clear()
        self.start.clear()
        self.grammar.clear()
        self.simplify_cfg_result.clear()
        self.left_common_factor_result.clear()
        self.left_recursion_result.clear()
        self.first_result.clear()
        self.follow_result.clear()
        self.fa_graph.clear()
        self.dfa_graph.clear()
        self.minidfa_graph.clear()

    def open_clicked(self):
        file_name = QFileDialog.getOpenFileName(self, "打开文件", "",
                                                "txt files(*.txt);;all files(*.*)")
        with open(file_name[0], 'r') as f:
            self.grammar.clear()
            lines = f.readlines()
            self.show_vn.setText(lines[0])
            self.show_vt.setText(lines[1])
            self.start.setText(lines[2])
            for line in lines[3:]:
                if line[-1] == '\n':
                    self.grammar.append(line[:-1])
                else:
                    self.grammar.append(line)

    def save_clicked(self):
        file_name = QFileDialog.getSaveFileName(self, "保存文件", "",
                                                "txt files(*.txt);;all files(*.*)")
        with open(file_name[0], 'a') as f:
            f.seek(0)  # 定位
            f.truncate()  # 清空文件
            # lines = self.grammar.toPlainText().split('\n')
            if self.show_vn.text()[-1] != '\n':
                f.write(self.show_vn.text() + '\n')
            else:
                f.write(self.show_vn.text())
            if self.show_vt.text()[-1] != '\n':
                f.write(self.show_vt.text() + '\n')
            else:
                f.write(self.show_vt.text())
            # f.write(self.show_vt.text())
            if self.start.text()[-1] != '\n':
                f.write(self.start.text() + '\n')
            else:
                f.write(self.start.text())
            # f.write(self.start.text())
            f.write(self.grammar.toPlainText())

    def cfg_initial(self):
        global cfg
        try:
            p = []
            vn = []
            vt = []
            lines = self.grammar.toPlainText().split('\n')
            for line in lines:
                p.extend(split_production(line))
            if p:
                vn, vt = get_vn_vt(p)
                self.show_vn.setText(''.join(vn))
                self.show_vt.setText(''.join(vt))
            else:
                vn = list(self.show_vn.text())
                vt = list(self.show_vt.text())
            # print(vn,vt,p)
            self.start.setText(vn[0])
            s = self.start.text()
            if vn[-1] == '\n':
                vn = vn[:-1]
            if vt[-1] == '\n':
                vt = vt[:-1]
            if s[-1] == '\n':
                s = s[:-1]

            merge_P(p)  # 规则左部相同则合并
            cfg = CFG(vn, vt, p, s)  # 创建上下无关文法类
            QMessageBox.information(self, "", "初始化成功!", QMessageBox.Ok)
        except:
            QMessageBox.critical(self, "错误", "请按格式填入所有输入框!", QMessageBox.Ok)

    def Simplify_cfg_button_clicked(self):
        global cfg
        if self.check_initial():
            return
        # merge_P(cfg.p)  # 规则左部相同则合并
        simplify_cfg(cfg)  # 化简文法
        showlines = perform(cfg.p)
        self.simplify_cfg_result.clear()
        for line in showlines:
            self.simplify_cfg_result.append(line)
        self.tabWidget.setCurrentIndex(0)

    def Left_common_factor_button_clicked(self):
        global cfg
        if self.check_initial():
            return
        try:
            if not left_common_factor_indirect(cfg):  # 消除间接左公因子
                QMessageBox.critical(self, "错误", "推导大于4次，请检查文法!\n若确认文法无误，请写入错误报告!", QMessageBox.Ok)
            left_common_factor(cfg)  # 消除左公因子
            showlines = perform(cfg.p)
            self.left_common_factor_result.clear()
            for line in showlines:
                self.left_common_factor_result.append(line)
            self.tabWidget.setCurrentIndex(1)
        except:
            QMessageBox.critical(self, "错误", "消除左公因子失败，请检查文法!\n若确认文法无误，请写入错误报告!", QMessageBox.Ok)

    def Left_recursion_button_clicked(self):
        global cfg
        if self.check_initial():
            return
        try:
            left_recursion(cfg)  # 左递归
            showlines = perform(cfg.p)
            self.left_recursion_result.clear()
            for line in showlines:
                self.left_recursion_result.append(line)
            self.tabWidget.setCurrentIndex(2)
        except:
            QMessageBox.critical(self, "错误", "消除左递归失败，请检查文法!\n若确认文法无误，请写入错误报告!", QMessageBox.Ok)

    def Get_first_follow_button_clicked(self):
        global cfg
        if self.check_initial():
            return
        first = dict()  # first集合
        follow = dict()  # follow集合
        try:
            get_first(cfg, first)
            get_follow(cfg, first, follow)
            self.first_result.clear()
            for i in first.keys():
                self.first_result.append(i + ' = ' + str(first[i]))

            self.follow_result.clear()
            for i in follow.keys():
                self.follow_result.append(i + ' = ' + str(follow[i]))
            self.tabWidget.setCurrentIndex(3)
        except:
            QMessageBox.critical(self, "错误", "获取first和follow集合失败，请检查文法!\n若确认文法无误，请写入错误报告!", QMessageBox.Ok)

    def FA_button_clicked(self):
        global cfg
        if self.check_initial():
            return
        fa_value = Value(cfg)  # 创建fa自动机的类
        if is_regluar_grammer(cfg):  # 判断是否线性规则
            finite_machine(cfg, fa_value)  # 生成有穷自动机
            self.tabWidget.setCurrentIndex(4)
            try:
                nfa2dfa(fa_value)  # NFA转为DFA
                mini_dfa(fa_value)  # DFA最小化
                draw_dfa_graph(fa_value)  # 绘制dfa图
                draw_mini_dfa_graph(fa_value)  # 绘制最小化dfa图
                self.scrollArea.setWidget(self.scrollAreaWidgetContents)
                self.fa_graph.setPixmap(QPixmap("./graph/finite_machine.png"))
                self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
                self.dfa_graph.setPixmap(QPixmap("./graph/dfa.png"))
                self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
                self.minidfa_graph.setPixmap(QPixmap("./graph/mini_dfa.png"))
            except:
                QMessageBox.critical(self, "错误", "该有穷自动机不是NFA!", QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "错误", "非线性规则!\n产生式必须同时为左或右线性规则并且要符合格式!", QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.setFixedSize(w.width(), w.height())
    cfg = CFG(None, None, None, None)
    inform = "请按以下格式填入输入框\n" \
             "可以输入完产生式后直接点击“初始化”按钮\n系统将自动填写剩余输入框\n\n" \
             "格式举例如下：\n\n" \
             "vn(非终结符): AB\n\n" \
             "vt(终结符): ab\n\n" \
             "s(开始符): A\n\n" \
             "p(产生式): \n" \
             "A->a\n" \
             "B->b"
    w.grammar.setPlaceholderText(inform)
    # w.generate.setFocus()   # 设置默认按下回车即可触发按钮
    # w.generate.setShortcut(QKeySequence.InsertParagraphSeparator)
    # w.generate.setShortcut(Qt.Key_Return)
    w.show()
    sys.exit(app.exec_())
# --------end---------绑定槽函数显示的方法----------end------------
