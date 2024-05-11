# notebook2py

I learned to code python in Jupyter Notebook.  It works for me.  To that end, when the script is done, reformatting from .ipynb to .py is a bit of a pain.  In order to save time to work on other things, I created notebook2py.  It's pretty simple.  It will parse the xml of your .ipynb file and spit out a .py file.  It uses a GUI created with PyQt5.  You'll need the following import statements:

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog, QLineEdit, QTextEdit, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import nbformat
import os

I hope this helps you save some time!
