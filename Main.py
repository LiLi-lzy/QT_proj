import sys
import os

from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog


class UI_Mian_Windows():


    def leftclicked(self):
        print("hello")

    def __init__(self):
        app = QApplication(sys.argv)
        ui_file = QFile("test.ui")
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        # 在这里加入信号触发、空间控制等代码

        self.window.pushButton.clicked.connect(self.input_raw_data)
        self.window.pushButton_3.clicked.connect(self.input_register_data)

        # 添加结束
        self.window.show()
        sys.exit(app.exec_())

    def input_raw_data(self):
        listimages = []
        directory = QFileDialog.getExistingDirectory(self.window, "选取文件夹", "C:/")
        if directory == "":
            print("\n取消选择")
            return
        else:
            # 删选并添加文件到list中
            for root, dirs, files in os.walk(directory):
                for file in files:
                    # print(os.path.join(root, file))
                    listimages.append(os.path.join(root, file))
        png = QtGui.QPixmap(listimages[0])
        # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
        self.window.label.setPixmap(png)



    def input_register_data(self):
        registimages = []
        directory = QFileDialog.getExistingDirectory(self.window, "选取文件夹", "C:/")
        if directory == "":
            print("\n取消选择")
            return
        else:
            # 删选并添加文件到list中
            for root, dirs, files in os.walk(directory):
                for file in files:
                    # print(os.path.join(root, file))
                    registimages.append(os.path.join(root, file))
        png = QtGui.QPixmap(registimages[0])


        MyTable = self.window.tableWidget
        # MyTable.setHorizontalHeaderLabels(['姓名','身高','体重'])
        # self.window.tableWidget.setPixmap

        self.qlabelraw=QtWidgets.QLabel(MyTable)
        self.qlabelraw.setGeometry(QtCore.QRect(0, 0, 100, 100))
        self.qlabelraw.setObjectName("qlabelraw")
        self.qlabelraw.setPixmap(png)







if __name__ == "__main__":

    UI_Mian_Windows()