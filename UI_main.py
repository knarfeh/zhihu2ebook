#!/src/bin/env python
# -*- coding:utf-8 -*-

import sys

from PyQt4.QtGui import QApplication
from src.gui.ui import MainWindow


reload(sys)
sys.setdefaultencoding('utf8')


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
