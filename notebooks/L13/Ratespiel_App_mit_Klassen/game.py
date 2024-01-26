import random
sign = lambda x:(x > 0) - (x < 0)

class Game:
    def __init__(self):
        self.range = (1, 10)
        self.number_to_guess = None
        self.guesses_with_feedback =  []
        self.game_on = False
        self._callbacks = []
        
    def new_game(self):
        '''starte ein neues Spiel'''
        self.guesses_with_feedback.clear()
        self.number_to_guess = random.randint(*self.range)
        self.game_on = True
        self._notify('new_game', self)  
        
    def guess(self, zahl):
        '''behandle Rateversuch'''
        if self.game_on:
            feedback = sign(zahl - self.number_to_guess)
            if feedback == 0:
                self.game_on = False
            self.guesses_with_feedback.append((zahl, feedback))
            self._notify('guess', self)  
            
    def register_callback(self, callback):
        if callback not in self._callbacks:
            self._callbacks.append(callback)      
            
    def _notify(self, event, data):
        for f in self._callbacks:
            f(event, data)     
            
    def __repr__(self):
        return 'Game on: {}, Range: {}, Versuche: {}'.\
              format(self.game_on, self.range, self.guesses_with_feedback)
