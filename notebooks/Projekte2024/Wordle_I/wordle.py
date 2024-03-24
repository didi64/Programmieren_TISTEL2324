import random, time #zufallsgenerator, zeit
from ipycanvas import Canvas #fur zeichnungen
from ipycanvas import MultiCanvas #mehrere canvas ebenen
from ipywidgets import Output, Button, HBox, Select, VBox, IntSlider, RadioButtons, Image #buttons etc
from IPython.display import HTML, display #html für sound

#############################################################
###VARIABELN
#############################################################

#spielfelddaten -- zeichnen
size_w = 380
size_h = 460
sizerect = 40
linewidth = 2
#Schriftgrösse
charheight = sizerect*0.8
einzug = 20
zeilenabstand = 10

#Anzahl gemachter Versuche (Zähler)
guessnbr = 0

#gameVariable
gameOn = False

#Leere liste aus der dann später Grossbuchstaben werden und Umlaute entfernt werden
words = []



#Mögliche Buchstaben die eingegeben werden können
abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
#Umlaute, die nicht eingegeben werden können/dürfen
umlauts = 'äöüÄÖÜẞ'



#Output Konsole für Texte, Fehlermeldungen etc. (kann später wenn gewünscht entfernt werden)
out = Output(layout={'border': '1px solid black'})

#Startscreen laden:
startscreen = Image.from_file('startscreen.png')

#Error Bilder laden:
error_letters = Image.from_file('error_letters.png')
error_wordlist = Image.from_file('error_wordlist.png')

#Canvas erstellen
mcanvas = MultiCanvas(8, width = size_w, height = size_h, 
                layout = {'border' : '2px solid black'}
               )
actfield, mg, check, text, keyboard, grid, welcome, end = mcanvas # mvcanvas lässt sich auspacken, bg, mg, text = mcanvas

#Textformat definieren - Linienbreite, schriftart etc
text.font = str(charheight)+'px bold'
text.line_width = linewidth

#Buttonauswahl für Wortlänge:
select_wordlength = RadioButtons(
    options=[('Vier', 4),('Fünf', 5),('Sechs', 6)],
    value=5, # Standardwert ist 5 Buchstaben
    layout={'width': 'max-content'}, # wenn zu lang
    description='Wie viele Buchstaben soll das zu erratende Wort haben?',
    disabled=False,   
)
#Schieberegler Auswahl Anzahl Versuche:
select_nbrofguesses = IntSlider(
    style = {'description_width': 'initial'},
    value=6,
    min=3,
    max=9,
    step=1,
    description='Anzahl Versuche:',
    orientation='horizontal',
)

#Button New Game
bt_newgame = Button(description = 'New Game', button_style='success',
                layout = {'border' : '2px solid black', 
                 'width'  : '100px',
                 'height' : '30px',
                }
               )

#Aneinanderreihung von den verschiedenen Elementen
menue = VBox(children = [select_wordlength, select_nbrofguesses, bt_newgame])
hbox   = HBox(children = [mcanvas, menue])

###Funktionen zum überwachen der Auswahlmöglichkeiten
def on_change_select_wordlength(change):
    mcanvas.focus()
    
def on_change_select_nbrofguesses(change):
    mcanvas.focus()




#Grid zeichnen: Das Gitter bzw Spielfeld
@out.capture()
def drawgrid():
    for i in range(nbrofguesses):
        for k in range(wordlength):
            grid.stroke_style = 'black'
            x = einzug+k*sizerect
            y = ((zeilenabstand+(i*sizerect)+i*zeilenabstand))
            grid.stroke_rect(x,y, sizerect, sizerect)
    selectfield(actcell)
    


#feld färben mit fabrcode #FFFF00 :
def selectfield(actcell):
    '''
    Nimmt die Aktuelle Zelle auf und zeichnet auf der Ebene "actfield" ein wo die nächste Eingabe gemacht wird
    '''
    actfield.clear()
    actfield.line_width = 3
    actfield.stroke_style = '#FFFF00'
    actfield.stroke_rect(actcell[0]+1,actcell[1]+1,sizerect-2,sizerect-2)
    
    #nach rechts
def moveactcellforward():
    global actcell
    if actcell[0]<xpos[wordlength-1]:
        actcell = (xpos[xpos.index(actcell[0])+1], ypos[guessnbr]) 
        selectfield(actcell)
       
    #nach links
