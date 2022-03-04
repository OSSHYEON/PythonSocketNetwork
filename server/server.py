import socket
from threading import Thread
from socket import *
from PyQt5.QtCore import pyqtSignal, QObject

class ServerSocket(QObject):
    """
    socket 을 멤버 변수로 갖는 네트워크 관련 클래스
    :__init__:  부모 위젯을 전달 받음.
                클라이언트 접속, 접속 종료, 메시지 수신 시 전송되는 사용자 정의 시그널에 부모 윈도우의 함수를 슬롯으로 등록해 클래스 간 신호를 전달하기 위함이다.
    """

    update_signal = pyqtSignal(tuple, bool)
    recv_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent    # 부모 위젯 저장하는 변수
        self.bListen = False    # 서버 소켓이 접속 대기(listen) 상태인지, 아닌지 저장하는 변수
        self.clients = []       # 접속한 클라이언트들 저장할 리스트
        self.ip = []            # 접속한 클라이언트들의 ip 저장할 리스트
        self.threads = []       # listen 및 클라이언트 접속 시 마다 생성되는 쓰레드 저장 리스트
        self.server = None
        self.update_signal.connect(self.parent.update_client)
        self.recv_signal.connect(self.parent.update_msg)

    def __del__(self):  # ServerSocket 클래스 파괴될 때 호출되는 소멸자. stop() 함수 호출해 서버 소켓을 종료한다.
        self.stop()


    def start(self, ip, port):
        """
        부모 위젯에서 서버 실행 버튼을 누르면 호출되는 함수.
        AF_INET 은 IPv4를, SOCKET_STREAM은 연결 지향형 소켓으로 만들어달라는 뜻이다.
        :param ip: 입력 받은 ip 주소
        :param port: 입력 받은 port 번호
        :return: try~except 문을 사용해, 만들어진 소켓 + ip + port 번호와 bind()하고 서버 소켓이 계속 listen 상태임(True) 임을 반환
        """
        print("start", ip, port)
        self.server = socket(AF_INET, SOCK_STREAM)  # IPv4 방식, 소켓을 self.server 변수에 담아서 전달. AF_INET = IPv4
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        try:
            self.server.bind((ip, int(port)))

        except Exception as e:
            print('Bind Error : ', e)
            return False

        else:
            self.bListen = True
            self.server_thread = Thread(target=self.listen, args=(self.server,))
            self.server_thread.start()
            print('Server Listening...')
        return True

    def stop(self): # 서버 소켓 닫는 함수
        self.bListen = False    # listen 상태 아님을 저장
        try:
            if hasattr(self, 'server'):
                self.server.close()
                print('Server Stop')
                print('잠시만 기다려주세요! 서버가 닫힐 때까지 시간이 다소 소요됩니다...')
        except AttributeError:
            pass


    def listen(self, server):
        """
        쓰레드에서 호출되는 함수. 생성된 서버 소켓을 접속 대기(listen) 상태로 만든 후 accept() 함수 호출
        accept(), 클라이언트가 접속할 때까지 무한 대기한다. 클라이언트가 접속한 경우 accept() 함수를 탈출한다.
        accept() 함수를 탈출하면서 클라이언트 소켓, IP 주소를 리스트 변수에 저장하고 부모 위젯에 접속 알리고, 클라이언트와 데이터 수신 위한 쓰레드를 생성한다.
        """
        while self.bListen:

            server.listen(5)
            try:
                client, addr = server.accept()

            except Exception as e:
                print('Accept Error : ', e)
                break

            else:   # accpet() 함수 탈출하고 client, ip 받아 시그널, 쓰레드 생성하는 부분
                self.clients.append(client)
                self.ip.append(addr)
                self.update_signal.emit(addr, True)
                t= Thread(target=self.receive, args=(addr, client))
                self.threads.append(t)
                t.start()

    def receive(self, addr, client):    # 클라이언트가 접속할 때마다 생성되는 쓰레드가 실행하는 함수
        # 서버와 클라이언트간 1:1 연결 이루어진 상태. recv()함수 호출해 블럭 상태로 진입한 후 클라이언트가 보내는 메시지 수신하기 위해 대기한다.
        while True:
            try:
                recv = client.recv(1024) # 1024 바이트 크기의 소켓 받음. 데이터를 수신하면 utf-8 문자열로 만들고 부모 위젯으로 전달 후 else문으로 넘어간다.

            except Exception as e:
                print('Recv Error : ', e)
                break

            else:   # send() 함수 호출해 연결된 모든 클라이언트에게도 broadcasting 하는 부분
                msg = str(recv, encoding='utf-8')
                if msg:
                    self.send(msg)
                    self.recv_signal.emit(msg)
                    print('[RECV]:', addr, msg)


    def send(self, msg):   # 클라이언트가 보낸 데이터 수신 시, 연결된 모든 클라이언트에게 해당 메시지 보내는 함수
        try:

            for client in self.clients:
                print(msg)
                client.send(msg.encode())

        except Exception as e:
            print('Send Error : ', e)

