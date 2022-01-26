from threading import *
from socket import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QObject


class Signal(QObject):
    recv_signal = pyqtSignal(str)
    disconnect_signal = pyqtSignal()

class ClientSocket():

    def __init__(self, parent):
        self.parent = parent
        self.bConnect = False
        self.recv = Signal()
        self.recv.recv_signal.connect(self.parent.updateMsg)
        self.disconnect = Signal()
        self.disconnect.disconnect_signal.connect(self.parent.updateDisconnect)

    def __del__(self):
        self.stop()

    def connectServer(self, ip, port):
        self.client = socket(AF_INET, SOCK_STREAM)

        try:
            self.client.connect((ip, port))

        except Exception as e:
            print('Connect Error : ', e)
            return False

        else:
            self.bConnect = True
            self.thread = Thread(target=self.receive, args=(self.client,))
            self.thread.start()
            print("Connected")

        return True

    def stop(self):
        self.bConnect = False
        if hasattr(self, 'client'):
            del(self.client)
            print('Client Stop')
            self.disconnect.disconnect_signal.emit()

    def receive(self, client):
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
        if not self.bConnect:
            return
        try:
            self.client.send(msg.encode())

        except Exception as e:
            print('Send Error : ', e)


