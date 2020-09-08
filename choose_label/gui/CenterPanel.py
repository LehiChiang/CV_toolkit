from PyQt5.QtWidgets import QWidget, QTextEdit,  QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
import cv2
from qtpy import QtCore


class CenterWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.bottom_layout = QHBoxLayout()

        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)

        self.img_label = QLabel()
        self.xml_edit = QTextEdit()
        self.xml_edit.setFocusPolicy(QtCore.Qt.NoFocus)

        self.top_layout.addStretch(1)
        self.top_layout.addWidget(self.img_label)
        self.top_layout.addStretch(1)

        self.bottom_layout.addWidget(self.xml_edit)
        self.setLayout(self.main_layout)
        self.show()

    def loadimage(self,path):
        self.image = cv2.imread(path)
        self.showimage()

    def showimage(self):
        qimageformat = QImage.Format_Indexed8
        if len(self.image.shape)==3:
            if self.image.shape[2]==4:
                qimageformat = QImage.Format_RGBA8888
            else:
                qimageformat = QImage.Format_RGB888
        img = QImage(self.image,self.image.shape[1],self.image.shape[0],self.image.strides[0],qimageformat)
        img = img.rgbSwapped()
        self.img_label.setPixmap(QPixmap.fromImage(img))

    def read_xml(self, path):
        f = open(path, 'r')
        with f:
            data = f.read()
            self.xml_edit.setText(data)
