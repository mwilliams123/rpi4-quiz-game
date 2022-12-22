"""
Server class for game to interface with host screen.
"""
import socket
import select
from host.socket_util import get_lan

class Server():
    """Class for managing communication with Host when game is run in hosted mode."""
    def __init__(self, port=8081):
        lan = get_lan()
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
        """Send message to host."""
        self.client.send(msg.encode())

    def poll_for_connection(self):
        """Receive connection from host."""
        events = self.client_poller.poll(10)
        if len(events) > 0:
            client, _ = self.server.accept()
            print("Connected to host")
            self.client = client
            self.poller.register(client, select.POLLIN)

    def is_connected(self):
        """Returns whether host is connected."""
        return self.client is not None

    def poll(self):
        """Wait for response from host."""
        events = self.poller.poll(10)
        if len(events) > 0:
            resp = self.client.recv(512).decode()
            self.wait = False
            return resp
        return False

    def close(self):
        """Close connection with host."""
        self.server.close()
