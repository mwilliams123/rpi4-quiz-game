from gpiozero import Button, LED
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
       
       
# 
# have buzzed in so are active with light on
    def buzz_in(self):
  
       if (self.eligible):
           self.active = True
           self.led.on()
           self.manager.ring_in(self.number)
           
  

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
        print("Player " + str(self.number) + " score: " + str(self.score))
        
        
    def update_timer(self, elapsedTime):
         self.timer -= elapsedTime
    

    
    


