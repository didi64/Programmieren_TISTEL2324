class Game:
    
    def __init__(self):
        self.position = [None] *6
       
    def callback(self):
        print('Message from Callback:',  e, d)
        
    def are_valid(self, idxs):
        '''gibt True zurueck falls alle idx in der Liste idxs
           gueltige Indices fuer position sind
        '''   
        return all(0 <= idx < len(self.position) for idx in idxs)
    
    def is_legal(self, move_type, idxs):
        if not self.are_valid(idxs):
            return
        
        if move_type == 'place':
            src = idxs[0]
            return not self.position[src]
        
        if move_type == 'move':
            src, target = idxs
            return self.position[src] and not self.position[target]
           
    def place(self, src):  
        if not self.is_legal('place', (src,)):
            return
        
        self.position[src] = True
        self.callback('place_stone', (src,))
        
    def move(self, src, target):  
        if not self.is_legal('move', (src, target)):
            return
        
        self.position[src] = False
        self.position[target] = True
        self.callback('move_stone', (src, target))
        
    def __repr__(self):
        return 'Position: {}'.format(self.position)
