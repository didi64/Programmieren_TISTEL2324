class Game:
    def __init__(self, n = 9):
        self.players = [0, 1]
        self.nstones = n
        self.muehlen = ([[(r, i), (r, i+1), (r, (i+2) % 8)] 
                         for r in range(3) for i in range(8) if self.is_even(i)
                        ] +
                        [[(0, i), (1, i), (2, i)] for i in range(8) if self.is_odd(i)]
                       )
        self.callback = lambda event, data: print(event, data)
        
    def new_game(self):
        self.board = {(r, i): None for r in range(3) for i in range(8)}
        self.ptm = 0 # player to move
        self.ply = 0 # Halbzuege
        self.muehle = False  # hat jemand eine Muehle
        self.phase = 'place' # place, move
        self.winner = None   # 0 oder 1 oder None
        
        self.callback('new_game', (None,))
        data = (self.ptm, self.phase, self.muehle, self.winner, self.nstones)
        self.callback('show_status', data)
       
    def is_even(self, i):
        return i % 2 == 0
    
    def is_odd(self, i):
        return i % 2 == 1
    
    def is_adjacent(self, stone1, stone2):
        r, i = stone1
        s, j = stone2
        return (r == s and abs(i - j) in (1, 7) 
                or abs(r - s) == 1 and i == j and self.is_odd(i)
               )
                
    def is_blocked(self, stone):
        return None not in set(p for pos, p  in self.board.items() if self.is_adjacent(stone, pos))
                
    def cannot_move(self, player):
        stones = self.get_stones(player)
        locked_in = len(stones) > 3 and all(self.is_blocked(stone) for stone in  stones)
        return self.phase == 'move' and (len(stones) < 3 or locked_in)
                 
    def is_free(self, pos):
        return self.board[pos] is None
    
    def get_stones(self, player):
        return [stone for stone, p  in self.board.items() if p == player]
        
    def is_muehle(self, stone):
        for muehle in self.muehlen:
            if stone in muehle and len(set(self.board[pos] for pos in muehle)) == 1:
                return True
          
    def only_muehlen(self, player):
        stones = self.get_stones(player)
        return all(self.is_muehle(stone) for stone in stones)
    
    def is_legal(self, player, tp, src, target=None):
        # Spieler nicht am Zug oder Spiel zu Ende
        if player != self.ptm or self.winner is not None:
            return
        
        # Muehle, aber kein Stein wird entfernt
        if self.muehle and tp != 'r':
            return 
        
        def check_remove():
            target  =  self.board[src] == 1 - self.ptm
            removable =  not self.is_muehle(src) or self.only_muehlen(1 - self.ptm)
            return self.muehle and target and removable
           
        def check_place():
            return self.phase == 'place' and self.is_free(src)
               
        def check_move():
            adjacent_or_jump =  self.is_adjacent(src, target) or len(self.get_stones(self.ptm)) == 3
            ok =  self.board[src] == self.ptm and  self.is_free(target) 
            return self.phase == 'move' and ok and adjacent_or_jump
           
        return {'r': check_remove, 'p': check_place, 'm': check_move}[tp]()   
            
    def move(self, player, tp, src, target=None):
        if not self.is_legal(player, tp, src, target):
            return
        
        if tp == 'p':
            self.board[src] = player
            self.muehle = self.is_muehle(src)
            if self.ply >= 2 * self.nstones - 1:
                self.phase = 'move'
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
       
        self.update_ptm_and_winner()
        
    def update_ptm_and_winner(self):
        if self.cannot_move(1 - self.ptm):
            self.winner = self.ptm
            
        if self.winner is None and not self.muehle:
            self.ptm = 1 - self.ptm   
            self.ply += 1
            
        stones_left = self.nstones - self.ply // 2
        data =  (self.ptm, self.phase, self.muehle, self.winner, stones_left)
        self.callback('show_status', data)
        
    def __repr__(self):
        return 'Am Zug: {}\nWinner: {}\nBoard {}'.\
                format(self.ptm, self.winner, self.board)
