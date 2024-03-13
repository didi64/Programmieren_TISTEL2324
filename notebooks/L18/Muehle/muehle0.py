class Game:
    def __init__(self):
        self.players = [0, 1]
        self.muehlen = ([[(r, i), (r, i+1), (r, (i+2) % 8)] 
                         for r in range(3) for i in range(8) if self.is_even(i)
                        ] +
                        [[(0, i), (1, i), (2, i)] for i in range(8) if self.is_odd(i)]
                       )
        self.callback = lambda event, data: print(event, data)
        
    def new_game(self):
        self.board = {(r, i): None for r in range(3) for i in range(8)}
        self.ptm = 0 # player to move
        self.muehle = False  # hat jemand eine Muehle
        self.phase = 'place' # place, move
        self.callback('new_game', (None,))
       
    def is_even(self, i):
        return i % 2 == 0
    
    def is_odd(self, i):
        return i % 2 == 1
    
    def is_muehle(self, stone):
        for muehle in self.muehlen:
            if stone in muehle and len(set(self.board[pos] for pos in muehle)) == 1:
                return True
          
    def move(self, player, tp, src, target=None):
        if tp == 'p':
            self.board[src] = player
            self.muehle = self.is_muehle(src)
            self.callback('place_stone', (src, player))
        elif tp == 'm':
            self.board[src] = None
            self.board[target] = player 
            self.muehle = self.is_muehle(target)
            self.callback('move_stone', (src, target, player))
        elif tp == 'r':
            self.board[src] = None
            self.muehle = False
            self.callback('remove_stone', (src,))
       
        if not self.muehle:
            self.ptm = 1 - self.ptm   
        else:
            print('muehle')
        
    def __repr__(self):
        return 'Am Zug: {}\nBoard {}'.\
                format(self.ptm, self.board)
