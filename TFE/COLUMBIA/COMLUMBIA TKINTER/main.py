

#                                          TRAVAIL DE FIN D'ETUDES
#_______________________________Coding  by IFriee//Eliott Wengler_______________________________________________
#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_--_-_-_-_-_-_-_-_-_-_-__-_-_-_-_-_-_-_-_-_-_-__-_-_-_-_-_-_-_-_-_-_-_*


#-------------------------------------LES IMPORTS DE MODULES----------------------------------------
from tkinter import *
import os
import sqlite3
import random
import winsound

import PIL
import qrcode
from tkinter import messagebox

#from .GIFANIMATED import *


# --------------------------------connection sqlite base de donnée---------------------------------------------

conn = sqlite3.connect('basededonnee.db')


#--------------------------------------------------GIF---------------------------------------------------------
class GifAnimatedLabel(Label): #~copié collé d'internet
    """Label containing a GIF animated image

    Args:
        master: the master Widget for this GifAnimatedLabel
        filename: the file name contaning the GIF image
        speed: the delay in millisecond between each frame
    """

    def __init__(self, master, filename, speed, *args, **kwargs):
        self.speed = speed
        self.frames = []
        i = 0
        while True:
            try:
                p = PhotoImage(file=filename, format="gif - {}".format(i))
            except TclError:
                break
            self.frames.append(p)
            i += 1

        super().__init__(master, image=self.frames[0], *args, **kwargs)
        self.frame_idx = 0
        self.num_frames = i
        self.after(self.speed, self._animate)

    def _animate(self):
        self.frame_idx = (self.frame_idx + 1) % self.num_frames
        self['image'] = self.frames[self.frame_idx]
        self.after(self.speed, self._animate)

#------------------------------------------------Autre DEF---------------------------------------------------------


def return_valeur(cursor, row): # return la liste du scoreboard
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn.row_factory = return_valeur#row_factory change la table en dictionnaire

cursor = conn.cursor()

def msgerreur():
    #https://docs.python.org/fr/3/library/tkinter.messagebox.html
    pass

#--------------------------------------------------def DATA BASE------------------------------------------------------

def modif_portefeuilles(ID, montant):
    cursor.execute('''SELECT * FROM users WHERE ID = {}'''.format(ID))
    user = cursor.fetchone()  # execute une requete sql et envois 1 resultat
    # user["porte_feuilles"]  #cherhce le montant du portefeuille de l'utilisateur

    if user["porte_feuilles"] + montant <0:#si le contenu du porte feuille est plus petit que 0 , erreur

        return False



    cursor.execute(
        '''UPDATE users SET porte_feuilles = {} WHERE ID = {} '''.format(user["porte_feuilles"] + montant,ID))
    conn.commit()

    return True

def login(Login, Mdp):
    cursor.execute('''SELECT * FROM users WHERE pseudo = '{}' AND mdp = '{}' '''.format(Login, Mdp))
    user = cursor.fetchone()  # execute une requete sql et envoit 1 resultat

    return user

def getuser(user_ID):#renvois les donnée de l'user pour l'afficher par apres

    cursor.execute('''SELECT * FROM users WHERE ID = {}'''.format(user_ID))
    user = cursor.fetchone()  # execute une requete sql et envoit 1 resultat

    return user


def comptecreation(nom, mdp, mdp2):

    if mdp == mdp2:

        try:  # si erreur , on va pouvoir les afficher
            cursor.execute('''INSERT INTO users(
               pseudo, mdp) VALUES 
               ('{}','{}')'''.format(nom, mdp))  # prend le text et insert le nom et mdp dans accolade
            conn.commit()
            messagebox.showinfo('Success', 'Votre compte à bien été crée')
        except Exception as E:  # si execute lance une erreur , on affiche l'erreur
            messagebox.showerror('Error','Une erreur est survenue')
            print(E)


def scoreboard(ID_users,gains,multiplicateur):
    cursor.execute('''INSERT INTO scores(ID_users,gains,multiplicateur) VALUES 
                   ({},{},{})'''.format(ID_users,gains,multiplicateur))  # prend le text et insert le nom et mdp dans accolade
    conn.commit()

