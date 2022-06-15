"""Entrypoint for launching RPI Quiz Game.

  Usage Example:
    $ python main.py
"""
import pygame
from board import Board
from categories import IntroScreen
from daily_double import DailyDouble
from final import Final
from game import Game
from constants import GameState
from hall_of_fame import Hall
from loading import LoadingScreen
from question import Question
from tie_breaker import TieBreaker
from title import TitleScreen
from util import Font, SoundEffects

def main():
    """Initializes pygame display, loads resources, & launches game."""
    pygame.init()
    SoundEffects.load_sounds()
    Font.load_fonts()
    screen = pygame.display.set_mode((1300,700))
    game = Game(screen, {
        GameState.TITLE: TitleScreen(),
        GameState.LOADING: LoadingScreen(),
        GameState.INTRO: IntroScreen(),
        GameState.BOARD: Board(),
        GameState.QUESTION: Question(),
        GameState.DAILY_DOUBLE: DailyDouble(),
        GameState.FINAL: Final(),
        GameState.HALL: Hall(),
        GameState.TIE: TieBreaker(),
    })
    game.run()
    pygame.quit()


if __name__ == "__main__":
    main()
