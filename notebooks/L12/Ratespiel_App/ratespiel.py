import random
sign = lambda x:(x > 0) - (x < 0)

# Gamestate
state = {'range': (1, 10),
         'number_to_guess': None,
         'guesses_with_feedback': [],
         'is_game_on': False,
         'callback': lambda event, data: print('Event: {}\n{}'.format(event, state))
        }

# Handlungsoptionen
def game_new():
    '''starte ein neues Spiel'''
    state['guesses_with_feedback'].clear()
    state['number_to_guess'] = random.randint(*state['range'])
    state['is_game_on'] = True
    state['callback']('new_game', state)
    
def game_guess(zahl):
    '''behandle Rateversuch'''
    if state['is_game_on']:
        feedback = sign(zahl - state['number_to_guess'])
        if feedback == 0:
            state['is_game_on'] = False
        state['guesses_with_feedback'].append((zahl, feedback))
        state['callback']('guess', state)  
