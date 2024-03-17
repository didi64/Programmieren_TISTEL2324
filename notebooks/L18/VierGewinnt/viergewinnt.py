TIE = 2
class Game:
    '''
    game = Game() creates a game-instance
    game.new_game() starts a new game of  4-gewinnt.
    game.drop_piece(col) drops a piece in column col
    
    The function game.callback is intended to be overwritten by a class responsible for the presentation
    and is called 
    - if a new game is started, with arguments 
      'new_game', {'player': player, 'rows': rows, 'cols': cols)}
    - if a piece is dropped, with arguments 
      'place_piece', {'player': player, 'pos': (row, col)})   
    - if the game ends, with arguments 
      'update_result', {'result': result}
    '''
    def __init__(self):
        self.players = (0, 1)
        self.results = {0: 'Player 0 wins', 1: 'Player 1 wins', TIE: 'tie', None: None}
        self.callback = lambda event, data: print('event: {}, data: {}'.format(event, data))
        
    def new_game(self, cols = 7, player=0):
        '''starts a new game
           cols: int, number of columns
           player: either 0 or 1, player who starts
        '''   
        self.ptm = player # Spieler am Zug
        self.cols = cols
        self.rows = cols - 1
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        
        self.col_heights = [0] * self.cols # Fuellstand der Spalten
        self.ply = 0 # gespielte Halbzuege
        self.result = None # None, 0, 1, TIE
        
        self.callback('new_game', {'player': self.ptm, 'rows': self.rows, 'cols': self.cols})
        
    def is_game_over(self):
        return self.result is not None
    
    def get_field(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.board[row][col]
        
    def drop_piece(self, col):
        '''drops a stone in column col if game is still on and column not full'''
        row = self.col_heights[col]
        if self.is_game_over() or row == self.rows:
            return
        
        self.board[row][col] = self.ptm
        self.col_heights[col] += 1
        self.ply += 1
        self.callback('place_piece', {'player': self.ptm, 'pos': (row, col)})        
               
        if self.is_4gewinnt(row, col):
            self.result = self.ptm
        elif self.ply == self.rows*self.cols:
            self.result =  TIE
            
        if self.result is None:
            self.ptm = 1 - self.ptm
        else:
            self.ptm = None
            self.callback('update_result', {'result': self.result})
        
    def _n_connect(self, row, col, dr, dc, d=1):
        '''returns number of fields with same stone as in (row, pos) in direction (d*dr,d*dc)
           0 if stone has no neighbor of its kind
        '''
        p = self.board[row][col]
        i = 0
        while self.get_field(row + (i + 1)*d*dr, col + (i + 1)*d*dc) == p:
            i += 1
        return i 

    def is_4gewinnt(self, row, col):
        '''returns True if stone at (row, col) contributes to a 4gewinnt'''
        for vec in [(0, 1), (1, 0), (1, 1), (-1, 1)]:
            if sum(self._n_connect(row, col,*vec, d) for d in (-1, 1)) == 3:
                return True
        
    def _board2str(self):
        rows = [['{}'.format(x) for x in row] for row in self.board]
        return '\n'.join('{}'.format(row) for row in rows[::-1])
    
    def __repr__(self):
        return 'Am Zug: {}\nResultat: {}\n{}'.\
            format(self.ptm, self.results[self.result], self._board2str())
