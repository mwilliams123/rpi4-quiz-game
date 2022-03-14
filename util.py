import pygame
from constants import Colors
from pydub import AudioSegment
from pygame import mixer
from gtts import gTTS
from io import BytesIO
import time 

mixer.init()
def load_fonts():
    fonts = {}
    fonts['number'] = pygame.font.Font('fonts/Anton-Regular.ttf', 60)
    fonts['category'] = pygame.font.Font('fonts/Anton-Regular.ttf',24)
    fonts['clue'] = pygame.font.Font('fonts/Caudex-Bold.ttf', 60)
    return fonts

def draw_button(screen, text, pos):
    font = pygame.font.SysFont("arial", 40)
    text = font.render(text, True, Colors.WHITE)
    rect = text.get_rect(center=pos)
    screen.blit(text,rect)
    return rect

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

def play_speech(text):
    bytes_stream = BytesIO()
    tts = gTTS(text)
    tts.write_to_fp(bytes_stream)
    bytes_stream.seek(0)
    sound = AudioSegment.from_file(bytes_stream)
    #sound_fast = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate*1.5)})
    #sound_fast = sound.set_frame_rate(int(sound.frame_rate*0.8))
    wav = sound.export(bytes_stream, format='wav')
    sound = mixer.Sound(wav)
    channel = sound.play()

    # wait for sound to finish before exiting
    while channel.get_busy():
        time.sleep(0.1)