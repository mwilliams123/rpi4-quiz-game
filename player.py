from gpiozero import Button, LED, Device
from gpiozero.pins.mock import MockFactory
import threading
# if Device.pin_factory is None:
#     Device.pin_factory = MockFactory()
# actions required for each player
# 
# instance variables: score, eligible_to_ring, active, buzzer 
#  eligible = possible to ring in after Alex asks the question
#  active = have rung in first and now can answer the question
#  timer = time left to answer questin

# constructor takes in led pin number and buzzer pin number

class Player:
    def __init__(self, ledPin,buzzerPin, number, manager):
       self.led = LED(ledPin)
       self.active = False
       self.eligible = False
       self.score = 0
       self.buzzer = Button(buzzerPin)
       self.timer = 5000
       self.playerAnswer = ""
       self.buzzer.when_pressed = self.buzz_in
       self.number = number
       self.manager = manager
       self.locked_out = False
       
# 
# have buzzed in so are active with light on
    def buzz_in(self):
        if self.eligible and not self.locked_out:
           self.active = True
           self.led.on()
           self.manager.ring_in(self.number)
           self.timer = 5000
        elif not self.locked_out:
            self.locked_out = True
            t = threading.Timer(0.25, self.unlock)
            t.start()
  
    def unlock(self):
        print("unlock " + str(self.number))
        self.locked_out = False
# answer_question ()
# determine if gave correct answer and update score

    def answer_question (self, correct, value):
       if correct:
           self.update_score(value)
       else:
           self.update_score(-value)
        
       self.active = False
       self.led.off()
       self.eligible = False
       self.timer = 5000

    def update_score (self, newScore):
        self.score += newScore
        
        
    def update_timer(self, elapsedTime):
         self.timer -= elapsedTime
    

    
    


