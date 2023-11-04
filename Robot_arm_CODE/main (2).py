from PyQt5.QtWidgets import QApplication
import sys
from widget import Widget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widget(980, 560)
    sys.exit(app.exec())








