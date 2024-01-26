HELP = '''\
- press 'n' to start a new game
- press 12 to move a disk for stack 1 to stack 2
''' 

class Game:
    def __init__(self):
        self.stacks = []
        self.callback = lambda event, data: print('Event: {}\nData: {}'.format(event, data))
        
    def new_game(self):
        self.stacks[:] = [list(range(4)), [], []]
        self.callback('new_game', {'stacks': self.stacks})

    def move_disk(self, i, j):    
        x = self.stacks[i].pop()
        self.stacks[j].append(x)
        self.callback('move_disk', {'move': (i,j), 'stacks': self.stacks})
        
class View:
    from ipycanvas import Canvas
    
    positions = [50, 150, 250]
    disk_widths = [90, 70, 50, 30]
    disk_height = 10
    stack_width = 100
    colors = ['#8f5902', '#204a87', '#c4a000', '#f57900'] 
    
    def __init__(self, game):
        self.game = game
        self.game.callback = lambda event,data:self.draw_stacks(data['stacks'])
        self.canvas = View.Canvas(width = 300, height = 100, layout={'border': '1px solid black'})
        
    def draw_stack(self, stack, x):
        self.canvas.clear_rect(x - self.stack_width/2, 0, self.stack_width, self.canvas.height)
        for i, disk in enumerate(stack):
            self.canvas.fill_style = self.colors[disk]
            w = self.disk_widths[disk]
            h = self.disk_height
            self.canvas.fill_rect(x - w/2, self.canvas.height-(i+1)*h, w, h)
        
    def draw_stacks(self, stacks):
        for x, stack in zip(self.positions, stacks):
            self.draw_stack(stack, x)    
            
    def _ipython_display_(self):
        display(self.canvas)
        
class Controller:
    def __init__(self, game, view):
        self.game = game
        self.view = view
        self.view.canvas.on_key_down(self.on_key_down)
        self.src = None

    def on_key_down(self, key, *flags):
        if key in '123' and self.src is None:
            self.src = int(key) - 1
        elif key in '123' and self.src is not None:
            dst = int(key) - 1
            self.game.move_disk(self.src, dst)
            self.src = None
        elif key == 'n':
            self.game.new_game()
            self.src = None    
        else:
            self.src = None

print(HELP)
game = Game()
view = View(game)
controller = Controller(game, view)
display(view)