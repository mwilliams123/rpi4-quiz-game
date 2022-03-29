"""
Utility functions and classes
"""
from io import BytesIO
import pygame
from pydub import AudioSegment
from pygame import mixer
from gtts import gTTS
from constants import Colors

class Fonts():
    """Fonts for rendered text.

    Attributes:
        BUTTON (Font): for simple text like 'loading', and button text like 'continue'
        CLUE (Font): for drawing clue questions and answers
        NUMBER (Font): for drawing clue values, score values, or large category text
        CATEGORY (Font): for drawing category titles
        """
    @classmethod
    def load_fonts(cls):
        """Loads fonts to be used in game."""
        cls.BUTTON = pygame.font.SysFont("arial", 40)
        cls.CLUE = pygame.font.Font('fonts/Caudex-Bold.ttf', 60)
        cls.NUMBER = pygame.font.Font('fonts/Anton-Regular.ttf', 60)
        cls.CATEGORY = pygame.font.Font('fonts/Anton-Regular.ttf', 24)

class SoundEffects():
    """Sound effects

    Attributes:
        daily_double_sound (Sound): played when daily double is found
        time_sound (Sound): double beep when time is up
        final_sound (Sound): theme played during final question
        """
    @classmethod
    def load_sounds(cls):
        """Initializes sound module and loads sound effects."""
        mixer.init()
        cls.daily_double_sound = mixer.Sound("sounds/Jeopardy-daily2x.wav")
        cls.time_sound = mixer.Sound("sounds/Times-up.wav")
        cls.final_sound = mixer.Sound("sounds/Final-Music.wav")

    @classmethod
    def is_busy(cls):
        """Returns true if a sound is currently playing, false otherwise."""
        return pygame.mixer.Channel(0).get_busy()
    @classmethod
    def play(cls, type_):
        """Plays a sound effect (non-blocking)

        Args:
            type_ (int): Which sound to play
        """
        if type_ == 1:
            cls.time_sound.play()
        elif type_ == 2:
            cls.daily_double_sound.play()
        else:
            cls.final_sound.play()

class Button():
    """Representation of a UI button that can be clicked on.

    Attributes:
        text (Surface): Pygame surface with button's text rendered on it
        rect: (Rectangle): Rectangle that the button is contained within
    """
    def __init__(self, text):
        """Initializes button Object

        Args:
            text (str): Text that goes on button
        """
        self.text = Fonts.BUTTON.render(text, True, Colors.WHITE)
        self.rect = None

    def was_clicked(self):
        """Returns true if mouse is hovering over button, false otherwise."""
        return self.rect is not None and self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, screen, pos):
        """Draws button to pygame display.

        Args:
            screen (Surface): Pygame display where game will be drawn
            pos (int, int): Pixel value (row, column) where button should be centered
        """
        self.rect = self.text.get_rect(center=pos)
        screen.blit(self.text, self.rect)

def draw_text(screen, text, font, rect):
    """Draws multiline text centered horizontally and vertically within a rectangle.

    Args:
        screen (Surface): Pygame surface where game will be drawn
        text (str): The words to be drawn
        font (Font): Pygame Font to render the text in
        rect (int, int, int, int): Bounds (left, top, right, bottom) of the rectangle to draw
            the text within. Bounds are pixel values relative to screen.
    """
    words = text.split(' ') # list of words
    space = font.size(' ')[0]  # The width of a space
    max_width = rect[2] - rect[0]
    rects = [] # list of rectangles, where each box rectangles one line
    height = 0 # total height of all lines
    i = 0
    while i < len(words):
        # Add word to new line
        line = words[i]
        line_width, line_height = font.size(words[i])
        i += 1
        while i < len(words):
            # keep adding words to line until it would exceed max width
            word_len = font.size(words[i])[0]
            if word_len + space + line_width > max_width:
                break
            line += ' ' + words[i]
            line_width += word_len + space
            i += 1
        # render line to a rectangular surface
        text_rect = font.render(line, True, Colors.WHITE)
        height += line_height
        rects.append(text_rect)

    # draw text rectangles
    y_pos = (rect[1] + rect[3])/2 - height/2 + line_height/2 # center vertically
    x_pos = (rect[0] + rect[2]) // 2 # center horizontally
    for rect in rects:
        text_rect = rect.get_rect(center=(x_pos, y_pos))
        y_pos += line_height
        screen.blit(rect, text_rect)


class TTS():
    """Class for implementing Text to Speech."""
    channel = None

    @classmethod
    def play_speech(cls, text):
        """Uses google TTS to read given text aloud.

        Args:
            text (str): Words to be read aloud
        """
        # generate sound file
        tts = gTTS(text)
        # save sound output in buffer
        bytes_stream = BytesIO()
        tts.write_to_fp(bytes_stream)
        bytes_stream.seek(0) # roll back buffer stream to beginning of file
        # convert mp3 to wav format
        sound = AudioSegment.from_file(bytes_stream)
        wav = sound.export(bytes_stream, format='wav')
        # play sound
        sound = mixer.Sound(wav)
        cls.channel = sound.play()

    @classmethod
    def is_busy(cls):
        """Returns true if sound is currently play, otherwise returns false."""
        return cls.channel and cls.channel.get_busy()
