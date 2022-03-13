import pygame
from constants import Colors

def load_fonts():
    fonts = {}
    fonts['number'] = pygame.font.Font('fonts/Anton-Regular.ttf', 60)
    fonts['category'] = pygame.font.Font('fonts/Anton-Regular.ttf',24)
    fonts['clue'] = pygame.font.Font('fonts/Caudex-Bold.ttf', 60)
    return fonts

def draw_text(screen, text, font, rect):
    # draw multiline text centered in rect (left, top, right, bottom)
    words = text.split(' ') # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width = rect[2] - rect[0]
    i = 0
    height = 0
    rects = []
    while i < len(words):
        line_width, line_height = font.size(words[i])
        line = words[i]
        i += 1
        while i  < len(words):
            word_len = font.size(words[i])[0]
            if word_len + space + line_width > max_width:
                break
            line += ' ' + words[i]
            line_width += word_len + space
            i += 1
        text_rect = font.render(line, True, Colors.WHITE)
        height += line_height
        rects.append(text_rect)
    y = (rect[1] + rect[3])/2 - height/2 + line_height/2
    x = (rect[0] + rect[2]) // 2
    for r in rects:
        c = r.get_rect(center=(x, y))
        y += line_height
        screen.blit(r, c)