def moveactcellbackward():
    global actcell
    if actcell[0] > einzug:
        actcell = (xpos[xpos.index(actcell[0])-1], ypos[guessnbr]) 
        selectfield(actcell)
    
    #verfärbung anhand der eingabe
def colorguess(col, guessnbr, style, sizerect, xpos, ypos):
    '''
    Befüllt die Zelle mit der entsprechenden Farbe
    '''
    check.fill_style = style
    check.fill_rect(xpos[col],ypos[guessnbr],sizerect,sizerect)

#buchstabe zeichnen
def writekey(ebene,key, actcell, gameOn=True):
    '''
    Funktion zum beschreiben der actcell
    '''
    text.clear_rect(actcell[0], actcell[1], sizerect, sizerect)
    ebene.fill_style = 'black'
    ebene.text_align = 'center'
    ebene.fill_text(key, actcell[0]+0.5*sizerect, actcell[1]+charheight)
    moveactcellforward()
    if gameOn:
        addtosol(sol,key, actcell)
    return 


def deletekey(actcell):
    '''
    Löscht den Eintrag der aktuellen Zelle
    '''
    text.clear_rect(actcell[0], actcell[1], sizerect, sizerect) #Löscht den Inhalt des Feldes
    if xpos.index(actcell[0]) in sol:
        sol.pop(xpos.index(actcell[0]), None)
    else:
        moveactcellbackward()
    return sol

#Erstellt den Willkommensbildschirm in der Ebene mit dem Bild, das als startscreen definiert ist:
def draw_welcome_screen():
    '''Zeichnet den Willkommensbildschirm mit Startbutton.
    '''
    
    welcome.fill_style = 'black'
    welcome.fill_rect(0, 0, welcome.width, welcome.height) 
    welcome.draw_image(startscreen, 0, 0)

#dassselbe mit fehler    
def draw_error_screen(errortype):
    '''Erstellt den Errorscreen.'''
  
    welcome.fill_style = 'black'
    welcome.fill_rect(0, 0, welcome.width, welcome.height) 
    welcome.draw_image(errortype, 0, 0)
    time.sleep(2)   
    welcome.clear()
    
    
#Keyboard rechts zeichnen:    
def drawkeyboard():
    keyboard.stroke_style = 'black'
    keyboard.text_align = 'center'
    keyboard.text_baseline = 'middle'
    
    
    for i,(k, v) in enumerate(d_keys.items()):
        r = 13
        if i < 13:
            xy = (315,((i+1)*(r+20)))
            pts.append(xy)
            keyboard.fill_style = v
            keyboard.fill_circle(*xy,r)
            keyboard.fill_style = 'black'
            keyboard.stroke_circle(*xy, r)
            keyboard.fill_text(k, *xy )
        if i >= 13:
            xy = (350,((i-13+1)*(r+20)))
            pts.append(xy)
            keyboard.fill_style = v
            keyboard.fill_circle(*xy,r)
            keyboard.fill_style = 'black'
            keyboard.stroke_circle(*xy, r)
            keyboard.fill_text(k, *xy)


#Endpage darstellen wenn gewonnen oder verloren
@out.capture(clear_output=True)
def endpage(won, background):
    end.fill_style = background
    end.fill_rect(0, 0, end.width, end.height)
    if won:
        message1 = 'Bravo! Spiel gewonnen!'
        message2 = 'Du hast es in '+str(guessnbr)+' Versuchen erraten'
            
    else:
        message1 = 'Leider nicht geschafft'
        message2 = 'Versuch es nocheinmal'
    
    end.font = '20px serif'
    end.fill_style = 'black'
    end.text_align = 'center'
    end.fill_text(message1, end.width / 2, 40)
    end.font = '15px serif'
    end.fill_text('Das korrekte Wort war:', end.width / 2, 65)
    end.font = str(charheight)+'px bold'
    for k in range(wordlength):
            end.fill_style = '#428D3E'
            x = 50+(einzug+k*sizerect)
            end.fill_rect(x,80, sizerect, sizerect)
            end.stroke_style = 'black'
            end.stroke_rect(x,80, sizerect, sizerect)
            writekey(end, given[k], ((50+(einzug+k*sizerect)),80), gameOn)

    end.fill_style = 'black'
    end.font = '15px serif'
    end.fill_text(message2, end.width / 2, 140)
    
    
