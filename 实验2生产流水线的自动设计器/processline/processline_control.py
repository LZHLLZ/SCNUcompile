from PyQt5.QtGui import QImage, QPixmap, QKeySequence

from processline import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from value import *
from nfa_create import *
from dfa_create import *
from mini_dfa_create import *
from table_create import *
from graph_create import *


# ++++++++start---------绑定槽函数显示的方法----------start------------
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)

    def generate_clicked(self):
        val = Value(self.lineEdit.text())
        #   构建表
        try:
            transnfa(val, val.s)
            nfa2dfa(val)
            mini_dfa(val)
        except:
            QMessageBox.critical(self, "错误", "请输入正确的正则表达式!", QMessageBox.Ok)
            return

        #   绘制表
        draw_nfa_table(self, val)
        draw_dfa_table(self, val)
        draw_minidfa_table(self, val)
        #   绘制图
        draw_nfa_graph(val)
        draw_dfa_graph(val)
        draw_mini_dfa_graph(val)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.nfa_graph.setPixmap(QPixmap("./graph/nfa.png"))
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.dfa_graph.setPixmap(QPixmap("./graph/dfa.png"))
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.minidfa_graph.setPixmap(QPixmap("./graph/mini_dfa.png"))


    def save_clicked(self):
        file_name = QFileDialog.getSaveFileName(self, "保存文件", "",
                                                "txt files(*.txt);;all files(*.*)")
        with open(file_name[0], 'w') as f:
            f.write(self.lineEdit.text())

    def open_clicked(self):
        file_name = QFileDialog.getOpenFileName(self, "打开文件", "",
                                                "txt files(*.txt);;all files(*.*)")
        with open(file_name[0], 'r') as f:
            self.lineEdit.setText(f.read())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.setFixedSize(w.width(), w.height())
    w.generate.setFocus()   # 设置默认按下回车即可触发按钮
    w.generate.setShortcut(QKeySequence.InsertParagraphSeparator)
    w.generate.setShortcut(Qt.Key_Return)
    w.show()
    sys.exit(app.exec_())
# --------end---------绑定槽函数显示的方法----------end------------
