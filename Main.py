#############   https://pypi.tuna.tsinghua.edu.cn/simple

import sys
import os
import cv2
import json
import shutil

from PyQt5.QtCore import pyqtSignal
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtCore import QFile, QSize, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog, QLabel, QWidget, QVBoxLayout


rowPicture_Path = ''
target_Path = ''
registerPicture_Path = ''
targetPath_list = []                #生成目标文件夹中已经存在的子文件夹名


########结构体
class Person_info:
    def __init__(self):   #,id,gender,name,age,is_facemask,glasses,race,beard,checked,mark_name,check_name
        self.id = ' '              #空是未标注（默认属性）
        self.gender = 0            #0未标注（默认属性） 1男　2 女
        self.name = ' '            #姓名
        self.age = 0               #年龄：0未标注 （默认属性）
        self.is_facemask = 0       #是否戴口罩：0未标注（默认属性） 1带了 2没带
        self.glasses = 0           #眼镜：0未标注（默认属性）　1普通眼镜　2太阳镜 3不戴眼镜
        self.race = 0              #人种：0未标注（默认属性） 1黄种人 2黑人 3白人
        self.beard = 0             #是否有胡子：0未标注（默认属性）1有 2没有
        self.is_checked = 0           #是否已经审核：0未初始化  1审核通过　2审核不过
        self.marked_name = ' '       #标注人姓名
        self.checked_name = ' '      #审核人姓名
############写成json文件
def to_json(person,path):
    dict =  {
        'id':person.id,
        'gender':person.gender,
        'name':person.name,
        'age':person.age,
        'is_facemask':person.is_facemask,
        'glasses':person.glasses,
        'race':person.race,
        'beard':person.beard,
        'is_checked':person.is_checked,
        'marked_name':person.marked_name,
        'checked_name':person.checked_name
    }
    file_name = person.id + '.json'
    save_path = path + '/' + file_name
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(dict, ensure_ascii=False))





