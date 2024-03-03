import math
from ipycanvas import hold_canvas

def pts_on_circle(n, width, height):
    '''return [(with*cos(2*i*pi/n), -height*sin(2*i*pi/n)) for i in range(n)]'''
    alphas = [2*i*math.pi/n for i in range(n)]
    pts = [(width*math.cos(alpha)+100, -height*math.sin(alpha)+100) for alpha in alphas]
    return pts

def bar_ra_rc(game):
    x, y, w, h = game['bar']
    dx = game['bar_speed']
    if  game['bar_dir'] > 0:
        rect_to_add = (x+w, y, dx, h)
        rect_to_clear = (x, y, dx, h)
    else:
        rect_to_add = (x-dx, y, dx, h)
        rect_to_clear = (x+w-dx, y, dx, h)
        
    return rect_to_add, rect_to_clear

def update_bar_dir(game, lower, upper):
    x, _, width, _ = game['bar']
    if x <= lower:
        game['bar_dir'] = 1
    elif x + width >= upper:
        game['bar_dir'] = -1
        
def update_ball_dir(game, err = 5):
    i = game['ball_idx']
    i_next = (i + game['ball_speed'] * game['ball_dir']) % game['N']
    
    x0, y0 = game['pts'][i]
    x1, y1 = game['pts'][i_next]
    
    bar_x, bar_y, w, _ = game['bar']
    if (y0-err < bar_y < y1+err) and (bar_x < x0 < bar_x + w):
        game['ball_dir'] *= -1
        
def move_bar(game, canvas):
    update_bar_dir(game, 0, canvas.width)
    rect_to_add, rect_to_clear = bar_ra_rc(game)
    with hold_canvas():    
        canvas.fill_rect(*rect_to_add)
        canvas.clear_rect(*rect_to_clear)
    
    game['bar'][0] += game['bar_dir'] * game['bar_speed']
   
    
def move_ball(game, canvas):   
    update_ball_dir(game)
    i = game['ball_idx']
    j = (i + game['ball_speed'] * game['ball_dir']) % game['N']
    r = game['ball_r']
    x0, y0 = game['pts'][i]
    x1, y1 = game['pts'][j]
    with hold_canvas():    
        canvas.clear_rect(x0-(r+1), y0-(r+1), 2*(r+1))    
        canvas.fill_circle(x1, y1, r)
      
    game['ball_idx'] = j    
