import re
from ipywidgets import VBox, HBox, Button, Text, Checkbox, BoundedIntText
from . import helpers

class PatternCollector:
    
    def __init__(self):
        self.state = {}
        #self.descs = ['Regex', 'gross/klein egal', 'Alle:', 'Manche:']
        
        self.all_pats = []
        self.any_pats = []
        self.checkbox_re = Checkbox(indent=False, layout={'width': '100px'})
        self.checkbox_ic = Checkbox(value = True, indent=False, layout={'width': '100px'})
        self.textbox1 = Text(value = '', 
                             placeholder='Stichworte: Funktion, ...',
                             continuous_update = False,
                            )
        self.textbox2 = Text(value = '', 
                             placeholder='Stichworte: dict, ...',
                             continuous_update = False,
                            )
        self.int_text = BoundedIntText(value=5, min=1, layout={'width': '150px'})
        self.widgets = [self.textbox1, self.textbox2, self.checkbox_re, self.checkbox_ic, self.int_text] 
        self.descriptions = ['Alle:', 'Manche:', 'Regex', 'Case egal', 'Resultate:']
        for w, descr in zip(self.widgets, self.descriptions):
            w.description = descr
        
        self.hbox = HBox(children=[self.checkbox_re, self.checkbox_ic, self.int_text]) 
        self.widget = VBox(children=[self.textbox1, self.textbox2, self.hbox])
       
    def update_state(self):
        for w in self.widgets:
            self.state[w.description] = w.value
            
        kwargs = {'escape': not self.state['Regex'], 
                  'flags': not self.state['Case egal'] or re.IGNORECASE,
                 }
        self.all_pats = [helpers.make_pat(p.strip(), **kwargs) 
                         for p in self.state['Alle:'].split(';') if p]
        
        self.any_pats =  [helpers.make_pat(p.strip(), **kwargs) 
                          for p in self.state['Manche:'].split(';') if p]
        self.max_res = self.state['Resultate:']
       
    def __repr__(self):
        return 'PatternCollector()'
        
    def _ipython_display_(self):
        display(self.widget)   
