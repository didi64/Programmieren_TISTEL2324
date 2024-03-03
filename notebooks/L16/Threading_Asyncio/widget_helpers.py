import random
from ipywidgets import  Output, Button, HBox, VBox
from ipycanvas import Canvas

class Widget:
    
    def __init__(self):
        self.bt_names = ('start', 'pause', 'stop')
        self.callbacks = dict.fromkeys(self.bt_names)
        
        layout = {'border': '1px solid black'}
        self.out = Output(layout={'border': '1px solid black'})
        self.canvas = Canvas(width=300, height=100, layout={'border': '1px solid black'})
        self.buttons = {'start': Button(description='start', layout=layout),
                        'pause': Button(description='pause', layout=layout),
                        'stop' : Button(description='stop',  layout=layout),
                        'clear': Button(description='clear', layout=layout),
                       }
        self.widget = VBox(children = [self.canvas, self.out, 
                                  HBox(children = tuple(self.buttons.values())),
                                 ],
                           layout={'width': '300px'}
                     )
        
        self.canvas.on_key_down(self.on_key_down)
        self.buttons['clear'].on_click(lambda bt:self._clear())
        
        callbacks = {'start': self._start, 
                     'pause': self._pause,
                     'stop':  self._stop,
                    }
        self.register_callbacks(callbacks)
     
    def draw_pt(self):
        w = self.canvas.width
        h = self.canvas.height
        x, y = random.choice(range(w)), random.choice(range(h))
        self.canvas.fill_circle(x, y, 2)   
        
    def register_callbacks(self, callbacks):
        assert all(callable(f) for f in callbacks.values()),\
               'values of callbacks must be callabels'
        assert all(bt in self.bt_names for bt in callbacks),\
               'keys of callbacks must be in {}'.format(self.bt_names)
        
        for bt_name, fun in callbacks.items():
            if f := self.callbacks.get(bt_name):
                # remove old callback
                self.buttons[bt_name].on_click(f, remove=True)
           
            # redirect output and adjust signature
            f_out = self.out.capture()(fun)
            f = lambda bt, func=f_out: func()
            # add new callback
            self.callbacks[bt_name] = f
            self.buttons[bt_name].on_click(f)
      
    def _start(self):
        print('start pressed')
        
    def _pause(self):
        print('pause pressed') 
        
    def _stop(self):
        print('stop pressed')   
  
    def _clear(self):
        self.out.clear_output()
        self.canvas.clear()
        
    def on_key_down(self, key, *flags):
        colors = {'r':'red','g':'yellow' ,'b': 'blue'}
        if key in colors:
            self.canvas.fill_style = colors[key]
            
    def _ipython_display_(self):
        display(self.widget)
        
