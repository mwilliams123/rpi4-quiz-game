from constants import Colors
import pygame

def draw_score(screen, rect, font, score, i):
    text = font.render('$' + str(score), True, Colors.WHITE)
    text_rect = text.get_rect(center=((rect[0] + rect[2])/2, rect[1] + rect[3]*3/4))
    screen.blit(text,text_rect)

    text = font.render('Player ' + str(i), True, Colors.WHITE)
    text_rect = text.get_rect(center=((rect[0] + rect[2])/2, rect[1] + rect[3]/4))
    screen.blit(text,text_rect)


def display_score(screen, store, pm):
    width, height = screen.get_size()
    height = height / 3
    screen.fill(Colors.BLUE)
    font = store['fonts']['number']
    for i,p in enumerate(pm.players):
        rect = (0, i*height, width, height) # left top right bottom
        draw_score(screen, rect, font, p.score, i+1)
        pygame.draw.rect(screen, Colors.BLACK, rect, 5)
    