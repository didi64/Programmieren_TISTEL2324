import os
from ipywidgets import Output
from IPython.display import Markdown

mimetype_render = {'text/plain': lambda x:x,
                   'text/markdown': lambda x:Markdown(x),
                  }
class View:
    def __init__(self, nbsearcher):
        self.nbsearcher = nbsearcher
        self.link_widget = Output(layout={'border': '1px solid black'})
        # self.cell_widget = Output(layout={'border': '1px solid black'})
        
        self.nbsearcher.register_callback(self.show_results)
       
    def clear_output(self):
        self.link_widget.clear_output()
        # self.cell_widget.clear_output()
        
    def show_results(self, event, data):
        self.clear_output()
        nres, results = data
        with self.link_widget:
                display(Markdown('**Results** ({}/{}):  \n'.format(len(results), nres)))
        for res in results:
            s = res['searchable']
            score = int(res['score'])
            with self.link_widget:
                rel_path = os.path.relpath(s.path_to_file, os.getcwd())
                link = '[({1}) {0}](<{0}>)  '.format(rel_path, score)
                link =  Markdown(link)    
                display(link)
               
            # with self.cell_widget:    
            #     descr = s.description()
            #     if descr:
            #         content = mimetype_render[descr['mimetype']](descr['content'])
            #         display(content)
              
    def _ipython_display_(self):
        display(self.link_widget)  
        #display(self.link_widget, self.cell_widget)  
