from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw

from heaty.gui.settings import settings
from heaty.gui.user_input.form import ButtonBox


# noinspection PyArgumentList
class AboutDialog(qtw.QDialog):

    def __init__(self, parent):
        super().__init__(parent, modal=True)
        self.setWindowTitle('About')
        self.resize(400, 400)
        self.setLayout(qtw.QVBoxLayout())

        tabs = qtw.QTabWidget(self)
        tabs.addTab(InfoTab(tabs), 'Info')
        tabs.addTab(LicenseTab(tabs), 'License')
        self.layout().addWidget(tabs)

        buttonbox = ButtonBox(self, labels=['Close'], slots=[self.close])
        self.layout().addWidget(buttonbox)


class InfoTab(qtw.QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(qtw.QHBoxLayout())

        label = qtw.QLabel(self)
        label.setAlignment(qtc.Qt.AlignTop)
        ICON_PATH = settings.find_file(settings.RESOURCES_PATH, 'house.ico')
        pixmap = qtg.QPixmap(ICON_PATH)
        pixmap = pixmap.scaled(64, 64, qtc.Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        self.layout().addWidget(label)

        textbox = qtw.QTextEdit(self, readOnly=True)
        textbox.setFrameStyle(qtw.QFrame.NoFrame)
        self.layout().addWidget(textbox)

        ABOUT_PATH = settings.find_file(settings.RESOURCES_PATH, 'about.html')
        with open(ABOUT_PATH) as fh:
            lic = fh.read()
        textbox.setText(lic)


class LicenseTab(qtw.QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(qtw.QVBoxLayout())

        textbox = qtw.QTextEdit(self, readOnly=True)
        textbox.setFrameStyle(qtw.QFrame.NoFrame)
        self.layout().addWidget(textbox)

        LICENSE_PATH = settings.find_file(settings.RESOURCES_PATH, 'license.html')
        with open(LICENSE_PATH) as fh:
            lic = fh.read()
        textbox.setText(lic)
