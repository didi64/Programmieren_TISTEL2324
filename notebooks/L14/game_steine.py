import time, random

def engine(state, ptm):
    # nicht besetzte Spielfelder
    options = [i for i in range(64) if i not in state[0] and i not in state[1]]
    return random.choice(list(state[ptm])), random.choice(options)

class Game:
    
    def __init__(self):
        self.player_name = {0:'Rot', 1: 'Gelb'}
        self.position = {0: set((0, 2, 4, 6)),
                         1: set((59,)),
                        }
        self.ptm = 0 # player to move
        
    def is_legal(self, player, src, target):
        # Spieler ist nicht am Zug
        if player != self.ptm:
            return False
        # Spieler hat keinen Stein auf Feld src
        if src not in self.position[player]:
            return False
        # Zielfeld kein legales Feld
        if target < 0 or target > 63:
            return False
        # Zielfeld besetzt
        if target in self.position[player]:
            return False
        if target in self.position[1-player]:
            return False
        
        return True
    
    def move(self, player, src, target):  
        if not self.is_legal(player, src, target):
            return
        
        self.position[player].remove(src)
        self.position[player].add(target)
        
        # ruft noch zu registrierendes Callback auf
        self.callback('move_stone', (player, src, target))
        
        self.ptm = 1 - self.ptm
        
        player = self.player_name[self.ptm]
        if callable(player):
            src, target = player(self.position, self.ptm)
            time.sleep(1)
            self.move(self.ptm, src, target)
    def __repr__(self):
        return 'Am Zug: {}\nPosition: {}'.format(self.player_name[self.ptm], self.position)                
