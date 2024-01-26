from ipywidgets import IntSlider

class Controller:
    def __init__(self, game):
        self.game = game
        self.widget = IntSlider(value = 0,
                                min = 0,
                                max = game.range[1],
                                description = 'Your guess:',
                                continuous_update = False,
                               )
        self.widget.observe(self.submit_guess, names = 'value') 
        
    def submit_guess(self, change):
        zahl = change.new
        if zahl == 0:
            self.game.new_game() 
        else: 
            self.game.guess(zahl) 
            
    def _ipython_display_(self):
        display(self.widget)
