# CM7: INTERFACES : codes

from tkinter import * 
# def main():
#     fenetre = Tk()
#     fenetre.geometry("500x300+70+70")
#     label = Label(fenetre, text="cours de Python")
#     bouton = Button(fenetre, text="Quitter", fg="red", command=fenetre.destroy)
#     button2 = Button(fenetre, text="Click me")
#     button2.pack(side=LEFT, fill=BOTH)

#     label.pack()
#     bouton.pack() 
#     fenetre.mainloop()
# if __name__ == '__main__': 
#     main()

from tkinter import *
class Fenetre(Tk):
    def __init__(self,l=300,h=200):
        Tk.__init__(self)
        ecran_x = self.winfo_screenwidth()
        ecran_y = self.winfo_screenheight()
        pos_x = ecran_x // 2 - l // 2
        pos_y = ecran_y // 2 - h // 2
        geometrie = f"{l}x{h}+{pos_x}+{pos_y}"
        self.geometry(geometrie)
    #     self.title("Tests")
    #     self.create_label()
    #     self.create_boutons()
    #     print(self.label_welcome.cget("text"))

    # def create_label(self):
    #     self.label_welcome = Label(self,text="Bienvenue")
    #     self.label_welcome.pack()

    # def create_boutons(self):
    #     bouton_quitter = Button(self, text ='Quitter', command = self.destroy)
    #     bouton_quitter.pack()
    #     Button(self,text="Modif label",command=self.modif_label).pack()
    
    # def modif_label(self):
    #     self.label_welcome.config(text="Bienvenue modifiée")
    #     print(self.label_welcome.cget("text"))

        # CANVAS
        self.ca = Canvas()
        self.ca.create_line(10, 10, 10, 200, 200, 200, 120,120,fill="blue")
        self.ca.create_line(10, 10, 10, 200, 200, 200, smooth=1, fill="red")
        self.ca.create_rectangle(300, 100, 60, 120, fill="green", width=2)
        self.ca.create_text(100, 10, text="Exemple de Canevas", fill="red")
        points = [150, 100, 200, 120, 240, 180, 210,200, 150, 150]
        self.ca.create_polygon(points, outline='black',fill='blue', width=23)
        self.ca.pack()




        # self.creation_menus()

#menus
    def creation_menus(self):
        menu_principal = Menu(self)
        premier_menu = Menu(menu_principal,tearoff=0)
        premier_menu.add_command(label="etudiants")
        premier_menu.add_command(label="enseignants")
        premier_menu.add_command(label="personnels")
        premier_menu.add_command(label="quitter",command=self.quit)
        deuxieme_menu = Menu(menu_principal,tearoff=0)
        deuxieme_menu.add_command(label="notes")
        deuxieme_menu.add_command(label="median")
        deuxieme_menu.add_command(label="final")
        deuxieme_menu.add_command(label="fenêtre",command=self.creer_fenetre)
        menu_principal.add_cascade(label="Premier",menu=premier_menu)
        menu_principal.add_cascade(label="Deuxième",menu=deuxieme_menu)
        self.config(menu=menu_principal)
    def creer_fenetre(self):
        nouvelle_fenetre = Toplevel(self)
        nouvelle_fenetre.title("New")
        Label(nouvelle_fenetre,text="Nouvelle Fenêtre").pack()


        




#eg: Entry()
class Fenetre2(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Test entrée')
        self.label_valider = Label (self, text="") # label de la chaîne de validation
        self.label_valider.pack()
        self.entree = Entry (self)
        self.entree.pack()
        self.entree.focus_set()
        
        bouton_quitter = Button (self, text=' Quitter ',command=self.quit)
        bouton_quitter.pack()
        bouton_valider = Button (self, text=' Valider ',command=self.valider)
        bouton_valider.pack()
        
    def valider(self):
        chaine = "Voici l'entrée : " + self.entree.get()
        self.label_valider.config(text=chaine)
        self.initialiser()

    def initialiser(self):
        self.entree.delete(0, END)
        self.entree.focus()

# eg: intvar, check/radio buttons
# class Fenetre(Tk):
#     def __init__(self,l=300,h=200):
#         Tk.__init__(self)
#         ecran_x = self.winfo_screenwidth()
#         ecran_y = self.winfo_screenheight()
#         pos_x = ecran_x // 2 - l // 2
#         pos_y = ecran_y // 2 - h // 2
#         geometrie = "{}x{}+{}+{}".format(l, h, pos_x, pos_y)
#         self.geometry(geometrie)
#         self.title("Test StringVar")
#         Label(text="Test bouton click + StringVar").pack()
#         Button(self, text ='Quitter', command = self.destroy).pack()
#         self.value = IntVar()
#         Checkbutton(self, text="ok", variable=self.value, offvalue=0, onvalue=1,
#         command=self.valider_entree).pack()
#         Radiobutton(self, variable=self.value, text="voiture", value=3, 
#         command=self.valider_entree).pack()
#         Radiobutton(self, variable=self.value, text="vélo", value=4, 
#         command=self.valider_entree).pack()
#     def valider_entree(self):
#         Label(self, text=str(self.value.get())).pack()
#         print(self.value.get())


ma_fenetre = Fenetre()
ma_fenetre.mainloop()