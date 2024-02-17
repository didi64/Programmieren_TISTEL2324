from ipywidgets import VBox, HBox, Button
from .pattern_collector import PatternCollector
from .pathselector import PathSelector

class Controller:
    def __init__(self, nbsearcher):
        self.nbsearcher = nbsearcher
        self.pc = PatternCollector()
        self.ps = PathSelector(rootdir=nbsearcher.root)
        self.button = Button(description = 'suche!', 
                             layout = {'border' : '2px solid red', 'width'  : '100px'},
                            )
        self.button.on_click(self.on_click)
        self.widget = VBox(children = [HBox(children = [self.ps.widget, self.pc.widget]), self.button])
        
    def on_click(self, bt):
        self.pc.update_state()
        self.nbsearcher.search(self.ps.path, self.pc.all_pats, self.pc.any_pats, self.pc.max_res)
    
    def __repr__(self):
        return 'Controller({})'.format(self.nbsearcher)
    
    def _ipython_display_(self):
        display(self.widget)       