def recup_score():
    cursor.execute('''SELECT * FROM users join scores s on users.ID = s.ID_users
    ORDER BY S.gains DESC LIMIT 5''')
    return cursor.fetchall()#renvoit la liste de résultats

"""def recuphistorique(ID_users,gains,multiplicateur): #futur page historique

    cursor.execute('''SELECT * FROM users join scores s on users.ID = s.ID_users
        ORDER BY S.gains DESC LIMIT 50''')
    return cursor.fetchall()  # renvoit la liste de l'historique du joueur"""



#--------------------------------------------------def JEU------------------------------------------------------

def game(user_ID):
    for c in root.winfo_children():
        c.destroy()

    winsound.PlaySound(None, winsound.SND_ASYNC)



    user = getuser(user_ID)

    jumped=False

    multiplicateur = 1.00
    multiplicateur_MAX = random.uniform(1, 5)

    def boucle1mili():

        nonlocal multiplicateur  # donne la possibilité de modif le multiplicateur
        multiplicateur = multiplicateur + 0.001
        print(multiplicateur)
        multiplicateur_TEXT["text"] = "{:.2f}".format(multiplicateur)#"{:.2f}" = juste 2 décimales apres la virgule

        if multiplicateur <= multiplicateur_MAX and not jumped:#si le multiplicateur est plus petit ou egale que le multiplicateur max ET n'as pas encore sauté
            root.after(7, boucle1mili)  # execute la fonction boucle toute les millisecondes

        else:
            btnBET['text'] = 'BET'
            btnBET['command'] = start  # click et new Def

            if multiplicateur >= multiplicateur_MAX:#si il a perdu

                winsound.PlaySound("sources\explosion.wav", winsound.SND_ASYNC)
                labelexplosion.image=img_explosion
                labellaunch.pack_forget()
                labelexplosion.pack(side=LEFT, fill="x", expand=False)




    BGRIGHT = PhotoImage(file="sources\gameright.png")

    labelRIGHT = Label(root, image=BGRIGHT, bg="#282828")
    labelRIGHT.image = BGRIGHT  # Association de l image au widget
    labelRIGHT.pack(side=RIGHT)


    # ---------------IMAGE DU JEU-------------------

    img_WAITING = PhotoImage(file="sources\WAITING.png")
    labelLEFT = Label(root, image=img_WAITING, bg="#241F2B", anchor=W)
    labelLEFT.image = img_WAITING  # Association de l image au widget
    labelLEFT.pack(side=LEFT, fill="x", expand=False)

    img_explosion = PhotoImage(file="sources\BOOM.png")
    labelexplosion = Label(root, image=img_explosion, bg="#282828")
    
    
    labellaunch = GifAnimatedLabel(root, bg="#241F2B", anchor=W,
                                 filename="sources\GIF_LAUCHER_REPEAR.gif",
                                 speed=100)

    labeleject = GifAnimatedLabel(root, bg="#241F2B", anchor=W,
                                   filename="sources\EJECTGIFREPEAR.gif",
                                   speed=100)

    # ------------------------BOUTONS ET TEXTES--------------------------

    Mise=StringVar()#pour faire un text entry

    mise = Entry(root, textvariable=Mise, font=("American Captain", 10), bg="White",
                                    fg="black", width=17, border=2)
    mise.place(x=1055,y=630)

    #--SCORE--

    list_score=recup_score()

    for index,i in enumerate(list_score):   #pour chaque score dans la liste:------index =tour de boucle

        bestpseudo = Label(root, text=i["pseudo"], font=("American Captain", 20), bg="#282828", fg="#95C4FB")
        bestpseudo.place(x=920, y=150+index*35) #index *30 == la succession de la liste

        bestmultiplicateur = Label(root, text=str("{:.2f}".format(i["multiplicateur"])), font=("American Captain", 20), bg="#282828", fg="#95C4FB")
        bestmultiplicateur.place(x=1080, y=150+index*35)

        bestgains = Label(root, text=str("{:.2f}".format(i["gains"])), font=("American Captain", 20), bg="#282828", fg="#95C4FB")
        bestgains.place(x=1216, y=150+index*35)


    multiplicateur_TEXT = Label(root, text="", font=("IMPACT", 40), bg="#241F2B", fg="White")
    multiplicateur_TEXT.place(x=380, y=50)

    collect = Label(root, text="coming soon", font=("Arial", 9), bg="white", fg="black")
    collect.place(x=1050, y=517)




    pseudolabel = Label(root, text="Pseudo                   Porte-feuilles", font=("American Captain",15),bg="#282828", fg="#FD8A2D")
    pseudolabel.place(x=1015, y=385)


    userlabel = Label(root, text=user["pseudo"], font=("American Captain", 20), bg="#282828", fg="white")
    userlabel.place(x=1015,y=415)

    moneylabel = Label(root, text=str("{:.2f}".format(user["porte_feuilles"])), font=("American Captain", 20),
                      bg="#282828", fg="white")
    moneylabel.place(x=1125,y=415)

    def Jump():



        labellaunch.pack_forget()#retire l'ancienne image

        labeleject.pack(side=LEFT, fill="x", expand=False)


        btnBET['text'] = 'BET'
        btnBET['command'] = start  # click and new Def
        nonlocal jumped
        jumped = True

        gain_multi = multiplicateur*float(Mise.get())#on stock dans la variable le montant gagné

        scoreboard(user_ID, gain_multi, multiplicateur)

        modif_portefeuilles(user_ID,gain_multi)

        nonlocal user#met à jour le portefeuille
        user = getuser(user_ID)

        moneylabel['text'] = str("{:.2f}".format(user["porte_feuilles"]))




    def start():

        hasmoney=modif_portefeuilles(user_ID,-float(Mise.get())) #débite x euros du compte lorsqu'il appuie sur BET

        winsound.PlaySound("sources\LAUNCHMUSIC.wav", winsound.SND_ASYNC) #modifier mp3 en wav , demarrer la musique plus tard et modifier le volume car trop fort

        nonlocal user
        user = getuser(user_ID)

        if hasmoney:
            btnBET['text'] = 'Sauter'  # change le texte du btn BET
            btnBET['command'] = Jump  # click and new Def

            nonlocal jumped  # nonlocal )= modif une variable definie en dehors de la fonction
            jumped = False
            nonlocal multiplicateur_MAX
            multiplicateur_MAX = random.uniform(1, 5)

            moneylabel['text'] = str("{:.2f}".format(user["porte_feuilles"]))

            nonlocal multiplicateur  # donne la possibilité de modif le multi (je pense)
            multiplicateur = 1

            labelLEFT.pack_forget()  # cache l'image
            labeleject.pack_forget()
            labellaunch.pack(side=LEFT, fill="x", expand=False)
            labelexplosion.pack_forget()


            boucle1mili()


    def playgame():                                                             #erreur

        winsound.PlaySound(None, winsound.SND_ASYNC)


    btnBET = Button(root, text="BET", font=("Nasalization", 30),width=6,height=1, bg="#FD8A2D", fg="#241F2B",activebackground='#FD8A2D',
                    border=0, command=lambda: start())
    btnBET.place(x=1025, y=560)

    btnretour = Button(root, text="Retour", font=("American Captain", 15), bg="#FD8A2D", fg="#241F2B", width=6,
                       border=0, command=windows_menu)
    btnretour.place(x=1300, y=15)

    btnmusic = Button(root, text="Mute", font=("American Captain", 15), bg="#FD8A2D", fg="#241F2B", width=6,
                      border=0,command=playgame)
    btnmusic.place(x=1300, y=70)

    btnhistorique = Button(root, text="Historique", font=("American Captain", 12), bg="#95C4FB", fg="#241F2B", width=9,
                      border=0, command=Historique)
    btnhistorique.place(x=1075,y=700)


