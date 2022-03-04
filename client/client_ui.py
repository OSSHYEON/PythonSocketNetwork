import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem
from PyQt5.QtGui import QIcon
import client


ui = uic.loadUiType("client_ui.ui")[0] # PyQt designer로 작성한 ui 파일 불러오기

class client_window(QWidget, ui):
    """
    QWidget 으로부터 상속 받아 위젯 만드는 클래스. 불러온 ui 파일 바탕으로 위젯을 생성한다.
    :__init__:  client.py에서 작성한 ClientSocket 클래스를 호출하며, ClientSocket의 객체를 self.client_socket 이라는 이름으로 생성한다.
                designer 파일에서 작성한 connect_btn에 setCheckable() 함수를 사용해 True로 설정하여, 버튼을 누른 상태와 그렇지 않은 상태를 구분해준다.
    """
    def __init__(self):
        super().__init__()  # QWidget 으로부터 상속
        self.setupUi(self)  # 불러온 ui 파일 바탕으로 위젯 생성
        self.client_socket = client.ClientSocket(self) # client.py에서 작성한 ClientSocket 클래스 호출, ClientSocket의 객체를 self.client_socket이라는 이름으로 생성
        self.connect_btn.setCheckable(True)  # setCheckable(True) 설정 시, 버튼 누른 상태와 누르지 않은 상태 구분
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

    def updateMsg(self, msg): # 보낼 메시지에 작성한 내용을 소켓 클래스로 전달해 데이터 송신하는 역할
        self.connect_btn.setText('접속')
        self.recv_msg.addItem(QListWidgetItem(msg))

    def updateDisconnect(self): # 소켓 연결 끊어진 경우 호출되는 함수
        self.btn.setText('접속') # 다시 접속 버튼 누를 수 있도록 setText() 함수 사용해 버튼 내 텍스트 수정

    def sendMsg(self):
        send_msg = self.send_msg.toPlainText()
        self.client_socket.send(send_msg)
        self.send_msg.clear()

    def clearMsg(self): # 수신 받은 전체 메시지 삭제
        self.recv_msg.clear()

    def closeEvent(self, e):
        self.client_socket.stop()


if __name__ == "__main__":  # main 함수로 윈도우 창 생성하고 프로그램 생성
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
