import os
from .nb_searcher import NBSearcher
from .view import View
from .controller import Controller

def run(root=None):
    if root is None:
        root = '/home/tistel/venvs/python3.12/work'
    if root.isnumeric():
        n = int(root)
        root = os.path.join(os.curdir,*[os.pardir]*n)
    
    nbs = NBSearcher(root=root)
    display(Controller(nbs), View(nbs))