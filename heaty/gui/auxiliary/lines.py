from PyQt5 import QtWidgets as qtw


class QHLine(qtw.QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(qtw.QFrame.HLine)
        self.setFrameShadow(qtw.QFrame.Sunken)


class QVLine(qtw.QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(qtw.QFrame.VLine)
        self.setFrameShadow(qtw.QFrame.Sunken)
