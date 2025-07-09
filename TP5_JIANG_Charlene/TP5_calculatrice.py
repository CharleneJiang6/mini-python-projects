from tkinter import *


class Calculatrice(Tk   ) :
    def __init__(self, l=200, h=300) -> None:
        super().__init__()
        ecran_x = self.winfo_screenwidth()
        ecran_y = self.winfo_screenheight()
        pos_x = ecran_x // 2 - l // 2
        pos_y = ecran_y // 2 - h // 2
        geometrie = f"{l}x{h}+{pos_x}+{pos_y}"
        self.geometry(geometrie)

        self.title('Calculatrice')        
        
        zone_affichage=Label(self, text='').grid(row = 0, column = 0, columnspan = 4)

        #boutons
        self.creer_bouton()

        bouton_virgule=Button(self, text='.')
        bouton_clear=Button(self, text='clear')
        bouton_historique=Button(self, text='historique')
        bouton_sin=Button(self, text='sin')
        bouton_cos=Button(self, text='cos')
        bouton_tan=Button(self, text='tan')
        bouton_pi=Button(self, text='π')
        bouton_pi_au_carre=(self, text='π²')
        




    
    #operations
    def additionner (self, arg1, arg2):
        return int(arg1)+int(arg2)
    
    def soustraire(self, arg1, arg2):
        return int(arg1)-int(arg2)

    def multiplier(self, arg1, arg2):
        return int(arg1)*int(arg2)
    
    def diviser(self, arg1, arg2):
        return int(arg1)-int(arg2)
    


    








def main():
    calculatrice = Calculatrice()
    calculatrice.mainloop()