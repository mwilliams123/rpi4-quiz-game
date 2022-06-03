"""
Utility functions and classes
"""
from io import BytesIO
import pygame
from pydub import AudioSegment
from pygame import mixer
from gtts import gTTS
from constants import Colors

class Font():
    """Fonts for rendered text.

    Attributes:
        DEFAULT (int): for simple text like 'loading', and button text like 'continue'
        CLUE (int): for drawing clue questions and answers
        NUMBER (int): for drawing clue values, score values, or large category text
        CATEGORY (int): for drawing category titles
        """
    DEFAULT = 0
    CLUE = 1
    NUMBER = 2
    CATEGORY = 3
    _fonts = {}
    @classmethod
    def load_fonts(cls):
        """Loads fonts to be used in game."""
        cls._fonts[cls.DEFAULT] = pygame.font.SysFont("arial", 40)
        cls._fonts[cls.CLUE]= pygame.font.Font('fonts/Caudex-Bold.ttf', 60)
        cls._fonts[cls.NUMBER] = pygame.font.Font('fonts/Anton-Regular.ttf', 60)
        cls._fonts[cls.CATEGORY] = pygame.font.Font('fonts/Anton-Regular.ttf', 24)

    @classmethod
    def get_font(cls, font):
        """Returns requested font, raises an error if font does not exist.

        Args:
            font (int): Enum that specifies font. Can be DEFAULT, CLUE, NUMBERR, or CATEGORY.

        Raises:
            NotFoundErr: If font has not been loaded yet.

        """
        if font in cls._fonts:
            return cls._fonts[font]

        raise FileNotFoundError('That font has not been loaded. Please try load_fonts() first.')

    @classmethod
    @property
    def clue(cls):
        """Getter for clue font."""
        return cls.get_font(cls.CLUE)

    @classmethod
    @property
    def button(cls):
        """Getter for button font."""
        return cls.get_font(cls.DEFAULT)

    @classmethod
    @property
    def category(cls):
        """Getter for category font."""
        return cls.get_font(cls.CATEGORY)

    @classmethod
    @property
    def number(cls):
        """Getter for number font."""
        return cls.get_font(cls.NUMBER)

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
        self.text = Font.button.render(text, True, Colors.WHITE)
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

    def set_text(self, text):
        self.text = Font.button.render(text, True, Colors.WHITE)

def display_text(screen, text, font, rect):
    """Displays text with shadow.

    Args:
        screen (Surface): Pygame surface where game will be drawn
        text (str): The words to be drawn
        font (Font): Pygame Font to render the text in
        rect (int, int, int, int): Bounds (left, top, right, bottom) of the rectangle to draw
            the text within. Bounds are pixel values relative to screen.
    """
    offset = 2
    draw_text(screen, text, font, (rect[0]+offset, rect[1]+offset, rect[2]+offset, rect[3]+offset), Colors.BLACK)
    draw_text(screen, text, font, rect, Colors.WHITE)

def draw_text(screen, text, font, rect, color):
    """Draws multiline text centered horizontally and vertically within a rectangle.

    Args:
        screen (Surface): Pygame surface where game will be drawn
        text (str): The words to be drawn
        font (Font): Pygame Font to render the text in
        rect (int, int, int, int): Bounds (left, top, right, bottom) of the rectangle to draw
            the text within. Bounds are pixel values relative to screen.
    """
    words = text.split(' ') # list of words
    rects = [] # list of rectangles, where each box contains one line
    height = 0 # total height of all lines
    i = 0
    while i < len(words):
        # Add word to new line
        line = words[i]
        line_width, line_height = font.size(words[i])
        i += 1
        while i < len(words):
            # keep adding words to line until it would exceed max width
            word_len = font.size(words[i] + ' ')[0]
            if word_len + line_width > rect[2] - rect[0]:
                break
            line += ' ' + words[i]
            line_width += word_len
            i += 1
        # render line to a rectangular surface
        rects.append(font.render(line, True, color))
        height += line_height

    # draw text rectangles
    y_pos = (rect[1] + rect[3])/2 - height/2 + line_height/2 # center vertically
    x_pos = (rect[0] + rect[2]) // 2 # center horizontally
    for text_rect in rects:
        screen.blit(text_rect, text_rect.get_rect(center=(x_pos, y_pos)))
        y_pos += line_height


class TTS():
    """Class for implementing Text to Speech."""
    channel = None

    @classmethod
    def prepare_speech(cls, text):
        """Prepares text to be read aloud. 

        Args:
            text (string): raw text from clue database 

        Returns:
            string: cleaned text
        """
        return text.replace('____', ' blank ')

    @classmethod
    def play_speech(cls, text):
        """Uses google TTS to read given text aloud.

        Args:
            text (str): Words to be read aloud
        """
        # generate sound file
        tts = gTTS(cls.prepare_speech(text))
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
