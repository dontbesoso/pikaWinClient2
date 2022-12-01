#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QApplication)
from logownik import logownik

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    okno = logownik()
    sys.exit(app.exec_())