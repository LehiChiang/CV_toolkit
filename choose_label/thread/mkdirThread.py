import os
from shutil import copyfile
from traceback import format_exc

from PyQt5.QtCore import QThread, pyqtSignal


class makeDirThread(QThread):

    signal = pyqtSignal(str, str)

    def __init__(self, savepath):
        super(makeDirThread, self).__init__()
        self.savepath = savepath

    def run(self):
        try:
            self.saveAnnotationFolder = os.path.join(self.savepath, 'VOCdevkit', 'Annotation')
            os.makedirs(self.saveAnnotationFolder)
            self.saveImageFolder = os.path.join(self.savepath, 'VOCdevkit', 'JPEGImages')
            os.makedirs(self.saveImageFolder)
            self.signal.emit(self.saveImageFolder, self.saveAnnotationFolder)
        except Exception:
            print(format_exc())

class copyFileThread(QThread):

    signal = pyqtSignal(int)

    def __init__(self, dir1, dir2, dir3, dir4):
        super(copyFileThread, self).__init__()
        self.dir1 = dir1
        self.dir2 = dir2
        self.dir3 = dir3
        self.dir4 = dir4

    def run(self):
        try:
            copyfile(self.dir1, self.dir2)
            copyfile(self.dir3, self.dir4)
            self.signal.emit(1)
        except Exception:
            print(format_exc())
