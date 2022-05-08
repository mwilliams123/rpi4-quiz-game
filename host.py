"""Program for host to use when game to be run in hosted mode.
In hosted mode a human as the host can see answers and rule on responses.
"""
import socket
import select
import pygame
from host_screen import Host
from util import Font

def main():
    # get LAN address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    lan = s.getsockname()[0] #"192.168.1.31" 
    s.close()
    print(lan)

    pygame.init()
    Font.load_fonts()
    host = Host()
    host.startup()
    quit_pressed = False
    screen = pygame.display.set_mode((1300,700))
    # connect to server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((lan, 8080))
    poller = select.poll()
    poller.register(s, select.POLLIN)
    print("Connected to server")
    clock = pygame.time.Clock()
    text = ''
    while not quit_pressed:
        events = poller.poll(10)
        if len(events) > 0:
            msg = s.recv(512).decode()
            if msg == 'continue':
                host.timer_expired = True
            elif msg == 'rangin':
                host.rang_in = True
            else:
                text = msg
        quit_pressed = host.handle_event()
        if quit_pressed:
            break
        host.draw(screen, text)
        if host.update():
            # button was clicked, send back
            s.send(str(host.correct).encode())
            text = ''
            host.startup()
        # Display screen
        pygame.display.flip()
        clock.tick(40)

    s.close()


if __name__ == "__main__":
    main()
