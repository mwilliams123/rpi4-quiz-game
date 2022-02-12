from gpiozero import Button, LED, RGBLED
from signal import pause
import random
import time

button = Button(6)
button2 = Button(21)
button3 = Button(17)                                                                                                                                                                                                       
led = LED(19)
led2 = LED(16)
led3 = LED(12)

led.off()
led2.off()
led3.off()

go = False
end = False
def one_wins():
    global end, go
    if go and not end:
        print("Player 1 wins!")
        led.on()
        end = True
    else:
        print("Player 1 loses")
    button.when_pressed = None
    button2.when_pressed = None
    button3.when_pressed = None
    
def two_wins():
     global end, go
     if go and not end:
        print("Player 2 wins!")
        led2.on()
        end = True
     else :
        print("Player 2 loses")
     button.when_pressed = None
     button2.when_pressed = None
     button3.when_pressed = None

def three_wins():
     global end, go
     if go and not end:
        print("Player 3 wins!")
        led3.on()
        end = True
     else :
        print("Player 3 loses")
     button.when_pressed = None
     button2.when_pressed = None
     button3.when_pressed = None

def ready():
    print("Ready player 1?")
    button.wait_for_press()
    print("Player 1 ready")

    print("Ready player 2?")
    button2.wait_for_press()
    print("Player 2 ready")

    print("Ready player 3?")

    button3.wait_for_press()
    print("Player 3 ready")
    
def green_light():
    global go
    stoplight = RGBLED(red=18, blue=24, green=23)
    stoplight.color = (0, 1, 0)
    go = True

    button.when_pressed = one_wins
    button2.when_pressed = two_wins
    button3.when_pressed = three_wins

