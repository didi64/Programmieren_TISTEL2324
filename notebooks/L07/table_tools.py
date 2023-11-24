import random

def random_word(length, alphabet):
    '''gibt ein Wort der Laenge length mit Buchstaben
       aus der Liste/String alphabet zurueck
    '''   
    letters = random.choices(alphabet, k=length)
    word = ''.join(letters)
    return word

def random_words(n):
    '''gibt eine Liste mit n zufaelligen Woertern zurueck'''
    bounds = (3, 15)
    abc = 'abcdefghijklmnopqrstuvwxyz'
    words = []
    
    for _ in range(n):
        length = random.randint(*bounds)
        word = random_word(length, abc)
        words.append(word)
        
    return words 


def random_table():
    '''gibt eine zufaellige Tabelle zurueck'''
    table = []
    nrows = random.randint(3, 10)
    ncols = random.randint(1, 5)
    
    for _ in range(nrows):
        row = random_words(ncols)
        table.append(row)
        
    return table    

def _get_col_widths(header, table):
    '''table:   Liste von Listen
       Header:  Liste (Kopfzeile)
       returns: Liste mit den maximalen Spaltenbreiten 
    '''
    maxcolwidths = [len(col)  for col in header] 
   
    for row in table:
        for i,col in enumerate(row):
            width = len(col)
            if width > maxcolwidths[i]:
                maxcolwidths[i] = width
         
    return maxcolwidths    

def _print_table(widths, header, table):
    '''widths: Liste mit Spaltenbreiten
       header: Liste mit Spaltentiteln
       table:  Liste mit Tabellenzeilen
       
       gibt Header- und Tabellenspalten linksbuendig aus
       mit Breiten widths
    '''   
    hlines = ['-' * width   for width in widths]
    fheader = [col.ljust(width) for col, width in zip(header, widths)]
    ftable = [[col.ljust(width) for col, width in zip(row, widths)]  for row in table]
    
    print(' | '.join(fheader))
    print(' | '.join(hlines))
    for row in ftable:
        print(' | '.join(row))
        
def show_table(header, table):
    '''gibt Header und Tabelle formatiert aus
       header: Liste mit Spaltentiteln
       table:  Liste mit Tabellenzeilen
    '''
    widths =  _get_col_widths(header, table)
    _print_table(widths, header, table)        