# Required imports for basic PyQt application
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import sys

def window():
    
    # Gives the application information on your OS setup
    app = QApplication(sys.argv)
    
    # QMainWindows is the main view you see; People also use QWidget
    win = QMainWindow()
    
    # setGeometry(xpos, ypos, width, height)
    # xpos, ypos are where the top left hand corner of the window is displayed
    win.setGeometry(200, 200, 500, 500)

    win.setWindowTitle("BadgerCAN")

    # Adding text to the window
    label = QtWidgets.QLabel(win)
    label.setText("BadgerCAN")

    # move(xpos, ypos)
    label.move(0, 0)

    # Display the window
    win.show()

    # Waits for QApplication to exit, then executes a clean exit
    sys.exit(app.exec_())

window()