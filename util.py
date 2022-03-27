"""
Utility functions
"""
from io import BytesIO
import pygame
from pydub import AudioSegment
from pygame import mixer
from gtts import gTTS
from constants import Colors

class Fonts():
    """Fonts"""
    @classmethod
    def load_fonts(cls):
        cls.BUTTON = pygame.font.SysFont("arial", 40)
        cls.CLUE = pygame.font.Font('fonts/Caudex-Bold.ttf', 60)
        cls.NUMBER = pygame.font.Font('fonts/Anton-Regular.ttf', 60)
        cls.CATEGORY = pygame.font.Font('fonts/Anton-Regular.ttf', 24)

class SoundEffects():
    """Sound effects"""
    @classmethod
    def load_sounds(cls):
        mixer.init()
        cls.daily_double_sound = mixer.Sound("sounds/Jeopardy-daily2x.wav")
        cls.time_sound = mixer.Sound("sounds/Times-up.wav")
        cls.final_sound = mixer.Sound("sounds/Final-Music.wav")

    @classmethod
    def play(cls, type_):
        if type_ == 1:
            cls.time_sound.play()
        elif type_ == 2:
            cls.daily_double_sound.play()
        else:
            cls.final_sound.play()

class Button():
    def __init__(self, text) -> None:
        self.text = Fonts.BUTTON.render(text, True, Colors.WHITE)
        self.rect = None

    def was_clicked(self):
        return self.rect is not None and self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, screen, pos):
        self.rect = self.text.get_rect(center=pos)
        screen.blit(self.text, self.rect)

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
    y_pos = (rect[1] + rect[3])/2 - height/2 + line_height/2
    x_pos = (rect[0] + rect[2]) // 2
    for rect in rects:
        text_rect = rect.get_rect(center=(x_pos, y_pos))
        y_pos += line_height
        screen.blit(rect, text_rect)


class TTS():
    channel = None

    @classmethod
    def play_speech(cls, text):
        bytes_stream = BytesIO()
        tts = gTTS(text)
        tts.write_to_fp(bytes_stream)
        bytes_stream.seek(0)
        sound = AudioSegment.from_file(bytes_stream)
        wav = sound.export(bytes_stream, format='wav')
        sound = mixer.Sound(wav)
        cls.channel = sound.play()

    @classmethod
    def is_busy(cls):
        return cls.channel and cls.channel.get_busy()
