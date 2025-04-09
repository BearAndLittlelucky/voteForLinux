import sys

import numpy as np
import pandas as pd
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QMenu, QLineEdit
from UI.voteUI import Ui_Form
import UI.voteImageSource_rc

# 主程序
class myWindow(QWidget, Ui_Form):
    def __init__(self):
        super(myWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.signalFunction()
        self.count_votes = []
        self.info_votes = []
        self.menu_visible = 1
        self.font_size_list = pd.DataFrame([[19 for i in range(14)] for j in range(8)])
        self.font_style_list = pd.DataFrame([["仿宋" for i in range(14)] for j in range(8)])
        self.visibleMenu()

    def signalFunction(self):
        self.pushButton.clicked.connect(lambda :self.makeTable(self.lineEdit_row.text(),self.lineEdit_column.text()))
        self.pushButton_combine.clicked.connect(self.resetTable)
        self.pushButton_split.clicked.connect(self.clearCell)
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)
        self.pushButton_menu.clicked.connect(self.visibleMenu)
        self.pushButton_windowStatus.clicked[bool].connect(self.windowVisible)
        self.pushButton_addLine.clicked.connect(self.addOneLine)
        self.pushButton_addCol.clicked.connect(self.addOneCol)
        self.pushButton_delLine.clicked.connect(self.delOneLine)
        self.pushButton_delCol.clicked.connect(self.delOneCol)
        self.doubleSpinBox.valueChanged.connect(self.changeFontSize)
        # self.fontComboBox.currentFontChanged.connect(self.changeFontStyle)
        self.pushButton_add_font_size.clicked.connect(self.addFontSize)
        self.pushButton_down_font_size.clicked.connect(self.downFontSize)
        self.pushButton_head_show.clicked.connect(self.showTableHead)
        self.pushButton_head_hide.clicked.connect(self.hideTableHead)
        # 点击事件获取所选内容、行列
        self.tableWidget.cellPressed.connect(self.getPosContent)
        self.fontComboBox.currentFontChanged.connect(self.changeFontStyle)

    # 获取选中行列、内容
    def getPosContent(self, row, col):
        try:
            XYindex = self.getIndex()
            self.doubleSpinBox.setValue(float(
                self.font_size_list.loc[XYindex[-1][0],XYindex[-1][1]]))
            self.fontComboBox.setCurrentFont(QFont(self.font_style_list.loc[XYindex[-1][0],XYindex[-1][1]]))
            # content = self.tableWidget.item(row, col).text()
            # print("选中行：" + str(row))
            # print("选中列：" + str(col))
            # print('选中内容:' + content)
        except:
            print('选中内容为空')
            self.doubleSpinBox.setValue(float(
                self.font_size_list.loc[row,col]))
            self.fontComboBox.setCurrentFont(QFont(self.font_style_list.loc[row,col]))

    def showTableHead(self):
        self.tableWidget.setShowGrid(True)
        self.tableWidget.verticalHeader().setVisible(True)  # 隐藏垂直表头
        self.tableWidget.horizontalHeader().setVisible(True)  # 隐藏水平表头
    def hideTableHead(self):
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.tableWidget.horizontalHeader().setVisible(False)  # 隐藏水平表头

    # 调整字体大小
    def downFontSize(self):
        size = int(self.doubleSpinBox.value())
        self.doubleSpinBox.setProperty("value", size - 1)
        self.changeFontSize(size - 1)
        row = self.tableWidget.currentRow()
        column = self.tableWidget.currentColumn()
        self.font_size_list.iloc[row, column] = size - 1
    def addFontSize(self):
        size = int(self.doubleSpinBox.value())
        self.doubleSpinBox.setProperty("value", size + 1)
        self.changeFontSize(size + 1)
        row = self.tableWidget.currentRow()
        column = self.tableWidget.currentColumn()
        self.font_size_list.iloc[row, column] = size + 1

    def changeFontStyle(self,font):
        print(self.fontComboBox.currentFont().family())
        print(font.family())
        XYindex = self.getIndex()
        for item in XYindex:
            try:
                self.dynamic_variable[f'btnRightClick{item[0]},{item[1]}'].setStyleSheet("background-color:transparent;"
                                                                                         "border-width:1px;border-style:outset;"
                                                                                         "font: {}pt {};".format(int(self.font_size_list.loc[item[0],item[1]]),font.family()))
                self.font_style_list.iloc[item[0],item[1]] = font.family()
            except:
                try:
                    self.tableWidget.item(item[0], item[1]).setFont(QFont(font.family(),int(self.font_size_list.loc[item[0],item[1]])))
                    self.font_style_list.iloc[item[0], item[1]] = font.family()
                except:
                    continue

    def changeFontSize(self,size):
        XYindex = self.getIndex()
        for item in XYindex:
            try:
                self.dynamic_variable[f'btnRightClick{item[0]},{item[1]}'].setStyleSheet("background-color:transparent;"
                                                                                         "border-width:1px;border-style:outset;"
                                                                                         "font: {}pt {};".format(int(size),self.font_style_list.loc[item[0],item[1]]))
                self.font_size_list.iloc[item[0],item[1]] = int(size)
            except:
                try:
                    self.tableWidget.item(item[0], item[1]).setFont(QFont(self.font_style_list.loc[item[0],item[1]], int(size), QFont.Black))
                    self.font_size_list.iloc[item[0], item[1]] = int(size)
                except:
                    continue

    # 删除最后列
    def delOneCol(self):
        index = self.tableWidget.columnCount()
        if index:
            self.tableWidget.removeColumn(index - 1)
            temp_delList = []
            for item in self.count_votes:
                if item[1] == index - 1:
                    temp_delList.append(item)
            for item in temp_delList:
                self.count_votes.remove(item)
            temp_delList = []
            for item in self.info_votes:
                if item[1] == index - 1:
                    temp_delList.append(item)
            for item in temp_delList:
                self.info_votes.remove(item)
            self.font_size_list.drop(self.font_size_list.columns[[-1, ]], axis=1, inplace=True)
            self.font_style_list.drop(self.font_style_list.columns[[-1, ]], axis=1, inplace=True)

    # 删除最后行
    def delOneLine(self):
        index = self.tableWidget.rowCount()
        if index:
            self.tableWidget.removeRow(index - 1)
            temp_delList = []
            for item in self.count_votes:
                if item[0] == index - 1:
                    temp_delList.append(item)
            for item in temp_delList:
                self.count_votes.remove(item)
            temp_delList = []
            for item in self.info_votes:
                if item[0] == index - 1:
                    temp_delList.append(item)
            for item in temp_delList:
                self.info_votes.remove(item)
            self.font_size_list.drop([len(self.font_size_list) - 1], inplace=True)
            self.font_style_list.drop([len(self.font_style_list) - 1], inplace=True)

    # 在最后行添加一行
    def addOneLine(self):
        index = self.tableWidget.rowCount()
        self.tableWidget.insertRow(index)
        if index == 0:
            self.addOneCol()
        self.font_size_list.loc[self.font_size_list.shape[0]] = [18 for i in range(self.font_size_list.shape[1])]
        self.font_style_list.loc[self.font_style_list.shape[0]] = ["仿宋" for i in range(self.font_style_list.shape[1])]




    # 在最后列添加一列
    def addOneCol(self):
        index = self.tableWidget.columnCount()
        self.tableWidget.insertColumn(index)
        self.font_size_list[self.font_size_list.shape[1]] = [19 for i in range(self.font_size_list.shape[0])]
        self.font_style_list[self.font_style_list.shape[1]] = ["仿宋" for i in range(self.font_style_list.shape[0])]

    # 窗口满屏显示与正常大小显示
    def windowVisible(self,status):
        if status:
            self.showFullScreen()
            self.pushButton_windowStatus.setStyleSheet("#pushButton_windowStatus{\n"
                                                       "    \n"
                                                       "    border-image: url(:/vote/image/缩小.png);\n"
                                                       "    border-width: 5px;\n"
                                                       "}\n"
                                                       "#pushButton_windowStatus:hover\n"
                                                       "{\n"
                                                       "    \n"
                                                       "    border-image: url(:/vote/image/缩小-press.png);\n"
                                                       "    border-width: 0px;\n"
                                                       "}\n"
                                                       " \n"
                                                       "#pushButton_windowStatus:pressed\n"
                                                       "{\n"
                                                       "    border-image: url(:/vote/image/缩小-press.png);\n"
                                                       "    border-width: 3px;\n"
                                                       "\n"
                                                       "}\n"
                                                       " ")
        else:
            self.showNormal()
            self.pushButton_windowStatus.setStyleSheet("#pushButton_windowStatus{\n"
                                                       "    \n"
                                                       "    border-image: url(:/vote/image/fullscreen.png);\n"
                                                       "    border-width: 5px;\n"
                                                       "}\n"
                                                       "#pushButton_windowStatus:hover\n"
                                                       "{\n"
                                                       "    \n"
                                                       "    border-image: url(:/vote/image/fullscreen-press.png);\n"
                                                       "    border-width: 0px;\n"
                                                       "}\n"
                                                       " \n"
                                                       "#pushButton_windowStatus:pressed\n"
                                                       "{\n"
                                                       "    border-image: url(:/vote/image/fullscreen-press.png);\n"
                                                       "    border-width: 3px;\n"
                                                       "\n"
                                                       "}\n"
                                                       " ")

    # 重置表格（全删除）
    def resetTable(self):
        for item in self.count_votes:
            self.tableWidget.removeCellWidget(item[0], item[1])
        for item in self.info_votes:
            self.tableWidget.removeCellWidget(item[0], item[1])
        self.count_votes = []
        self.info_votes = []
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.font_size_list = pd.DataFrame()
        self.font_style_list = pd.DataFrame()
        self.lineEdit_row.setText("")
        self.lineEdit_column.setText("")

    # 隐藏\显示右侧功能区和表头、网格
    def visibleMenu(self):
        if self.menu_visible:
            self.groupBox.hide()
            self.menu_visible = 0
            self.pushButton_menu.setStyleSheet("#pushButton_menu{\n"
                                               "    border-image: url(:/vote/image/左箭头.png);\n"
                                               "    border-width: 5px;\n"
                                               "}\n"
                                               "#pushButton_menu:hover\n"
                                               "{\n"
                                               "    border-image: url(:/vote/image/左箭头-press.png);\n"
                                               "    border-width: 0px;\n"
                                               "}\n"
                                               " \n"
                                               "#pushButton_menu:pressed\n"
                                               "{\n"
                                               "    border-image: url(:/vote/image/左箭头-press.png);\n"
                                               "    border-width: 3px;\n"
                                               "\n"
                                               "}\n"
                                               " ")
        else:
            self.groupBox.show()
            self.menu_visible = 1
            self.pushButton_menu.setStyleSheet("#pushButton_menu{\n"
                                               "    border-image: url(:/vote/image/右箭头.png);\n"
                                               "    border-width: 5px;\n"
                                               "}\n"
                                               "#pushButton_menu:hover\n"
                                               "{\n"
                                               "    border-image: url(:/vote/image/右箭头-press.png);\n"
                                               "    border-width: 0px;\n"
                                               "}\n"
                                               " \n"
                                               "#pushButton_menu:pressed\n"
                                               "{\n"
                                               "    border-image: url(:/vote/image/右箭头-press.png);\n"
                                               "    border-width: 3px;\n"
                                               "\n"
                                               "}\n"
                                               " ")

    # 清空选中单元格内容，含控件
    def clearCell(self):
        XYindex = self.getIndex()
        for item in XYindex:
            self.tableWidget.removeCellWidget(item[0],item[1])
            self.tableWidget.takeItem(item[0],item[1])
            try:
                self.count_votes.remove([item[0],item[1]])
            except:
                pass
            try:
                self.info_votes.remove([item[0],item[1]])
            except:
                pass

    # 表格中右键功能
    def generateMenu(self, pos):
        if self.tableWidget.columnCount():
            XYindex = self.getIndex()
            if [self.tableWidget.currentRow(),self.tableWidget.currentColumn()] not in self.count_votes:
                # 获取点击行号
                for i in self.tableWidget.selectionModel().selection().indexes():
                    rowNum = i.row()
                    columnNum = i.column()
                menu = QMenu()
                item1 = menu.addAction("居中显示")
                item2 = menu.addAction("合并单元格")
                item3 = menu.addAction("拆分单元格")
                item4 = menu.addAction("设置计票单元格")
                item5 = menu.addAction("添加单元格边框")
                item6 = menu.addAction("清空选中单元格")
                # 转换坐标系
                screenPos = self.tableWidget.mapToGlobal(pos)
                print(screenPos)
                # 被阻塞
                action = menu.exec(screenPos)
                if action == item1:
                    print('选择了第1个菜单项：居中显示')
                    try:
                        for item in XYindex:
                                try:
                                    self.tableWidget.item(item[0], item[1]).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                except Exception as e:
                                    continue
                    except Exception as e:
                        pass
                if action == item2:
                    print('选择了第2个菜单项：合并单元格')
                    self.combineCell()

                elif action == item3:
                    print('选择了第3个菜单项：拆分单元格')
                    self.splitCell()

                elif action == item4:
                    print('选择了第4个菜单项：设置计票单元格')
                    try:
                        for item in XYindex:
                            try:
                                self.tableWidget.setCellWidget(item[0],item[1],self.createWidgets(item[0],item[1]))
                            except Exception as e:
                                continue
                    except Exception as e:
                        pass
                elif action == item5:
                    print('选择了第5个菜单项：添加边框')
                    try:
                        for item in XYindex:
                            try:
                                self.tableWidget.setCellWidget(item[0],item[1],self.createWidgetsForAddLine(item[0],item[1]))
                            except Exception as e:
                                continue
                    except Exception as e:
                        pass
                elif action == item6:
                    print('选择了第6个菜单项：清空选中单元格')
                    self.clearCell()

        else:
            pass

    # 合并单元格
    def combineCell(self):
        try:
            combine_list = self.getIndex()
            self.tableWidget.setSpan(combine_list[0][0], combine_list[0][1],
                                     combine_list[-1][0]-combine_list[0][0] + 1,
                                     combine_list[-1][1]-combine_list[0][1] + 1)

        except Exception as e:
            pass

    # 获取选中单元格的坐标
    def getIndex(self):
        combine_list = []
        # 点击事件获取所选行列
        try:
            for item in self.tableWidget.selectionModel().selectedIndexes():
                combine_list.append([item.row(),item.column()])
        except Exception as e:
            pass
        if len(combine_list) == 1:
            combine_list.append([combine_list[0][0],combine_list[0][1]])
        return combine_list

    # 拆分单元格
    def splitCell(self):
        self.tableWidget.clearSpans()

    # 制作表格白板
    def makeTable(self,row,column):
        try:
            self.tableWidget.setRowCount(int(row))  # 设置表格的行数
            self.tableWidget.setColumnCount(int(column))  # 设置表格的列数
            self.font_size_list = pd.DataFrame([[19 for i in range(int(column))] for j in range(int(row))])
            self.font_style_list = pd.DataFrame([["仿宋" for i in range(int(column))] for j in range(int(row))])
        except Exception as e:
            print("{}\t请输入整数".format(str(e)))


    # 填充窗口背景
    def resizeEvent(self, event):
        palette = QPalette()
        pix = QPixmap(":/vote/image/演示文稿1.png")
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)

    def createWidgetsForAddLine(self,index_i,index_j):
        name = "{},{}".format(index_i, index_j)
        self.info_votes.append([index_i, index_j])
        self.dynamic_variable = globals()
        self.dynamic_variable[f'btnRightClick{name}'] = LineEdit(self)
        self.dynamic_variable[f'btnRightClick{name}'].setStyleSheet("background-color:transparent;"
                                                                    "border-width:1px;border-style:outset;"
                                                                    "font: 19pt '仿宋';")
        self.dynamic_variable[f'btnRightClick{name}'].setContextMenuPolicy(Qt.NoContextMenu)
        self.dynamic_variable[f'btnRightClick{name}'].setAlignment(Qt.AlignHCenter)
        self.dynamic_variable[f'btnRightClick{name}'].focus_in_signal.connect(lambda :self.focus_in(index_i,index_j))
        # self.dynamic_variable[f'btnRightClick{name}'].clicked.connect(lambda :self.setFontSizeAtDYN)
        try:
            self.dynamic_variable[f'btnRightClick{name}'].setText(str(
                self.tableWidget.item(index_i, index_j).text()
            ))
            self.tableWidget.item(index_i,index_j).setText("")
        except:
            self.dynamic_variable[f'btnRightClick{name}'].setText("")
        return self.dynamic_variable[f'btnRightClick{name}']

    def createWidgets(self,index_i,index_j):
        self.tableWidget.takeItem(index_i,index_j)
        name = "{},{}".format(index_i,index_j)
        self.count_votes.append([index_i,index_j])
        self.dynamic_variable = globals()
        self.dynamic_variable[f'btnRightClick{name}'] = RightClickButton(self)
        self.dynamic_variable[f'btnRightClick{name}'].setStyleSheet("background-color:transparent;"
                                                                    "border-width:1px;border-style:outset;"
                                                                    "font: 19pt '仿宋';")
        self.dynamic_variable[f'btnRightClick{name}'].setContextMenuPolicy(Qt.NoContextMenu)
        self.dynamic_variable[f'btnRightClick{name}'].setText('')
        self.dynamic_variable[f'btnRightClick{name}'].clickedSignal.connect(self.test)
        self.dynamic_variable[f'btnRightClick{name}'].setAlignment(Qt.AlignHCenter)
        self.dynamic_variable[f'btnRightClick{name}'].focus_in_signal.connect(lambda: self.focus_in(index_i, index_j))
        # self.tableWidget.item(index_i, index_j).setText("")
        return self.dynamic_variable[f'btnRightClick{name}']

    def test(self, flag):
        if flag:
            # self.btnRightClick.setText("单击成功")
            print("左")
            i = self.tableWidget.currentRow()
            j = self.tableWidget.currentColumn()
            try:
                num_init = self.dynamic_variable['btnRightClick{},{}'.format(i,j)].text()
                num = str(int(num_init) + 1)
                self.dynamic_variable['btnRightClick{},{}'.format(i,j)].setText(num)
            except:
                self.dynamic_variable['btnRightClick{},{}'.format(i,j)].setText('1')
        else:
            # self.btnRightClick.setText("右击成功")
            print("右")
            i = self.tableWidget.currentRow()
            j = self.tableWidget.currentColumn()
            try:
                num = str(int(self.dynamic_variable['btnRightClick{},{}'.format(i, j)].text()) - 1)
                self.dynamic_variable['btnRightClick{},{}'.format(i, j)].setText(num)
            except:
                self.dynamic_variable['btnRightClick{},{}'.format(i,j)].setText('0')

    @pyqtSlot()
    def focus_in(self,row,col):
        self.doubleSpinBox.setValue(float(
            self.font_size_list.loc[row, col]))
        self.fontComboBox.setCurrentFont(QFont(self.font_style_list.loc[row, col]))

class RightClickButton(QLineEdit):
    clickedSignal = pyqtSignal(bool)  # 定义带参信号
    focus_in_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(RightClickButton, self).__init__(parent)

    def focusInEvent(self, event):
        self.focus_in_signal.emit()
        super().focusInEvent(event)

    def mouseDoubleClickEvent(self, e):
        self.mousePressEvent(e)

    def mousePressEvent(self, event):  # 重定义该函数，对不同的操作释放不同的信号参数
        if event.buttons() == Qt.LeftButton:
            self.clickedSignal.emit(True)
        elif event.buttons() == Qt.RightButton:
            self.clickedSignal.emit(False)

class LineEdit(QLineEdit):
    focus_in_signal = pyqtSignal()
    def focusInEvent(self, event):
        self.focus_in_signal.emit()
        super().focusInEvent(event)



# main window
def menu():
    app = QApplication(sys.argv)  # 创建一个桌面应用程序
    myShow = myWindow()  # 创建主窗口
    myShow.show()

    sys.exit(app.exec_())
if __name__ == '__main__':
    menu()
