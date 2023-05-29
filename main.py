
from calendar_1 import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())