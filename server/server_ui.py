import sys, signal, socketio
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QListWidgetItem, QLineEdit, QListWidget
from PyQt5.QtGui import QIcon
import server

ui = uic.loadUiType("server_window.ui")[0]  # PyQt designer로 작성한 ui 파일 불러오기

class server_window(QWidget, ui):
    """
    부모 윈도우 에서 버튼을 클릭하면, 데이터를 받아와 소켓 통신을 실행하는 클래스
    client_ui.py 파일의 client_window 클래스 실행 시 호출된다.
    :__init__:  불러온 ui 파일 바탕으로 윈도우 생성
                server.py 파일의 ServerSocket 클래스 호출, ServerSocket의 객체를 self.server_socket이라는 이름으로 생성한다.
                designer 파일에서 작성한 connect_btn에 setCheckable() 함수를 사용해 True로 설정하여, 버튼을 누른 상태와 그렇지 않은 상태를 구분
                디자인 수정 추가
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.server_socket = server.ServerSocket(self)
        self.connect_btn.setCheckable(True)
        self.guest.setColumnWidth(0, 169)
        self.guest.setColumnWidth(1, 169)


    def toggle_btn(self, state):    # ip, port 번호 받고, 통신이 시작했을 때는 버튼에 종료, 통신을 끊었을 때는 버튼에 연결이라는 텍스트를 띄우는 함수
                                    # 서버 실행시, ip와 port번호를 ServerSocket클래스로 전달해 리슨 소켓 생성, 실행.
                                    # 종료시, 서버 소켓 클래스의 close()함수 호출해 서버 소켓 닫는 동작 수행
        if state:
            ip = self.input_ip.text()
            port = self.input_port.text()
            if self.server_socket.start(ip, port):
                self.connect_btn.setText("종료")
            else:
                self.server_socket.stop()
                self.msg_list.clear()
                self.connect_btn.setText("연결")
        else:
            self.server_socket.stop()
            self.msg_list.clear()
            self.connect_btn.setText("연결")


    def update_client(self, addr, isConnect=False):     # 접속한 클라이언트를 표에 띄우는 함수
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

    def update_msg(self, msg):
        self.msg_list.addItem(QListWidgetItem(msg))
        self.msg_list.setCurrentRow(self.msg_list.count() - 1)

    def sendMsg(self):  # 보낼 메시지에 글을 적고 보내기 버튼 눌렀을 때, 입력한 내용을 ServerSocket으로 전달해 모든 클라이언트에게 메시지 송신하는 역할과 연결된다
        if not self.server_socket.bListen:
            self.send_msg.clear()
            return

        send_msg = self.send_msg.text()
        self.update_msg(send_msg)
        self.server_socket.send(send_msg)
        self.send_msg.clear()
        self.send_msg.setFocus()


    def clearMsg(self):
        self.msg_list.clear()

    def closeEvent(self, e):
        try:
            self.server_socket.stop()
        except TypeError:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_window = server_window()
    chat_window.setWindowTitle('oss talk')
    chat_window.setWindowIcon(QIcon('teddy-bear.png'))
    chat_window.show()
    try:
        app.exec_()
    except Exception as e:
        print("Error 발생! ㅠㅠ : ", e)
    else:
        print("-"*10,"잘가요", "-"*10)
