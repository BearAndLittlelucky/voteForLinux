# from PIL import Image
# im = Image.open('F:/PyTotalItems/vote/UI/image/548e8391bb19458d8b3478b426175a9d.jpg').convert('RGBA')
# im.save('./changed.png')
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
#
#
# class GUI(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.createWidgets()
#         self.setupUI()
#
#     def setupUI(self):
#         self.show()
#
#     def createWidgets(self):
#         self.btnRightClick = RightClickButton(self)
#         self.btnRightClick.setText("左/右击功能测试")
#         self.btnRightClick.clickedSignal.connect(self.test)
#
#     def test(self, flag):
#         if flag:
#             self.btnRightClick.setText("单击成功")
#             print("左")
#         else:
#             self.btnRightClick.setText("右击成功")
#             print("右")
#
#
# class RightClickButton(QPushButton):
#     clickedSignal = pyqtSignal(bool)  # 定义带参信号
#
#     def __init__(self, parent=None):
#         super(RightClickButton, self).__init__(parent)
#
#     def mousePressEvent(self, event):  # 重定义该函数，对不同的操作释放不同的信号参数
#         if event.buttons() == Qt.LeftButton:
#             self.clickedSignal.emit(True)
#         elif event.buttons() == Qt.RightButton:
#             self.clickedSignal.emit(False)
#
#
# if __name__ == '__main__':
#     app = QApplication([])
#     ui = GUI()
#     app.exec_()
import pandas as pd
import numpy as np
listtemp = [["仿宋" for i in range(3)] for j in range(4)]
data_list = pd.DataFrame()
# leng = len(data_list[0])
# data_list[len(data_list[0])-1] = [19 for i in range(len(data_list))]
# data_list[4] = [19 for i in range(len(data_list))]
# data_list = data_list.append([[18 for i in range(2)]])
# data_list.insert(int(len(data_list)-1),[i for i in range(len(data_list[0]))],new_list)
# data_list.loc[data_list.shape[0]] = [18 for i in range(data_list.shape[1])]
data_list[data_list.shape[1]] = [19 for i in range(data_list.shape[0])]
# data_list.drop([len(data_list) - 1], inplace=True)
# data_list.drop(data_list.columns[[-1,]], axis=1, inplace=True)
print(data_list)