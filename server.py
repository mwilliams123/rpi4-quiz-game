import socket
import select

class Server():
    """Class for managing communication with Host when game is run in hosted mode.
    """
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
        client, _ = self.server.accept()
        self.client = client
        self.poller = select.poll()
        self.poller.register(client, select.POLLIN)
        self.wait = False

    def send(self, msg):
        self.client.send(msg.encode())

    def poll(self):
        events = self.poller.poll(10)
        if len(events) > 0:
            resp = self.client.recv(512).decode()
            self.wait = False
            return resp
        return False

    def close(self):
        self.server.close()
