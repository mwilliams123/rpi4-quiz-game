from constants import Colors, GameState
import pygame

def draw_answer(screen, store, pm, mouse_click):
    screen.fill(Colors.BLUE)
    text = store['clue']['question']
    blit_text(screen, text)
    w, h = pygame.display.get_surface().get_size()
     # draw start button
    font = pygame.font.SysFont("arial", 40)
    text = font.render('Correct', True, Colors.WHITE)
    text_rect = text.get_rect(center=(w*1/4, h*3/4))
    screen.blit(text,text_rect)

    # determine if start button clicked
    if mouse_click and text_rect.collidepoint(pygame.mouse.get_pos()):
        pm.update(True, store['clue']['value'])
        return GameState.BOARD
    
     # draw start button
    font = pygame.font.SysFont("arial", 40)
    text = font.render('Incorrect', True, Colors.WHITE)
    text_rect = text.get_rect(center=(w*3/4, h*3/4))
    screen.blit(text,text_rect)

    # determine if start button clicked
    if mouse_click and text_rect.collidepoint(pygame.mouse.get_pos()):
        pm.update(False,store['clue']['value'])
        return GameState.BOARD
    return GameState.ANSWER

def draw_question(screen, store):
    screen.fill(Colors.BLUE)
    text = store['clue']['answer']
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
