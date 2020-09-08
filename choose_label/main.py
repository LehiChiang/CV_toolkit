import glob
import os
import sys

from qtawesome import icon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QDesktopWidget, QLabel, \
    QFileDialog
from PyQt5.QtGui import QCursor

from gui.CenterPanel import CenterWidget
from thread.mkdirThread import makeDirThread, copyFileThread


class Choose_Label_MainWIndow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.imagefilepath = ''
        self.annotationfilepath = ''
        self.savepath = ''
        self.currentIndex = 0
        self.tmppath = os.getcwd()
        self.iconsizenum = 25
        self.widthRatio = 0.65
        self.heightRatio = 0.7
        desktop = QApplication.desktop()
        self.winWidth = desktop.width()
        self.winHeight = desktop.height()
        self.screenWidth = self.winWidth * self.widthRatio
        self.screenHeight = self.winHeight * self.heightRatio
        self.initUI()

    def initUI(self):
        self.statusBar()
        self.initAction()
        self.Creat_Menu()
        self.Creat_ToolBar()
        self.resize(self.screenWidth, self.screenHeight)
        self.centerWidget = CenterWidget()
        self.setCentralWidget(self.centerWidget)
        self.setWindowTitle('Chestimouse——数据集选择工具')
        self.show()

    def Creat_Menu(self):
        self.menu = self.menuBar()

        fileMenu = self.menu.addMenu('&文件')
        fileMenu.addAction(self.exitAction)

    def initAction(self):
        self.preLabelAction = QAction(icon('fa.arrow-left', color='green'), '上一张', self)
        self.preLabelAction.setShortcut('a')
        self.preLabelAction.setStatusTip('浏览上一张数据')
        self.preLabelAction.triggered.connect(self.preLabelEvent)

        self.nextLabelAction = QAction(icon('fa.arrow-right', color='green'), '下一张', self)
        self.nextLabelAction.setShortcut('d')
        self.nextLabelAction.setStatusTip('浏览下一张数据')
        self.nextLabelAction.triggered.connect(self.nextLabelEvent)

        self.saveLabelAction = QAction(icon('fa.save', color='orange'), '保存', self)
        self.saveLabelAction.setShortcut('w')
        self.saveLabelAction.setStatusTip('保存此张数据')
        self.saveLabelAction.triggered.connect(self.saveLabelEvent)

        self.exitAction = QAction(icon('fa.times', color='red'), '退出', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('退出程序')
        self.exitAction.triggered.connect(self.close)

        self.openImageAction = QAction(icon('fa5.images', color='blue'), '图片文件路径', self)
        self.openImageAction.setShortcut('Ctrl+I')
        self.openImageAction.setStatusTip('选择图片文件路径')
        self.openImageAction.triggered.connect(self.openImageEvent)

        self.openAnnotationAction = QAction(icon('fa5.file-excel', color='blue'), 'Annotation文件路径', self)
        self.openAnnotationAction.setShortcut('Ctrl+A')
        self.openAnnotationAction.setStatusTip('选择Annotation文件路径')
        self.openAnnotationAction.triggered.connect(self.openAnnotationEvent)

        self.saveImageAction = QAction(icon('fa.download', color='blue'), '保存路径', self)
        self.saveImageAction.setShortcut('Ctrl+S')
        self.saveImageAction.setStatusTip('选择保存路径')
        self.saveImageAction.triggered.connect(self.saveImageEvent)

    def Creat_ToolBar(self):
        self.toolBar = QToolBar()
        self.addToolBar(Qt.LeftToolBarArea, self.toolBar)

        self.toolBar.addWidget(QLabel('加载'))
        self.toolBar.addAction(self.openImageAction)
        self.toolBar.addAction(self.openAnnotationAction)
        self.toolBar.addAction(self.saveImageAction)

        self.toolBar.addWidget(QLabel('操作'))
        self.toolBar.addAction(self.preLabelAction)
        self.toolBar.addAction(self.nextLabelAction)
        self.toolBar.addAction(self.saveLabelAction)
        self.toolBar.addAction(self.exitAction)

    def openImageEvent(self):
        self.imagefilepath = QFileDialog.getExistingDirectory(self, "选择图片文件路径", self.tmppath)
        self.tmppath = self.imagefilepath
        self.setStatusTip(self.imagefilepath)
        if self.imagefilepath!='' and self.annotationfilepath!='':
            self.load_data()

    def openAnnotationEvent(self):
        self.annotationfilepath = QFileDialog.getExistingDirectory(self, "选择Annotation文件路径", self.tmppath)
        self.tmppath = self.annotationfilepath
        self.setStatusTip(self.annotationfilepath)
        if self.imagefilepath!='' and self.annotationfilepath!='':
            self.load_data()

    def saveImageEvent(self):
        try:
            self.savepath = QFileDialog.getExistingDirectory(self, "选择保存路径", self.tmppath)
            self.tmppath = self.savepath
            self.setStatusTip(self.savepath)
            self.thread = makeDirThread(savepath=self.savepath)
            self.thread.signal.connect(self.mkdir_callback)
            self.thread.start()
        except Exception as e:
            print(e)

    def mkdir_callback(self,dir1, dir2):
        self.saveAnnotationFolder = dir2
        self.saveImageFolder = dir1

    def preLabelEvent(self):
        try:
            self.currentIndex -= 1
            self.path = self.imagelist[self.currentIndex]
            self.centerWidget.loadimage(self.path)
            self.centerWidget.read_xml(self.get_xmlfile_name(self.path))
        except Exception:
            self.currentIndex = 0

    def nextLabelEvent(self):
        try:
            self.currentIndex += 1
            self.path = self.imagelist[self.currentIndex]
            self.centerWidget.loadimage(self.path)
            self.centerWidget.read_xml(self.get_xmlfile_name(self.path))
        except Exception:
            self.currentIndex = 0

    def saveLabelEvent(self):
        xml_path = self.get_xmlfile_name(self.path)
        self.copythread = copyFileThread(self.path,
                                         os.path.join(self.saveImageFolder, self.path.split('\\')[-1]),
                                         xml_path,
                                         os.path.join(self.saveAnnotationFolder, xml_path.split('\\')[-1]))
        self.copythread.signal.connect(self.copy_callback)
        self.copythread.start()

    def copy_callback(self, index):
        if index == 1:
            self.setStatusTip('保存成功！')

    def load_data(self):
        pathnew = os.path.join(self.imagefilepath, "*.jpg")
        self.imagelist = glob.glob(pathnew)
        self.path = self.imagelist[self.currentIndex]
        self.centerWidget.loadimage(self.path)
        self.centerWidget.read_xml(self.get_xmlfile_name(self.path))

    def get_xmlfile_name(self, path):
        return os.path.join(self.annotationfilepath, path.split('\\')[-1].split('.')[0]+'.xml')

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    # 创建应用程序和对象
    app = QApplication(sys.argv)
    ex = Choose_Label_MainWIndow()
    sys.exit(app.exec_())
