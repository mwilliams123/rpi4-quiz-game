"""Program for host to use when game to be run in hosted mode.
In hosted mode a human as the host can see answers and rule on responses.
"""
import socket
import select
import time
import pygame
from host.screen import Host
from host.socket_util import get_lan
from util.util import Font

def main():
    """Launch host program."""
    pygame.init()
    Font.load_fonts()
    host = Host()
    host.startup()
    lan = get_lan()
    quit_pressed = False
    screen = pygame.display.set_mode((1300,700))
    while True:
        try:
            print("Trying to connect...")
            # connect to server
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((lan, 8080))
            break
        except ConnectionRefusedError:
            time.sleep(1)

    poller = select.poll()
    poller.register(sock, select.POLLIN)
    print("Connected to server")
    clock = pygame.time.Clock()
    text = ''
    while not quit_pressed:
        events = poller.poll(10)
        if len(events) > 0:
            msg = sock.recv(512).decode()
            print(msg)
            if msg == 'continue':
                host.timer_expired = True
            elif msg == 'rangin':
                host.rang_in = True
            elif len(msg) > 8:
                text = msg[8:]
        quit_pressed = host.handle_event()
        if quit_pressed:
            break
        host.draw(screen, text)
        if host.update():
            # button was clicked, send back
            sock.send(str(host.correct).encode())
            if host.correct or host.timer_expired:
                # reset
                host.startup()
                text = ''
        # Display screen
        pygame.display.flip()
        clock.tick(40)

    sock.close()


if __name__ == "__main__":
    main()
