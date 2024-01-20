from ipywidgets import Output
widget = Output(layout={'border': '1px solid black'})
def callback(event, state):
    widget.clear_output()
    with widget:
        print('Event: {}'.format(event))
        print('Game on: {}, Range: {}, Versuche: {}'.
              format(state['is_game_on'], 
                     state['range'], 
                     state['guesses_with_feedback']))
