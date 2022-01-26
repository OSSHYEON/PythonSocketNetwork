import sys, signal, socketio
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QListWidgetItem, QLineEdit, QListWidget
from PyQt5.QtGui import QIcon
import server

ui = uic.loadUiType("server_window.ui")[0]

class client_window(QWidget, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.server_socket = server.ServerSocket(self)
        self.connect_btn.setCheckable(True)
        self.guest.setColumnWidth(0, 169)
        self.guest.setColumnWidth(1, 169)



    def toggle_btn(self, state):
        if state:
            ip = self.input_ip.text()
            port = self.input_port.text()
            if self.server_socket.start(ip, port):
                self.connect_btn.setText("종료")
        else:
            pass

    def update_client(self, addr, isConnect=False):
        row = self.guest.rowCount()
        if isConnect:
            self.guest.setRowCount(row+1)
            self.guest.setItem(row, 0, QTableWidgetItem(addr[0]))
            self.guest.setItem(row, 1, QTableWidgetItem(str(addr[1])))

        else:
            for one_row in range(row):
                ip = self.guest.item(one_row, 0).text()
                port = self.guest.item(one_row, 1).text()
                if addr[0] == ip and str(addr[1]) == port:
                    self.guest.removeRow(one_row)
                    break

    def update_msg(self, msg_list):
        pass

    def sendMsg(self, msg):
        if not self.server_socket.bListen:
            self.send_msg.clear()
            return

        send_msg = self.send_msg.text()
        self.msg_list.addItem(QListWidgetItem(send_msg))
        self.msg_list.setCurrentRow(self.msg_list.count() - 1)
        self.send_msg.clear()
        self.send_msg.setFocus()


    def clearMsg(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_window = client_window()
    chat_window.setWindowTitle('osstalk')
    chat_window.setWindowIcon(QIcon('teddy-bear.png'))
    chat_window.show()
    app.exec_()
