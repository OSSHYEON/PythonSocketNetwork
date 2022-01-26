import socket
from threading import Thread
from socket import *
from PyQt5.QtCore import Qt, pyqtSignal, QObject

class ServerSocket(QObject):
    update_signal = pyqtSignal(tuple, bool)
    recv_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.bListen = False
        self.clients = []
        self.ip = []
        self.threads = []
        self.server = None
        self.update_signal.connect(self.parent.update_client)
        self.recv_signal.connect(self.parent.update_msg)


    def start(self, ip, port):
        print("start", ip, port)
        self.server = socket(AF_INET, SOCK_STREAM)  # IPv4 방식, 소켓 self.server에 담아서 전달
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

    def stop(self):
        self.bListen = False
        try:
            if hasattr(self, 'server'):
                self.server.close()
                print('Server Stop')
                print('잠시만 기다려주세요! 서버가 닫힐 때까지 시간이 다소 소요됩니다...')
        except AttributeError:
            pass


    def listen(self, server):
        while self.bListen:
            server.listen(5)
            try:
                client, addr = server.accept()

            except Exception as e:
                print('Accept Error : ', e)
                break

            else:
                self.clients.append(client)
                self.ip.append(addr)
                self.update_signal.emit(addr, True)
                t= Thread(target=self.receive, args=(addr, client))
                self.threads.append(t)
                t.start()

    def receive(self, addr, client):
        while True:
            try:
                recv = client.recv(1024) # 1024 바이트 크기의 소켓 받음

            except Exception as e:
                print('Recv Error : ', e)
                break

            else:
                msg = str(recv, encoding='utf-8')
                if msg:
                    self.send(msg)
                    self.recv_signal.emit(msg)
                    print('[RECV]:', addr, msg)


    def send(self, msg):
        try:
            print(len(self.clients))
            for client in self.clients:
                client.send(msg.encode())

        except Exception as e:
            print('Send Error : ', e)

