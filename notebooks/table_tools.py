
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
    
    for i in range(n):
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
