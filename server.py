import socket
import time
class Server():
    def __init__(self, port=8080):
        # get LAN address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        lan = s.getsockname()[0]
        s.close()

        # start server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((lan, port))
        self.server.listen(1)
        client, addr = self.server.accept()
        self.client = client

    def send(self, msg):
        print("sending")
        self.client.send(msg.encode())

    def close(self):
        self.server.close()

# test
print("starting server")
server = Server()
server.send('test')

time.sleep(60)
server.close()
