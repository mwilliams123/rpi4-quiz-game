import socket
import select

class Server():
    """Class for managing communication with Host when game is run in hosted mode.
    """
    def __init__(self, port=8060):
        # get LAN address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        lan = s.getsockname()[0]
        s.close()
        print(lan)

        # start server
        print("Starting host server...")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((lan, port))
        self.server.listen(1)
        self.client_poller = select.poll()
        self.client_poller.register(self.server, select.POLLIN)
        self.client = None
        self.poller = select.poll()
        self.wait = False

    def send(self, msg):
        self.client.send(msg.encode())

    def poll_for_connection(self):
        events = self.client_poller.poll(10)
        if len(events) > 0:
            client, _ = self.server.accept()
            print("Connected to host")
            self.client = client
            self.poller.register(client, select.POLLIN)

    def is_connected(self):
        return self.client is not None

    def poll(self):
        events = self.poller.poll(10)
        if len(events) > 0:
            resp = self.client.recv(512).decode()
            self.wait = False
            return resp
        return False

    def close(self):
        self.server.close()
