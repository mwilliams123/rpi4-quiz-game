from gpiozero import Button, LED
import time
# Player(19, 6, 0, self), Player(16, 21, 1, self), Player(12, 17, 2, self)
buzzer_pins = [6,21,17, 22, 26]
led_pins = [19, 16, 12, 27, 13]
buzzers = []

class Buzzer:
    def __init__(self, buzz_pin, led_pin) -> None:
        self.buzzer = Button(buzz_pin)
        self.led = LED(led_pin)
        self.buzzer.when_pressed = self.buzz_in

    def buzz_in(self):
        self.led.on()

for i in range(len(buzzer_pins)):
    buzz = Buzzer(buzzer_pins[i], led_pins[i])
    buzzers.append(buzz)

time.sleep(30)
