"""
Utility functions for socket connections.
"""
import socket

def get_lan():
    """Return name of LAN."""
    # get LAN address
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    lan = sock.getsockname()[0]
    sock.close()
    return lan