#--------------------------------------------------------MENU------------------------------------------------------


def Historique():
    # creation fenetre
    win_historique = Toplevel()
    win_historique.geometry("1000x330")
    win_historique.title("Historique de jeu")
    win_historique.iconbitmap("sources\ICON.ico")
    win_historique.config(bg="#241F2B")
    win_historique.resizable(height=False, width=False)

    img = qrcode.make('http://www.ifosupwavre.be/')#tuto de graven
    img.save('qrcode.png')
    imgqr = PhotoImage(file="qrcode.png")
    labelLEFT = Label(win_historique, image=imgqr, bg="#241F2B", anchor=W)
    labelLEFT.image = imgqr  # Association de l image au widget
    labelLEFT.pack(side=RIGHT, fill="x", expand=True)

    btnretour = Button(win_historique, text="Retour", font=("American Captain", 20), bg="#FD8A2D", fg="#241F2B",
                       width=6,
                       border=0, command=win_historique.destroy)
    btnretour.place(x=600, y=200)

    text = Label(win_historique, text="Dans un futur lointain, \ril y aura l'historique des parties du joueur sur un site, \r mais pour le moment le qr code generé par python \r vous emènes sur le site de l'ifosup ", font=("Comic sans MS", 15), bg="#241F2B", fg="white",
                       border=0)
    text.place(x=400, y=50)






