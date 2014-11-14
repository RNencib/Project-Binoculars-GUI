import sys
from PyQt4 import QtGui

from Window import *


def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = SimpleGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
