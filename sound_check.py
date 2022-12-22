"""
Check that audio output is configured correctly.
"""
import time
from util.util import TTS, SoundEffects

SoundEffects.load_sounds()
TTS.play_speech(' This is a test')
time.sleep(2)
