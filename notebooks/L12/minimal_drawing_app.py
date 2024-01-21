from ipycanvas import MultiCanvas, Canvas

HELP = '''\
Zeichen Linie von Maus-Down nach Maus-Up.
Tasten: Shift vor Maus-Up: zeichne Kreis statt Linie
        ESC vor Maus-Up:   zeichen nichts
        c:                 loesche Zeichnung
        q:                 quit
        1, ..., 9:         setzt Linienbreite
        r, g, b, y, k, o:  setzt Farbe (red, green, blue, yellow, black, orange)
'''

def distance(pt1, pt2):
    '''return the distance between the points pt1=(x1,y1) and pt2=(x2,y2)'''
    return ((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)**0.5    

def on_mouse_down(x, y):
    '''update state
       zeichne Punkt (Kreis mit Radius halbe line_width) auf mg
    '''
    state['pt'] = (x, y)
    state['mouse_down'] = True
    mg.fill_circle(x, y, radius = bg.line_width / 2)

def on_mouse_up(x, y):
    '''update state
       zeichen auf bg (background), je nach gedrueckter Taste
       loesche mg (middleground)
    '''
    state['mouse_down'] = False
    pt_current = (x, y)
    pt_clicked = state['pt']
    
    if state['key_pressed'] == 'Shift':
        r = distance(pt_clicked,  pt_current)
        bg.stroke_circle(*pt_clicked, r)
    elif  state['key_pressed'] == 'Escape':   
        pass
    else:    
        line = [pt_clicked,  pt_current]
        bg.stroke_lines(line)
        
    state['key_pressed'] = None
    show_state(fg)
    mg.clear()
    
def on_key_down(key, *flags):
    '''update state['key_pressed']
       je nach state und gedrueckter Taste: set stroke_style und line_width von bg und fg
       redraw state on fg (foregrond)
    '''
    if state['mouse_down']:
        state['key_pressed'] = key
        
    if key == 'c':
        bg.clear()
    elif key == 'q':
        mcanvas.close()
        return
    elif key in colors:
        fg.stroke_style = colors[key]
        bg.stroke_style = colors[key]
    elif key in '123456789':
        fg.line_width = int(key)
        bg.line_width = int(key)
        
    show_state(fg)    
    
def show_state(fg):
    '''show state on fg (foreground)'''
    pts = [(x, HEADER_Y) for x in  HEADER_XS]
    fg.clear()
    
    fg.fill_text('Linewidth: ', *pts[0])
    fg.stroke_lines(pts[1:3])
    
    text = 'key: {}'.format(state['key_pressed'])
    fg.fill_text(text , *pts[3])    
    
WIDTH = 300
HEIGHT = 200
HEADER_Y = 20
HEADER_XS = (10, 100, 150, 170)
FONT = '12px serif'  # https://ipycanvas.readthedocs.io/en/latest/drawing_text.html
LINEWIDTH = 4
LAYOUT = {'border': '1px solid black'}    

mcanvas    = MultiCanvas(3, width=WIDTH, height=HEIGHT, layout = LAYOUT)
bg, mg, fg  = mcanvas # Background, Middleground, Foreground, 3 uebereinanderliegende Canvas'

fg.font = FONT
fg.text_baseline = 'middle'
fg.line_width = LINEWIDTH
bg.line_width = LINEWIDTH

state  = {'pt': (0,0), 'mouse_down': False, 'key_pressed': None}
colors = {'r': 'red', 'g': 'green', 'b':'blue', 'y': 'yellow', 'k': 'black', 'o': 'orange'}

# registriere obige Funktionen als Callbacks 
mcanvas.on_mouse_down(on_mouse_down)
mcanvas.on_mouse_up(on_mouse_up)
mcanvas.on_key_down(on_key_down)

print(HELP)
show_state(fg)
display(mcanvas)

