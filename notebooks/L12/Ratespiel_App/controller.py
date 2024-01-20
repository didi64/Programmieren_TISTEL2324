import ratespiel
from ipywidgets import IntSlider

def submit_guess(change):
    zahl = change.new
    if zahl == 0:
        ratespiel.game_new() 
    else:    
        ratespiel.game_guess(zahl) 

kwargs = {'value': 0, 
          'min': 0, 
          'max': ratespiel.state['range'][1],
          'step': 1, 
          'description': 'Your guess:', 
          'continuous_update': False,
         }
slider = IntSlider(**kwargs)
slider.observe(submit_guess, names = 'value')      
