from threading import *
from socket import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QObject


class Signal(QObject):
    recv_signal = pyqtSignal(str)
    disconnect_signal = pyqtSignal()

class ClientSocket():
    """
    부모 클래스 윈도우 에서 버튼을 클릭하면, 데이터를 받아와 소켓 통신을 실행하는 클래스
    client_ui.py 파일의 client_window 클래스 실행 시 호출된다.
    :__init__: 부모클래스인 ui, 데이터 수신 시그널, 연결 끊김 시그널 선언
    """

    def __init__(self, parent): # 라인 생성자 함수
        self.parent = parent    # 부모 윈도우 저장할 self.parent 변수 선언
        self.bConnect = False
        self.recv = Signal()    # 데이터 수신 시그널 선언
        self.recv.recv_signal.connect(self.parent.updateMsg)
        self.disconnect = Signal()   # 연결 끊길 때 사용할 시그널 선언
        self.disconnect.disconnect_signal.connect(self.parent.updateDisconnect)

    def __del__(self):
        self.stop()

    def connectServer(self, ip, port): # 접속 버튼 눌렀을 때 호출되는 함수. 소켓 생성, 해당 IP 주소의 포트 번호로 연결 시도
        self.client = socket(AF_INET, SOCK_STREAM)

        try:
            self.client.connect((ip, port))    #

        except Exception as e:
            print('Connect Error : ', e)
            return False

        else:
            self.bConnect = True
            self.thread = Thread(target=self.receive, args=(self.client,))
            self.thread.start()
            print("Connected")

        return True

    def stop(self):    # 소켓 닫고 부모 클래스에 알리는 함수
        self.bConnect = False
        if hasattr(self, 'client'):
            del(self.client)
            print('Client Stop')
            self.disconnect.disconnect_signal.emit()

    def receive(self, client):   # 클라이언트 소켓 연결이 정상적으로 이루어지면 생성되는 쓰레드에 의해 호출되는 함수
        """
        무한루프 통해 소켓의 데이터 수신하기 위해 대기하는 코드.
        반드시 쓰레드로 구성되어야 하며,
        또 다른 데이터가 언제 수신될 지 모르기 때문에 무한 루프로 구성해 계속 대기할 수 있어야 한다.
        :param client:  쓰레드에서 받는 클라이언트 소켓
        :return:
        """
        while self.bConnect:
            try:
                recv = client.recv(1024)
            except Exception as e:
                print("Recv Error : ", e)
                break
            else:
                msg = str(recv, encoding='utf-8')
                if msg:
                    self.recv.recv_signal.emit(msg)
                    print('[RECV] : ', msg)
        self.stop()

    def send(self, msg):
        """
        부모클래스 윈도우의 보내기 버튼을 누르면 호출되는 함수
        보낼 메시지 내용 복사해 연결된 소켓으로 전송하는 역할을 담당한다.
        :param mag:  복사된 메시지. 바이너리 데이터로 부호화해서 연결된 소켓으로 전송된다.
        :return:
        """
        if not self.bConnect:
            return
        try:
            self.client.send(msg.encode())

        except Exception as e:
            print('Send Error : ', e)


