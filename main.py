"""Entrypoint for launching RPI Quiz Game.

  Usage Example:
    $ python main.py
"""
import pygame
from game import Game
from states.board import Board
from states.categories import IntroScreen
from states.daily_double import DailyDouble
from states.final import Final
from states.hall_of_fame import Hall
from states.loading import LoadingScreen
from states.options import OptionsScreen
from states.question import Question
from states.stats import Stats
from states.tie_breaker import TieBreaker
from states.title import TitleScreen
from util.util import Font, SoundEffects
from util.constants import GameState

def main():
    """Initializes pygame display, loads resources, & launches game."""
    pygame.init()
    SoundEffects.load_sounds()
    Font.load_fonts()
    screen = pygame.display.set_mode((1600,1000))
    game = Game(screen, {
        GameState.TITLE: TitleScreen(),
        GameState.OPTIONS: OptionsScreen(),
        GameState.LOADING: LoadingScreen(),
        GameState.INTRO: IntroScreen(),
        GameState.BOARD: Board(),
        GameState.QUESTION: Question(),
        GameState.DAILY_DOUBLE: DailyDouble(),
        GameState.FINAL: Final(),
        GameState.HALL: Hall(),
        GameState.TIE: TieBreaker(),
        GameState.STATS: Stats()
    })
    game.run()
    pygame.quit()


if __name__ == "__main__":
    main()
