from ipycanvas import Canvas, MultiCanvas

def remove_all_callbacks(obj):
    '''remove all registered callbacks from a Canvas/MultiCanvas object'''
    d =  {'on_mouse_down': '_mouse_down_callbacks', 
          'on_mouse_up':   '_mouse_up_callbacks',
          'on_mouse_move': '_mouse_move_callbacks',
          'on_mouse_out':  '_mouse_out_callbacks',
          'on_key_down':   '_key_down_callbacks', 
         }

    if isinstance(obj, Canvas):
        widget = obj
    elif isinstance(obj, MultiCanvas):
        widget = obj[-1]
    else:
        raise TypeError('obj must be an instance of Canvas of MultiCanvas')
        
    for event_name, dispatcher_name in d.items():
        dispatcher = getattr(widget, dispatcher_name, None)
        method = getattr(widget, event_name)
        # use copy!
        for callback in dispatcher.callbacks[:]:
            method(callback, remove=True)
            
    