import  os
from .observable import Observable
from . import helpers, searchables

class NBSearcher(Observable):
    '''NBSearcher(root)
       its method
         search(root_dir, all_pats=(), any_pats=(), max_res=5)
       calls the registered callbacks with arguments 'search' and
       (len(self.results), self.results[:max_res])
    '''
   
    def __init__(self, root='/home/probst/Projects/JupyterNotebooks'):
        self.root = root
        self.results = None
        
    def search(self, rootdir, all_pats=(), any_pats=(), max_res=5):
        pats = set(all_pats) | set(any_pats)
        results = []
       
        # iterator
        files = helpers.file_iter(rootdir, 
                                  filetypes = ('.ipynb', '.py'), 
                                  exclude_dirs=('__pycache__', 'src'),
                                 )
        for fn in files:
            s = searchables.Searchable(fn)
            d = s.search(pats)
            
            all_scores = [d[x] for x in all_pats]
            any_scores = [d[x] for x in any_pats]
            score = helpers.get_score(all_scores, any_scores)
            
            if score:
                res = {'searchable': s, 
                       'score': score, 
                      }
                results.append(res)
                
        self.results = sorted(results, key = lambda x:x['score'], reverse=True)  
        data = (len(self.results), self.results[:max_res])
        self._notify('search', data)
      
    def __repr__(self):
        return 'NBSearcher(root={})'.format(self.root)
