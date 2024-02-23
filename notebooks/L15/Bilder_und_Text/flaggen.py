def draw_BRD_flag(canvas, pos, size):
    '''BRD Flagge: Seitenverhaeltnis Hoehe:Breite = 3:5,
       3 horizontale Streifen: schwarz, gel, rot
    '''   
    x0, y0 = pos
    canvas.fill_style = 'gray'
    canvas.fill_rect(x0, y0, size)

    for i, color in [(1, 'black'), (2, 'red'), (3, 'yellow')]:
        canvas.fill_style = color
        canvas.fill_rect(x0, y0 + i/5 * size, width = size, height = size/5)  

def draw_BE_flag(canvas, pos, size):
    '''BE Flagge: Seitenverhaeltnis Hoehe:Breite = 13:15,
       3 vertikale Streifen: schwarz, gelb, rot
    '''
    x0, y0 = pos
    canvas.fill_style = 'gray'
    canvas.fill_rect(x0, y0, size)
   
    for i, color in enumerate(('black', 'yellow', 'red')):
        canvas.fill_style = color
        canvas.fill_rect(x0 + i/3 * size, y0 + 1/15 * size, width = size/3, height = 13/15*size)