# Funktion erstellen, um audio im loop zu spielen
def play_audio_loop(filepath):
    audio_html = f"""
    <audio controls autoplay loop>
      <source src="sound.mp3" type="audio/mp3">
        </audio>
    """
    display(HTML(audio_html))

# Pfad zu MP3 -- Nicht notebooks/PROJEKT/sound.mp3 !!! sondern nur sound.mp3
mp3_file_path = 'sound.mp3'


#############################################################
###SPIELFUNKTIONEN (LOGIK)
#############################################################

#nimmt die wortliste zusammengesetzt mit wortliste und der entsprechenden _nummer
def createwordlist(wordlength):
    file = 'wortliste_'+str(wordlength)+'.txt'
    with  open(file, mode = 'r') as f:
        wordlist = []
        for line in f:
            
            #line.split('\n')
            wordlist.append(line[:-1])
            
    return wordlist

def playablewords():
    '''
    Wort aus Wortliste uppercase in die Liste words hinzufügen wenn sie keinen Umlaut enthalten
    '''
    for word in wordlist:
        add = True
        for ch in word: 
            if ch in umlauts:
                add = False     
        if add == True:
            words.append(word.upper())
               
def newgame():
    '''
    Startet ein neues Spiel:
    Zurücksetzen aller benötigten Variabeln, neuzeichnen des Spielbretts
    '''
    global guessnbr, actcell, given, wordlength, xpos, ypos, sol, wordlist, words, einzug, d_keys, gameOn, pts, nbrofguesses
    #WelcomeScreen löschen um zu starten
    welcome.clear()
    gameOn = True
    
    wordlength = select_wordlength.index+4 #Aktualisiert die Wortlänge basierend auf der Benutzerauswahl
    nbrofguesses = select_nbrofguesses.value # Aktualisiert die Anzahl der Versuche basierend auf der Benutzerauswahl
    
    einzug = ((size_w-100)/2)-(wordlength/2*40)
    words = [] # Leert die Liste der spielbaren Wörter
    wordlist = createwordlist(wordlength)
    
    #Leere Liste pts um das Keyboard rechts zu benutzen
    pts = []
    
    #Neues Wort auswählen
    playablewords()
    #Zu lösendes Wort aus Wortliste herauspicken:
    given = list(words[random.randint(0,len(words)-1)])

    #Mögliche x-Positionen der Felder
    xpos = [einzug + i*sizerect for i in range(wordlength)]
    #Mögliche y-Positionen der Felder
    ypos = [zeilenabstand+i*(sizerect+zeilenabstand) for i in range(nbrofguesses)]
    guessnbr = 0
    sol = {} # Leert die aktuelle Lösung
    actcell = (xpos[0],ypos[0])
    mcanvas.clear()
    drawgrid()
    selectfield(actcell)
    
    #Keyboard zeichnen
    d_keys = {ch: 'white' for ch in abc[:26]}
    drawkeyboard()
    
    return

#
def addtosol(sol, key, actcell):
    '''
    Befüllt den dictionnary sol mit der aktuellen Lösung
    '''
    sol[xpos.index(actcell[0])] = key
    return sol

#Funktion zum checken der Eingabe
def checkchars(given, sol):
    #Kopie von hidden word und guess, da diese abgeändert werden müssen:
    giv = given.copy()
 
    #Zuerst alle die übereinstimmen
    for i,(ch_sol, ch_giv) in enumerate(zip(sol, giv)):
        if ch_sol != 0:
            if ch_sol == ch_giv:
                d_keys[ch_sol] = '#428D3E'
                colorguess(i, guessnbr, '#428D3E', sizerect, xpos, ypos)
                #hidden und guess verändern, dass diese Buchstaben nicht nochmals verwendet werden können
                giv[i] = 0
                sol[i] = 0
    #Danach check ob noch korrekte Buchtaben da sind
    done = False
    for i,(ch_sol, ch_giv) in enumerate(zip(sol, giv)):
        if ch_sol != 0:
            if ch_sol in giv:
                if d_keys[ch_sol] != '#428D3E':
                    d_keys[ch_sol] = '#FFFF00'
                colorguess(i, guessnbr, '#FFFF00', sizerect, xpos, ypos)
                #giv position auf 0 stellen wenn Eintrag vorhanden
                giv[giv.index(ch_sol)] = 0
                    
                #giv = [0 if ch_sol == value else value for value in giv]
            #Wenn verloren
            else:
                if d_keys[ch_sol] != '#428D3E' and d_keys[ch_sol] != '#FFFF00':
                    d_keys[ch_sol] = 'grey'
                colorguess(i, guessnbr, 'grey', sizerect, xpos, ypos)

