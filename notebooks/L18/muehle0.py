class Game:
    def __init__(self):
        self.players = [0, 1]
        self.muehlen = ([[(r, i), (r, i+1), (r, (i+2) % 8)] 
                         for r in range(3) for i in range(8) if self.is_even(i)
                        ] +
                        [[(0, i), (1, i), (2, i)] for i in range(8) if self.is_odd(i)]
                       )
        
        self.new_game()
        
    def new_game(self):
        self.board = {(r, i): None for r in range(3) for i in range(8)}
        self.ptm = 0
        self.result = None
       
    def is_even(self, i):
        return i % 2 == 0
    
    def is_odd(self, i):
        return i % 2 == 1
    
    def is_adjacent(self, pos1, pos2):
        r, i = pos1
        s, j = pos2
        return (r == s and abs(i - j) in (1, 7) 
                or abs(r - s) == 1 and i == j and self.is_odd(i))
                
    def is_blocked(self, pos):
        return None not in set(self.board[(r,i)] for r in range(3) for i in range(8) if self.is_adjacent(pos, (i,j)))
                
    def cannot_move(self, player):
        stones = [(r, i) for r in range(3) for i in range(9) if position[r][i] == player]
        return all(self.is_blocked(stone) for stone in  stones)   
        
    def update_result(self):
        pass
   
    def is_legal(self, player, tp, src, target=None):
        if player != self.ptm:
            return False
        
        return True
        
    def move(self, player, tp, src, target=None):
        if not self.is_legal(player, tp, src, target):
            return
        
        if tp == 'p':
            self.board[src] = player
        elif tp == 'r':
            self.board[src] = None
        elif tp == 'm':
            self.board[src] = None
            self.board[target] = player
        
        self.result = self.update_result()
        
        if tp != 'r' and not self.update_result():
            self.ptm = 1 - self.ptm   
        
    def __repr__(self):
        return 'Am Zug: {}\nResult: {}\nBoard {}'.\
                format(self.ptm, self.result, self.board)
