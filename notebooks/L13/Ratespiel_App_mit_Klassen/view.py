from ipycanvas import MultiCanvas

class View: 
    def __init__(self, config, game):
        self.game = game
        self.game.register_callback(self.callback)
        
        for k,v in config.items():
            setattr(self, k,v)
        
        self.widget = MultiCanvas(2, 
                                  width=self.width, 
                                  height=self.height, 
                                  layout={'border' : '2px solid black'},
                                 )
        self.bg, self.fg = self.widget
        self.bg.font = self.font
        self.bg.fill_text(self.text, *self.text_pos)

    def on_new_game(self, game = None):
        '''loesche Vordergrund, zeichne Skala'''
        self.fg.clear()
        self.fg.stroke_lines([self.line_start, self.line_end])
      
    def get_pt_pos(self, zahl, upper):
        '''gibt x und y Koordinate des Punktes zurueck,
           der zahl auf der Skala repraesentiert
        '''
        x0, y0 = self.line_start
        x1 = self.line_end[0]
        return x0 + (x1 - x0)/(upper-1) * (zahl-1), y0        
        
    def on_guess(self, game):
        '''Zeichen Versuch auf Skala ein'''
        guess, feedback = game.guesses_with_feedback[-1]
        self.fg.fill_style = self.colors[feedback]
        pos = self.get_pt_pos(guess, game.range[1])
        self.fg.fill_circle(*pos, radius = self.pt_size)         

    def callback(self, event, data):
        '''rufe Methode mit Namen 'on_' + event auf'''
        getattr(self, 'on_' + event)(data)
        
    def _ipython_display_(self):
        display(self.widget)
