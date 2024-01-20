from ipycanvas import MultiCanvas

# View-Konfiguration
WIDTH =  200
HEIGHT = 50
LINE_START = (20, 40)
LINE_END = (180, 40)
PT_SIZE = 3
FONT = '20px serif'
TEXT = 'Guess a Number'
TEXT_POS = (20, 20)
COLORS = {-1: 'blue', 0: 'green', 1: 'red'}

widget = MultiCanvas(2, width=WIDTH, height=HEIGHT, layout={'border' : '2px solid black'})
bg, fg = widget
bg.font = FONT
bg.fill_text(TEXT, *TEXT_POS)

def on_game_new(state):
    '''loesche Vordergrund, zeichne Skala'''
    fg.clear()
    fg.stroke_lines([LINE_START, LINE_END])
      
def get_pt_pos(zahl, upper):
    '''gibt x und y Koordinate des Punktes zurueck,
       der zahl auf der Skala repraesentiert
    '''
    x0, y0 = LINE_START
    x1 = LINE_END[0]
    return x0 + (x1 - x0)/(upper-1) * (zahl-1), y0        
        
def on_game_guess(state):
    '''Zeichen Versuch auf Skala ein'''
    guess, feedback = state['guesses_with_feedback'][-1]
    fg.fill_style = COLORS[feedback]
    pos = get_pt_pos(guess, state['range'][1])
    fg.fill_circle(*pos, radius = PT_SIZE)            
    
# callback die auf Canvas schreibt
event_action = {'new_game': on_game_new, 'guess': on_game_guess}
callback = lambda event, data: event_action[event](data)    