class UI_Mian_Windows():
    #########初始化窗口设置
    def __init__(self):
        app = QApplication(sys.argv)
        ui_file = QFile("test.ui")
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        # 在这里加入信号触发、空间控制等代码

        self.window.pushButton.clicked.connect(self.input_raw_data)         #【选择标注文件夹】按钮所绑定的事件
        self.window.pushButton_3.clicked.connect(self.input_register_data)  #【选择注册文件夹】按钮所绑定的事件
        self.window.pushButton_4.clicked.connect(self.get_save_Info)        #【下一张】按钮所绑定的事件
        self.window.pushButton_2.clicked.connect(self.get_targetPath)       #【选择目标文件夹】按钮所绑定的事件

        # 添加结束
        self.window.show()
        sys.exit(app.exec_())

    ##################获取目标文件夹路径
    def get_targetPath(self):
        directory = QFileDialog.getExistingDirectory(self.window, "选取文件夹", "C:/")
        target_Path = directory
        print(target_Path)

    ###########导入原始未标注图片
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
                    listimages.append(os.path.join(root, file).replace('\\','/'))
        img = cv2.imread(listimages[0])  # opencv读取图片
        print(listimages[0])
        rowPicture_Path = listimages[0]
        res = cv2.resize(img, (800, 600), interpolation=cv2.INTER_CUBIC)  # 用cv2.resize设置图片大小
        img2 = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
        _image = QtGui.QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,
                              QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
        jpg_out = QtGui.QPixmap(_image)  # 转换成QPixmap
        self.window.label.setPixmap(jpg_out)  # 设置图片显示

        # png = QtGui.QPixmap('C:/Users/GEORGE/Desktop/myself/1.jpg') #listimages[0]
        # # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
        # self.window.label.setScaledContents(True)  # 图片自适应
        # self.window.label.setPixmap(png)

    ################导入注册图片
    def input_register_data(self):
        registimages = []
        filenum = 0
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
                    filenum += 1
        img = cv2.imread(registimages[0])  # opencv读取图片
        res = cv2.resize(img, (800, 600), interpolation=cv2.INTER_CUBIC)  # 用cv2.resize设置图片大小
        img2 = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
        _image = QtGui.QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,
                              QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
        jpg_out = QtGui.QPixmap(_image)  # 转换成QPixmap

        MyTable = self.window.tableWidget
        # # 实例化表格窗口条目
        # item = QTableWidgetItem()
        #  # 用户点击表格时，图片被选中
        # item.setFlags(Qt.ItemIsEnabled)
        # # 图片路径设置与图片加载
        # icon = QIcon(r'C:/Users/GEORGE/Desktop/myself/11.png')
        # item.setIcon(QIcon(icon))
        # # 输出当前进行的条目序号
        # # 将条目加载到相应行列中
        # self.window.tableWidget.setItem(0, 0, item)
        MyTable.setHorizontalHeaderLabels(['姓名', '身高', '体重'])

        self.qlabelraw = QtWidgets.QLabel(MyTable)
        self.qlabelraw.setGeometry(QtCore.QRect(0, 0, 200, 200))
        self.qlabelraw.setObjectName("qlabelraw")
        self.qlabelraw.setPixmap(jpg_out)
        self.setTableContext(registimages)

        ###############设置表格内容
    def setTableContext(self, registimages):
        filenum = len(registimages)
        flag = 0
        for j in range(4):
            for i in range(int(filenum / 4)):
                self.setRowData(i, j, registimages[flag])
                flag += 1
        if filenum % 4:
            for k in range(int(filenum / 4) * 4, filenum):
                self.setRowData(int(filenum / 4), k % 4, registimages[k])

        QApplication.processEvents()

    def label_pic_click(self):
        print('单击放大')

    def setRowData(self, row, col, imgurl):
        ##########在table中添加控件

        img = cv2.imread(imgurl)  # opencv读取图片
        res = cv2.resize(img, (218, 218), interpolation=cv2.INTER_CUBIC)  # 用cv2.resize设置图片大小
        img2 = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
        _image = QtGui.QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,
                              QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
        jpg_out = QtGui.QPixmap(_image)  # 转换成QPixmap
        clickable_image = QClickableImage(218, 218, jpg_out, imgurl)

        self.window.tableWidget.setCellWidget(row, col, clickable_image)

    #################点击下一张按钮功能模块
    def get_save_Info(self):
        p = Person_info()
        self.getInfo(p)
        id = p.id
        save_path = target_Path + '/' + id           #拿到保存json文件的路径，若没有相应的文件夹则创建
        if(os.path.exists(save_path) == False):
            os.mkdir(save_path)
        to_json(p,save_path)     #将标注信息存储到json文件中
        picture_save_path = save_path + '/' + id + '.jpg'
        shutil.copy(rowPicture_Path, picture_save_path)

    ##########获取标注信息
    def getInfo(self,p):
        def get_Gender(self):
            if self.window.radioButton.isChecked() == True:
                return 2
            elif self.window.radioButton_2.isChecked() == True:
                return 1
            else:
                return 0
        def get_Maskface(self):
            if self.window.radioButton_4.isChecked() == True:
                return 2
            elif self.window.radioButton_3.isChecked() == True:
                return 1
            else:
                return 0
        def get_glasses(self):
            if self.window.radioButton_7.isChecked() == True:
                return 3
            elif self.window.radioButton_5.isChecked() == True:
                return 2
            elif self.window.radioButton_6.isChecked() == True:
                return 1
            else:
                return 0
        def get_Race(self):
            if self.window.radioButton_10.isChecked() == True:
                return 3
            elif self.window.radioButton_8.isChecked() == True:
                return 2
            elif self.window.radioButton_9.isChecked() == True:
                return 1
            else:
                return 0
        def get_Beard(self):
            if self.window.radioButton_11.isChecked() == True:
                return 2
            elif self.window.radioButton_12.isChecked() == True:
                return 1
            else:
                return 0
        p.id = self.window.lineEdit.text()
        p.gender = get_Gender(self)
        p.age = self.window.lineEdit_2.text()
        p.is_facemask = get_Maskface(self)
        p.glasses = get_glasses(self)
        p.race = get_Race(self)
        p.beard = get_Beard(self)
        p.is_checked = self.window.lineEdit.text()
        p.marked_name = self.window.lineEdit_3.text()
        # p.checked_name = self.window.lineEdit_3.text()



class MyLabel(QLabel):
    def __init__(self, pixmap=None, image_id=None):
        QLabel.__init__(self)
        self.pixmap = pixmap
        self.image_id = image_id
        self.setPixmap(pixmap)

        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):

        if event.buttons() == QtCore.Qt.LeftButton:  # 左键按下 ,缩略图

            print("单击鼠标左键 放大")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.RightButton:  # 右键按下

            print("单击鼠标右键  放大")



class QClickableImage(QWidget):
    image_id = ''

    def __init__(self, width=0, height=0, pixmap=None, image_id=''):
        QWidget.__init__(self)

        self.width = width
        self.height = height
        self.pixmap = pixmap

        self.layout = QVBoxLayout(self)

        if self.width and self.height:
            self.resize(self.width, self.height)
        if self.pixmap and image_id:
            pixmap = self.pixmap.scaled(QSize(self.width, self.height), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label1 = MyLabel(pixmap, image_id)
            self.label1.setObjectName('label1')

            self.layout.addWidget(self.label1)
            print(image_id)
        # if image_id:
        #     self.image_id = image_id
        #     self.lable2.setText(image_id.split('\\')[-1])
        #     self.lable2.setAlignment(Qt.AlignCenter)
        #     ###让文字自适应大小
        #     self.lable2.adjustSize()
        #     self.layout.addWidget(self.lable2)
        self.setLayout(self.layout)

    clicked = pyqtSignal(object)
    rightClicked = pyqtSignal(object)

    def imageId(self):
        return self.image_id


if __name__ == "__main__":
    UI_Mian_Windows()