def reglement_window():
    # _____Permet de changer de page sans changer de fenetre (detruit les widget de l'ancienne)
    for c in root.winfo_children():
        c.destroy()

        # root.config(bg="#241F2B")

        # BACKGROUND + REGLES
        imgBG = PhotoImage(file="sources\REGLEDUJEU.png")
        canvas = Canvas()
        canvas.create_image(imgBG.width() / 2, imgBG.height() / 2, image=imgBG)
        labell = Label(root, image=imgBG)
        labell.image = imgBG  # Association de l image au widget
        labell.pack()
        canvas.image = imgBG  # Association de l image au canva.
        canvas.pack()

    frame_reglement = Frame(root, bg="#95C4FB")
    text_commentjouer = Label(frame_reglement, text="Comment y jouer ?", font=("American Captain", 50), bg="#95C4FB",
                              fg="#241F2B")
    text_commentjouer.pack()
    btn_retour = Button(frame_reglement, text="Retour", font=("American Captain", 20), bg="#FCA627", fg="#241F2B",
                        width=25, border=0, command=windows_menu)
    btn_retour.pack()
    frame_reglement.place(x=470, y=25)



def framecreecompte(frame_connection, win_connection):
    frame_connection.destroy()#detruit la frame connection

    # CREE UN COMPTE FRAME
    # frame menu connection pseudo mdp

    pseudo = StringVar()  # objet lié au champ de texte et cela contient la valeur inscrite et relier au textvariable dans les Entry
    Mdp = StringVar()
    Mdp2 = StringVar()

    frame_creecompte = Frame(win_connection, bg="#241F2B")
    connection_text = Label(frame_creecompte, text="Cree un compte", font=("American Captain", 50), bg="#241F2B",
                            fg="#95C4FB")
    connection_text.grid(row=0, column=1)
    Pseudo = Label(frame_creecompte, text="Pseudo: ", font=("American Captain", 20), bg="#241F2B", fg="white", border=0)
    Pseudo.grid(row=1, column=0)
    global pseudo_creecompte_entry
    pseudo_creecompte_entry = Entry(frame_creecompte, textvariable=pseudo, font=("Comic Sans MS", 20), bg="White",fg="black", width=25,border=0)
    pseudo_creecompte_entry.grid(row=1, column=1)

    # ajout d'un espace
    espace = Label(frame_creecompte, text="", bg="#241F2B", height=1)
    espace.grid(row=2, column=0)

    # '''''''''''''''''''
    mdp = Label(frame_creecompte, text="Mot de passe:                  ", font=("American Captain", 20), bg="#241F2B",
                fg="white", border=0)
    mdp.grid(row=4, column=0)

    # ajout d'un espace
    espace = Label(frame_creecompte, text="", bg="#241F2B", height=1)
    espace.grid(row=5, column=0)

    mdp2 = Label(frame_creecompte, text="Confirmer le MDP:         ", font=("American Captain", 20), bg="#241F2B",
                 fg="white", border=0)
    mdp2.grid(row=6, column=0)
    global mdp_creecompte_entry
    mdp_creecompte_entry = Entry(frame_creecompte, textvariable=Mdp, font=("Comic Sans MS", 20), bg="White",
                                 fg="black", width=25,
                                 border=0,show="*")
    mdp_creecompte_entry.grid(row=4, column=1)
    global mdp2_creecompte_entry
    mdp2_creecompte_entry = Entry(frame_creecompte, textvariable=Mdp2, font=("Comic Sans MS", 20), bg="White",
                                  fg="black", width=25,
                                  border=0,show="*")
    mdp2_creecompte_entry.grid(row=6, column=1)

    # ajout d'un espace
    espace = Label(frame_creecompte, text="", bg="#241F2B", height=1)
    espace.grid(row=6, column=0)

    # ajout d'un espace
    espace = Label(frame_creecompte, text="", bg="#241F2B", height=1)
    espace.grid(row=7, column=0)

    # Bouton crée compte
    def retour_connection():#detruit la fenetre et reouvre une autre (car la frame connection a ete detruite et je ne sais pas comment la faire reapparaitre
        win_connection.destroy()
        connection_window()


    creecompte_retour = Button(frame_creecompte, text="Retour", font=("American Captain", 20),
                                      bg="#FCA627", fg="#241F2B", width=15, border=0,
                                      command=retour_connection)
    creecompte_retour.grid(row=7, column=0)

    creecompte_connection_bt = Button(frame_creecompte, text="Cree mon compte", font=("American Captain", 20),
                                      bg="#FCA627", fg="#241F2B", width=25, border=0,
                                      command=lambda: comptecreation(pseudo.get(), Mdp.get(), Mdp2.get()))
    creecompte_connection_bt.grid(row=7, column=1)
    frame_creecompte.pack(expand=YES)






