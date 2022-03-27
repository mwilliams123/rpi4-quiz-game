"""
Main Game Loop
"""
import pygame
from board import Board
from categories import IntroScreen
from daily_double import DailyDouble
from final import Final
from game import Game
from constants import GameState
from loading import LoadingScreen
from question import Question
from title import TitleScreen
from util import Fonts, SoundEffects

def main():
    pygame.init()
    SoundEffects.load_sounds()
    Fonts.load_fonts()
    screen = pygame.display.set_mode((1300,700))
    game = Game(screen, {
        GameState.TITLE: TitleScreen(),
        GameState.LOADING: LoadingScreen(),
        GameState.INTRO: IntroScreen(),
        GameState.BOARD: Board(),
        GameState.QUESTION: Question(),
        GameState.DAILY_DOUBLE: DailyDouble(),
        GameState.FINAL: Final(),
    })
    game.run()
    pygame.quit()


if __name__ == "__main__":
    main()
