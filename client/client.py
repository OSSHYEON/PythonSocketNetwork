import sys, signal, socketio
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QListWidgetItem, QLineEdit, QListWidget
from PyQt5.QtGui import QIcon


ui = uic.loadUiType("client_ui.ui")[0]

class client_window(QWidget, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_window = client_window()
    chat_window.setWindowTitle('oss talk')
    chat_window.setWindowIcon(QIcon('teddy-bear.png'))
    chat_window.show()
    try:
        app.exec_()
    except Exception as e:
        print("Error 발생! ㅠㅠ : ", e)
    else:
        print("-"*10,"잘가요", "-"*10)
