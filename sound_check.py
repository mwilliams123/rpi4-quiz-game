"""
Check that audio output is configured correctly.
"""
from util import TTS, SoundEffects
import time
SoundEffects.load_sounds()
TTS.play_speech(' This is a test')
time.sleep(2)
