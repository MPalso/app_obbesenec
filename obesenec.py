#importujem si modul pythonu tkinter ktory zabezpecuje zobrazenie plochy
import tkinter
#importujem si modul random, ktory zabezpeci vyber nahody
import random
#importujem si modul time, ktory mi zabezpecuje to, ze aplikacia pocka urcite sekundy po ukonceni hry a nasledne skonci,
#teda zavrie okno
import time

#vykreslim si okno hry
canvas = tkinter.Canvas(width=640, height=480)
canvas.pack()

#vykreslim sibenicu v okne hry
def nakresli_sibenica(x, y):
    sibenica = x, y, x, y-40, x-100, y-40, x-100, y+160
    canvas.create_line(sibenica, width=5)
    canvas.create_line(x-150, y+160, x-50, y+160, width=15)

#vykreslim obesenca pod sibenicou, ale nezobrazim (HIDDEN) jeho casti, ktore sa budu zobrazovat az na zaklade stavu hry
def obesenec(x, y):
    hlava = canvas.create_oval(x - 20, y, x + 20, y + 40, width=3, state=tkinter.HIDDEN)
    trup = canvas.create_line(x, y + 40, x, y + 90, width=3, state=tkinter.HIDDEN)
    lavar = canvas.create_line(x - 40, y + 60, x, y + 60, width=3, state=tkinter.HIDDEN)
    pravar = canvas.create_line(x + 40, y + 60, x, y + 60, width=3, state=tkinter.HIDDEN)
    lavan = canvas.create_line(x, y + 90, x - 30, y + 130, width=3, state=tkinter.HIDDEN)
    pravan = canvas.create_line(x, y + 90, x + 30, y + 130, width=3, state=tkinter.HIDDEN)
    return hlava, trup, lavar, pravar, lavan, pravan

#vykreslim pismena ale tiez ich schovam pred zaciatkom hry
def nakresli_pismena(pismena):
    start = 320 - 20*len(pismena)
    
#zabezpecenie aby v pripade viacerych slov medzi ktorymi je medzera bola tato medzera nezobrazovana ako znak
    pismeno_ids = {pismeno:[] for pismeno in pismena if pismeno != " "}
    for pismeno in pismena:
        if pismeno == " ":
            start += 40
            continue
        canvas.create_line(start+5, 100, start+35, 100, width=2)
        idx = canvas.create_text(start+20, 85, text=pismeno.upper(), font="arial 30", state=tkinter.HIDDEN)
        pismeno_ids[pismeno].append(idx)
        start += 40
    return pismeno_ids

def nahraj_slovo(file_name):
    with open(file_name, "r") as fp:
        zoznam_slov = fp.read().splitlines()
    nahodne_slovo  = random.choice(zoznam_slov)
    return nahodne_slovo

def dopln_pismeno(pismeno_ids, zoznam_hadanych_pismen):
    for pismeno, ids in pismeno_ids.items():
        if pismeno in zoznam_hadanych_pismen:
            for idx in ids:
                canvas.itemconfig(idx, state=tkinter.NORMAL)

def dopln_obesenca(zle_zvolene_pismeno, obesenec_ids):
    for i in range(0, zle_zvolene_pismeno):
        canvas.itemconfig(obesenec_ids[i], state=tkinter.NORMAL)

def dobre_pismeno(pismeno):
    zoznam_hadanych_pismen.append(pismeno)
    dopln_pismeno(pismeno_ids, zoznam_hadanych_pismen)
    
def zle_pismeno(pismeno):
    global zle_zvolene_pismeno
    zoznam_hadanych_pismen.append(pismeno)
    zle_zvolene_pismeno +=1
    dopln_obesenca(zle_zvolene_pismeno,obesenec_ids)

def je_vytaz(pismeno_ids, zoznam_hadanych_pismen):
    for pismeno in pismeno_ids:
        if pismeno not in zoznam_hadanych_pismen:
            return False
    return True

def check_hra():
    global hra
    if je_vytaz(pismeno_ids, zoznam_hadanych_pismen):
        hra = "vyhra"
    elif zle_zvolene_pismeno > 5:
            hra = "prehral"
            
def koniec_hry(stav_hry):
    if stav_hry == "vyhra":
        canvas.create_text(300, 240, text="GRATULUJEM", font="arial 60", fill="RED")
    else:
        canvas.create_text(300, 240, text="PREHRAL SI", font="arial 60", fill="RED")

    canvas.update()
    time.sleep(3)


nakresli_sibenica(300,240)
obesenec_ids = obesenec(300, 240)
slovo = nahraj_slovo("zoznam_slov.txt")
pismeno_ids = nakresli_pismena(slovo)
hra = "hra ide" 
zoznam_hadanych_pismen = []
zle_zvolene_pismeno = 0

while hra == "hra ide":
    zvolene_pismeno = input("napis pismeno: ")
    if zvolene_pismeno in zoznam_hadanych_pismen:
        continue
    elif zvolene_pismeno in pismeno_ids:

        dobre_pismeno(zvolene_pismeno)
    else:

        zle_pismeno(zvolene_pismeno)


    check_hra()
    canvas.update()

koniec_hry(hra)

