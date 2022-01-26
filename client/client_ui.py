import sys, signal, socketio
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QListWidgetItem, QLineEdit, QListWidget
from PyQt5.QtGui import QIcon
import client
from socket import *

ui = uic.loadUiType("client_ui.ui")[0]

class client_window(QWidget, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.client_socket = client.ClientSocket(self)
        self.connect_btn.setCheckable(True)
        self.bConnect = False

    def connectClicked(self):
        if self.client_socket.bConnect == False:
            ip = self.input_ip.text()
            port = self.input_port.text()
            if self.client_socket.connectServer(ip, int(port)):
                self.connect_btn.setText('종료')
            else:
                self.client_socket.stop()
                self.send_msg.clear()
                self.recv_msg.clear()
                self.connect_btn.setText('접속')
        else:
            self.client_socket.stop()
            self.seind_msg.clear()
            self.recv_msg.clear()
            self.connect_btn.setText('접속')

    def updateMsg(self, msg):
        self.connect_btn.setText('접속')
        self.recv_msg.addItem(QListWidgetItem(msg))

    def updateDisconnect(self):
        self.btn.setText('접속')

    def sendMsg(self):
        send_msg = self.send_msg.toPlainText()
        self.client_socket.send(send_msg)
        self.send_msg.clear()

    def clearMsg(self):
        self.recv_msg.clear()

    def closeEvent(self, e):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_window = client_window()
    chat_window.setWindowTitle('oss talk')
    chat_window.setWindowIcon(QIcon('message.png'))
    chat_window.show()
    try:
        app.exec_()
    except Exception as e:
        print("Error 발생! ㅠㅠ : ", e)
    else:
        print("-"*10,"잘가요", "-"*10)
