import sys
from PyQt5 import QtWidgets as qtw
from heaty.gui.main_window import MainWindow


def main():
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
