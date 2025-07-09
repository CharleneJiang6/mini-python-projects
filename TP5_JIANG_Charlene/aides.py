# les opérations doivent fonctionner aec 2 elmt (si +elm idgaf) #with getter/setter
# historique : ds une liste d'opérations ouo une liste de float/str
# class Operation:
#     def __init__(self, op1, op2, symbol) -> None:
#         pass
    
#     def calc(self):
# AFFICHAGE historique :
# opération 1 : 3*5=bla
# ----------2 : 4+2            

#no need same design, just need need right placement et even size button

# PLACEMENT DES ELMT
# .pack()   : place les elm a la suite des autres
# .grid()
# .place(x,y)  useless

#no need properties for TP5
import tkinter as tk
class Calc(tk.Tk):
    # def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
    #     super().__init__(screenName, baseName, className, useTk, sync, use)

    def __init__(self):
       super().__init__()
    
# 1 : creer des COMPOSANTS : ts les labels, entrées, puis bouton : Label(self), Entry(self), Button(self)
    a)text : cte
    b)textvariable 
    c) command [pr button]

self._resultat = tk.floatvar()

# button(self, command=fonction_to_callback)
# command à excuter apres cliquer sur le boutton

widget.grid(row=    , column=    , rowspan=    , columnspan=  2 (l'elm est plus petit qu'une colonne, va pas s'étendre sur la 2e col), 
            sticky=coller sur quel coté [N,E,S,West]    si je fais "EW" je l'étend pr que ca colle a droite et a gauche,
            ipadding =   etc) #esthetiq optionnel



command = lambda : self.button_number_clicked(1)