from .nb_searcher import NBSearcher
from .view import View
from .controller import Controller

def run():
    nbs = NBSearcher()
    display(Controller(nbs), View(nbs))