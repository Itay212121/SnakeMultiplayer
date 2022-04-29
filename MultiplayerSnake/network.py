"10.0.0.1"

import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 6003
        self.server = "10.0.0.14"

        self.addr = (self.server, self.port)
        self.connect()

    def get(self):
        return self.client.recv(8192)

    def connect(self):
        self.client.connect(self.addr)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(8192))
        except socket.error as e:
            print(e)
