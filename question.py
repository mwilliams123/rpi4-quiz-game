from constants import Colors
import pygame

def draw_question(screen, store):
    screen.fill(Colors.BLUE)
    text = store['clue']
    blit_text(screen, text)
def blit_text(screen, text, color=Colors.WHITE, font_size=60):
    font = pygame.font.SysFont("arial", font_size)
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = screen.get_size()
    max_width = max_width - 100
    pos = (100,100)
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            screen.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