@out.capture()
def checksol(sol):
    '''
    Checkt ob die eingegebene Lösung korrekt ist
    '''
    global actcell, guessnbr, gameOn
        #Prüfen ob 5 Buchstaben
    if len(sol) != wordlength:
        print('Keine gültige Eingabe')
        draw_error_screen(error_letters)
        return False
    if len(sol) == wordlength:
        #Prüfen ob die Buchstaben ein korrektes Wort sind
        sol = [sol[i] for i in range(wordlength)]
        if ''.join(sol) in words:
            # dict sol in Liste konvertieren
            
            print(given, sol, given == sol)
            if given == sol:
                #Lösche den Layer Actfield
                actfield.clear()
                
                #game ausschalten
                gameOn = False
                # nbrofguesses erhöhen
                guessnbr +=1
                endpage(True, 'lightgreen')
                return
            # Einfärben der Buchstaben
            checkchars(given, sol)
            
            #Einfärben des Keyboards:
            drawkeyboard()
            
            # nbrofguesses erhöhen
            guessnbr +=1
            # actcell umstellenm selectfield
            if guessnbr != nbrofguesses:
                actcell = (einzug, ypos[guessnbr])
                selectfield(actcell)
                return True
            else:
                #game ausschalten
                gameOn = False
                endpage(False, '#FF8F8F')
                return False
        else: 
            print('Wort nicht in Wortliste')
            draw_error_screen(error_wordlist)
            return False

#Distanz zu den Punkten auf dem Keyboard        
def distance(p, q):
    return ((p[0] - q[0])**2 + (p[1] - q[1])**2)**0.5

#Den nächsten Punkt herausfinden
def get_closest(pts, pt0, err=13):
    dist_idx = []
    for i, pt in enumerate(pts):
        dist = distance(pt, pt0)
        if dist < err:
            dist_idx.append((dist, i))
    
    return min(dist_idx, default=(None, None))[1]




#############################################################
###STEUERFUNKTIONEN
#############################################################

#Tastensteuerung
@out.capture(clear_output=True)
def on_key_down(key, *flags):
    '''
    Funktion um Keyboardeingaben auszuwerten
    '''
    global actcell, sol
    if key in abc:
        writekey(text, key.upper(), actcell)
        
    elif key == 'ArrowRight':
        moveactcellforward()

    elif key == 'ArrowLeft':
        moveactcellbackward()

    elif key == 'Backspace':
        deletekey(actcell)
        
    elif key == 'Enter':    
        #Wenn die Funktion True herausgibt lösche den dictionnary
        if checksol(sol):
            sol = {}

    elif key == '0': 
        newgame()
    else:
        return
        
#Maussteuerung
@out.capture(clear_output=True)
def on_mouse_down(x, y):
    global actcell
    idx = get_closest(pts, (x, y))
    if idx is not None:
        keyboard.selected_field = idx
        print(keyboard, idx, abc[idx])
        writekey(text,abc[idx], actcell, gameOn=True)
    
    
    if einzug < x < einzug+(wordlength*sizerect) and ypos[guessnbr] < y < ypos[guessnbr] + sizerect :
        #einzug < x < einzug+(wordlength*sizerect) and
        x = xpos[int((x-einzug)//sizerect)]
        y = ypos[int(((y-(y//sizerect)*zeilenabstand))//sizerect)]
        actcell = (x,y)
        selectfield(actcell)
    else:
        return

def on_click(bt_newgame):
    '''Wenn der Button newgame geklickt wird startet ein neues Spiel
    '''   
    newgame()
    mcanvas.focus()
                
#Maus und Keyboard überwachen
mcanvas.on_key_down(on_key_down)
mcanvas.on_mouse_down(on_mouse_down)
bt_newgame.on_click(on_click)

#Auswahlregler überwachen
select_wordlength.observe(on_change_select_wordlength, names='value')
select_nbrofguesses.observe(on_change_select_nbrofguesses, names='value')

display(hbox)
draw_welcome_screen()
# Audio in Schleiffe abspielen
play_audio_loop(mp3_file_path)