# fenetre conection
def connection_window():
    # creation fenetre
    win_connection = Toplevel()
    win_connection.geometry("600x340")
    win_connection.title("Connection")
    win_connection.iconbitmap("sources\ICON.ico")
    win_connection.config(bg="#241F2B")
    win_connection.resizable(height=False, width=False)

    # frame menu connection pseudo mdp

    frame_connection = Frame(win_connection, bg="#241F2B")

    Login = StringVar()
    Mdp = StringVar()

    connection_text = Label(frame_connection, text="Se connecter", font=("American Captain", 50), bg="#241F2B",
                            fg="#95C4FB")
    connection_text.grid(row=0, column=1)
    Pseudo = Label(frame_connection, text="Pseudo: ", font=("American Captain", 20), bg="#241F2B", fg="white", border=0)
    Pseudo.grid(row=1, column=0)
    global pseudo_entry
    pseudo_entry = Entry(frame_connection, font=("Comic Sans MS", 20), textvariable=Login, bg="White", fg="black",
                         width=25, border=0)
    pseudo_entry.grid(row=1, column=1)

    # ajout d'un espace
    espace = Label(frame_connection, text="", bg="#241F2B", height=1)
    espace.grid(row=2, column=0)

    # '''''''''''''''''''
    mdp = Label(frame_connection, text="Mot de passe:                  ", font=("American Captain", 20), bg="#241F2B",
                fg="white", border=0,)
    mdp.grid(row=4, column=0)
    global mdp_entry
    mdp_entry = Entry(frame_connection, font=("Comic Sans MS", 20), textvariable=Mdp, bg="White", fg="black",
                      width=25, border=0,show="*")
    mdp_entry.grid(row=4, column=1)


    # ajout d'un espace
    espace = Label(frame_connection, text="", bg="#241F2B", height=1)
    espace.grid(row=5, column=0)

    # Bouton Login
    def Log(): # login regarde si utilisateur et lance le jeu
        user=login(Login.get(), Mdp.get()) #stock les données dans une variable
        if user:
            messagebox.showinfo('Success','Vous etes bien connecté, bon jeu !!')
            game(user["ID"])

        else:
            messagebox.showerror('Error','Une erreur est survenue')




    Login_connection_bt = Button(frame_connection, text="Login", font=("American Captain", 20), bg="#FCA627",
                                 fg="#241F2B", width=25, border=0, command=Log)
    Login_connection_bt.grid(row=6, column=1)

    # ajout d'un espace
    espace = Label(frame_connection, text="", bg="#241F2B", height=1)
    espace.grid(row=6, column=0)
    # ajout d'un espace
    espace = Label(frame_connection, text="Pas encore de compte?", font="Helvetica", bg="#241F2B", fg="white", height=1)
    espace.grid(row=7, column=1)

    # Bouton crée un compte

    creecompte_bt = Button(frame_connection, text="Cree un compte", font=("American Captain", 20), bg="#FCA627",
                           fg="#241F2B", width=25, border=0,
                           command=lambda: framecreecompte(frame_connection, win_connection))
    creecompte_bt.grid(row=8, column=1)
    frame_connection.pack(expand=YES)




