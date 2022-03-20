from constants import Colors
import pygame

def draw_score(screen, rect, font, score, i, timer, active):
    text = font.render('$' + str(score), True, Colors.WHITE)
    text_rect = text.get_rect(center=((rect[0] + rect[2])/2, rect[1] + rect[3]*2/3))
    screen.blit(text,text_rect)

    text = font.render('Player ' + str(i), True, Colors.WHITE)
    text_rect = text.get_rect(center=((rect[0] + rect[2])/2, rect[1] + rect[3]/4))
    screen.blit(text,text_rect)

    little_rect_width = rect[2]/9
    for i in range(9):
        color = Colors.BLACK
        if active:
            color = Colors.RED
            if (i < 5 and 4 - timer / 1000 > i) or (i >= 5 and timer / 1000 +4 < i):
                color = Colors.BLACK
        #pygame.draw.rect(screen, Colors.WHITE, (5, i*height+5, width-10, height-10), 10)
        pygame.draw.rect(screen, color, (rect[0] + little_rect_width*i,rect[1]-10 + rect[3] - 20, little_rect_width, 20))
        pygame.draw.rect(screen,Colors.WHITE,(rect[0] + little_rect_width*i,rect[1]-10 + rect[3] - 20, little_rect_width, 20), 2)



def display_score(screen, store, pm):
    width, height = screen.get_size()
    height = height / 3
    screen.fill(Colors.BLUE)
    font = store['fonts']['number']
    for i,p in enumerate(pm.players):
        rect = (0, i*height, width, height) # left top right bottom
        draw_score(screen, rect, font, p.score, i+1, p.timer, p.active)
        if p.active:
            pygame.draw.rect(screen, Colors.WHITE, (5, i*height+5, width-10, height-10), 10)
        pygame.draw.rect(screen, Colors.BLACK, rect, 5)
    