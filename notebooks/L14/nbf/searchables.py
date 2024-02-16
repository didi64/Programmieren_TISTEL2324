'''\
Searchable(path_to_file, **kwargs)
creates a searchable object that implements the methods
- search(patterns, **kwargs)
  returns a dictionary `{pat: score,...}` 
- description(**kwargs)  
  returns a dictionary with keys 'mimetype' and 'content', where mimetype is e.g.
  'text/plain' or 'text/markdown' and content is a str.
'''
import ast, json, os
from .helpers import echo_args

class Notebook:
    
    def __init__(self, path_to_file, **kwargs):
        self.path_to_file = path_to_file
        self.kwargs = kwargs
      
    def _as_json(self):
        with open(self.path_to_file, 'r') as f:
            nb = json.loads(f.read())
        return nb   
    
    def search(self, pats):
        '''pats: iterable of compiled regexes
           returns a dict {pattern: number of matches for each pattern in pats}
        '''   
        d = dict.fromkeys(pats, 0)
        
        json = self._as_json()
        for cell in json['cells']:
            if cell['cell_type'] not in ('code', 'markdown'):
                continue

            for line in  cell['source']:
                for pat in pats:
                    d[pat] += bool(pat.search(line))

        return d     
    
    def description(self):
        first_cell = self._as_json()['cells'][0] 
        if first_cell['cell_type'] == 'markdown':
            md = ''.join(first_cell['source'])
            return {'mimetype': 'text/markdown', 'content': md}

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, echo_args(self.path_to_file, **self.kwargs))    
    
class PyFile:
    
    def __init__(self, path_to_file, **kwargs):
        self.path_to_file = path_to_file
        self.kwargs = kwargs
      
    def _get_lines(self):
        with open(self.path_to_file, 'r') as f:
            lines = f.readlines()
        return lines
    
    def search(self, pats):
        '''pats: iterable of compiled regexes
           returns a dict {pattern: number of matches for each pattern in pats}
        '''   
        d = dict.fromkeys(pats, 0)
        lines = self._get_lines()
        for line in  lines:
            for pat in pats:
                d[pat] += bool(pat.search(line))

        return d     
    
    def description(self):
        with open(self.path_to_file, 'r') as f:
            tree = ast.parse(f.read())
            docstring = ast.get_docstring(tree, clean=True)
            return {'mimetype': 'text/plain', 'content': docstring}

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, echo_args(self.path_to_file, **self.kwargs))    
    
def Searchable(path_to_file, **kwargs):
    fn, ext = os.path.splitext(path_to_file)  
    cls = filetypes_class.get(ext)
    if not cls:
        raise TypeError('Filetype {} is not supported')
    return cls(path_to_file, **kwargs)    
    
filetypes_class = {'.ipynb': Notebook, '.py': PyFile}    