def windows_menu():
    for c in root.winfo_children():
        c.destroy()

    # root.config(bg="#241F2B")

    winsound.PlaySound(None, winsound.SND_PURGE)

    winsound.PlaySound('sources\musicmenu.wav', winsound.SND_ASYNC)
    # ------image de fond

    imgBG = PhotoImage(file="sources\MENU PRINCIPAL.png")
    canvas = Canvas()
    canvas.create_image(imgBG.width() / 2, imgBG.height() / 2, image=imgBG)
    labell = Label(root, image=imgBG)
    labell.image = imgBG  # Association de l image au widget
    labell.pack()
    canvas.image = imgBG  # Association de l image au canva.
    canvas.pack()
    # ------cree une frame (boite)
    frame_menu = Frame(root, bg="#241F2B")

    # ------Menu text
    '''''menu_text = Label(frame_menu, text="MENU", font=("American Captain",50), bg="#241F2B", fg="#FCA627")
    menu_text.pack()'''''

    # ------Bouton menu cliquable
    # --connection
    bt_connection = Button(frame_menu, text="Connection", font=("American Captain", 40), bg="White", fg="#241F2B",
                           border=0, command=connection_window)
    bt_connection.pack()

    # ---Regles du jeu
    bt_regle = Button(frame_menu, text="Regle du jeu", font=("American Captain", 40), bg="#241F2B", fg="White",
                      border=0, command=reglement_window)
    bt_regle.pack(pady=0)

    # ---Option
    bt_Option = Button(frame_menu, text="=test=", font=("American Captain", 40), bg="#241F2B", fg="White", border=0,
                       command=lambda :game(user_ID=4))
    bt_Option.pack()

    # --Quitter
    bt_quitter = Button(frame_menu, text="Quitter", font=("American Captain", 40), bg="#241F2B", fg="White", border=0,
                        command=root.quit)
    bt_quitter.pack()

    # ------boite du menu position et affichage
    frame_menu.place(x=700, y=250)

    # ------image de font ((((J'ai trouvé mieux !!!)
    """can_imgfont = Canvas(app,width=1366, height=768,bg="#241F2B")
    imgfont = PhotoImage(file="F:\PHYTON CODE\TFE\COLUMBIA\COMLUMBIA TKINTER\sources\MENU PRINCIPAL.png")
    can_imgfont.create_image(0,0, anchor=NW, image=imgfont)
    can_imgfont.place(x=0,y=100)"""

root = Tk()
root.geometry("1366x768")
root.title("Columbia")
root.iconbitmap("sources\ICON.ico")
root.resizable(height=False, width=False)

# ------image de font
img_bg = PhotoImage(file="sources\PRESS_START.png")
label = Label(root, image=img_bg)
label.pack()

pressstart = Button(root, text="Commencer", font=("American Captain", 40), bg="#DCD5C3", fg="#FD8A2D", border=7,
                    relief=RAISED, activebackground="#FD8A2D", command=windows_menu)
pressstart.place(x=565, y=650)

root.mainloop()
