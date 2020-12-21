from tkinter import *
from random import random, choice

class Tetris(Tk):

    # pour les mouvements je dois vérifier avant de faire pour
    #le cas droite si self.grille[lig][col-1] != 2 alors on bouge à droite self.grille[lig][col-1] = 1 pareilà gauche avec +1 pour col utiliser is not true est une autre possibilité
    #et il faut arrêter les mouvements des pièces à col-1 et col+1 en reprenant le principe de la ligne-1 du tick
    
    TAILLE_CASE = 40
    NBCOL = 10
    NBLIG = 15
    MARGE=80
    WIDTH = NBCOL*TAILLE_CASE
    HEIGHT = NBLIG*TAILLE_CASE
    VITESSE= 200

    S = [[[0,0,0,1,1],
      [0,0,1,1,0],
      [0,0,0,0,0],
      [0,0,0,0,0],
      [0,0,0,0,0]],
     [[0,0,0,0,0],
      [0,0,0,1,0],
      [0,0,0,1,1],
      [0,0,0,0,1],
      [0,0,0,0,0]]]

    Z =[[[0,0,1,1,0],
     [0,0,0,1,1],
     [0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0]],
    [[0,0,0,0,0],
     [0,0,0,1,0],
     [0,0,1,1,0],
     [0,0,1,0,0],
     [0,0,0,0,0]]]

    I = [[[0,0,0,1,0],
      [0,0,0,1,0],
      [0,0,0,1,0],
      [0,0,0,1,0],
      [0,0,0,0,0]],
     [[0,0,0,0,0],
      [0,1,1,1,1],
      [0,0,0,0,0],
      [0,0,0,0,0],
      [0,0,0,0,0]]]  

    O = [[[0,0,0,1,1],
      [0,0,0,1,1],
      [0,0,0,0,0],
      [0,0,0,0,0],
      [0,0,0,0,0]]]
     
    J = [[[0,0,1,0,0],
      [0,0,1,1,1],
      [0,0,0,0,0],
      [0,0,0,0,0],
      [0,0,0,0,0]],
     [[0,0,0,0,0],
      [0,0,1,1,0],
      [0,0,1,0,0],
      [0,0,1,0,0],
      [0,0,0,0,0]],
     [[0,0,0,0,0],
      [0,0,0,0,0],
      [0,0,1,1,1],
      [0,0,0,0,1],
      [0,0,0,0,0]],
     [[0,0,0,0,0],
      [0,0,0,1,0],
      [0,0,0,1,0],
      [0,0,1,1,0],
      [0,0,0,0,0]]]

    L = [[[0,0,0,0,1],
      [0,0,1,1,1],
      [0,0,0,0,0],
      [0,0,0,0,0],
      [0,0,0,0,0]],
     [[0,0,0,0,0],
     [0,0,0,1,0],
      [0,0,0,1,0],
      [0,0,0,1,1],
      [0,0,0,0,0]],
     [[0,0,0,0,0],
      [0,0,0,0,0],
      [0,0,1,1,1],
      [0,0,1,0,0],
      [0,0,0,0,0]],
     [[0,0,0,0,0],
      [0,0,0,1,1],
      [0,0,0,0,1],
      [0,0,0,0,1],
      
      [0,0,0,0,0]]]

    T = [[[0,0,0,1,0],
      [0,0,1,1,1],
      [0,0,0,0,0],
      [0,0,0,0,0],
      [0,0,0,0,0]],
     [[0,0,0,0,0],
      [0,0,1,0,0],
      [0,0,1,1,0],
      [0,0,1,0,0],
      [0,0,0,0,0]],
     [[0,0,0,0,0],
      [0,0,0,0,0],
      [0,1,1,1,0],
      [0,0,1,0,0],
      [0,0,0,0,0]],
     [[0,0,0,0,0],
      [0,0,1,0,0],
      [0,1,1,0,0],
      [0,0,1,0,0],
      [0,0,0,0,0]]]

    pieces = [S,Z,I,O,J,L,T]


    def __init__(self):
        Tk.__init__(self)
        self.title("Tetris")
        self.grille = None
        self.piece = Tetris.pieces[0]
        self.ori=0
        self.score = 0
        self.can = Canvas(self, width=Tetris.WIDTH+2*Tetris.MARGE, height=Tetris.HEIGHT+2*Tetris.MARGE,bg="white")
        self.can.pack()
        self.can.create_text(Tetris.WIDTH//2,Tetris.HEIGHT//2,text="Bienvenu sur mon tetris")
        Button(self,text="Jouer",command=self.initGrille).pack(side=LEFT)
        Button(self,text="Test",command=self.pieceTombe).pack(side=LEFT)
        Button(self,text="Quitter",command=self.quitter).pack()
        self.bind("<Left>", self.lateralgauche)
        self.bind("<Right>", self.lateraldroit)
        self.bind("<Up>", self.rotate)

    def quitter(self):
        self.quit()
        self.destroy()


    def indexBasPiece(self):
        res=4
        for ligne in self.piece[self.ori][::-1]:
            if any(ligne):return res
            res-=1
    
    def initGrille(self):
        self.can.delete(ALL)
        self.grille=[[0 for x in range(Tetris.NBCOL)] for x in range(Tetris.NBLIG)]
        #self.tirePiece()
        self.spawn()
        for ligne in range(Tetris.NBLIG+1):
            self.can.create_line(Tetris.MARGE,Tetris.MARGE+ligne*Tetris.TAILLE_CASE,Tetris.WIDTH+Tetris.MARGE,Tetris.MARGE+ligne*Tetris.TAILLE_CASE)
        for col in range(Tetris.NBCOL+1):
            self.can.create_line(Tetris.MARGE+col*Tetris.TAILLE_CASE,Tetris.MARGE,Tetris.MARGE+col*Tetris.TAILLE_CASE,Tetris.HEIGHT+Tetris.MARGE)
        self.fillGrille()
        self.tick()
        print(self.indexBasPiece())

    def fillGrille(self):
        self.can.delete('case')
        for lig in range(Tetris.NBLIG):
            for col in range(Tetris.NBCOL):
                if self.grille[lig][col] in (1,2) :self.drawCase(lig,col)

    @classmethod
    def coords(cls,lig,col):
        return (cls.MARGE+col*cls.TAILLE_CASE,cls.MARGE+lig*cls.TAILLE_CASE)

    def tirePiece(self):
        self.piece=choice(Tetris.pieces)
        self.ori=0

    def drawCase(self,lig,col,color="red"):
        (x1,y1)=self.coords(lig,col)
        (x2,y2)=(x1+Tetris.TAILLE_CASE,y1+Tetris.TAILLE_CASE)
        self.can.create_rectangle(x1,y1,x2,y2,fill=color,tag='case')
        
    def spawn(self):
        for i in range(0,5):
            self.grille[i][0:5]=self.piece[self.ori][i]

    def pieceTombe(self):
        for lig in range(Tetris.NBLIG)[::-1]:
            for col in range(Tetris.NBCOL):
                if self.grille[lig][col]==1:
                        self.grille[lig][col]=0
                        self.grille[lig+1][col]=1
        self.fillGrille()

    def isBlocked(self):
        if 1 in self.grille[-1]: return True
        for lig in range(Tetris.NBLIG-1):
            for col in range(Tetris.NBCOL):
                if self.grille[lig][col]==1 and self.grille[lig+1][col]==2:
                    return True
        return False

    #def isBlockedCol(self):
        #for i in range(Tetris.NBLIG)[::-1]:
            #if 1 in self.grille[i][1]: return True
            #if 1 in self.grille[i][-1]: return True

    def cantMovedroite(self):
        for lig in range(Tetris.NBLIG)[::-1]:
            for col in range(Tetris.NBCOL):
                if self.grille[lig][col]==1 and self.grille[lig][col+1]==2:
                    return True
        return False

    def cantMovegauche(self):
        for lig in range(Tetris.NBLIG)[::-1]:
            for col in range(Tetris.NBCOL):
                if self.grille[lig][col]==1 and (self.grille[lig][col-1]==2 or col==0):
                    return True
        return False

    def fini(self):
        if 2 in self.grille[3]:return True
        return False

    def tick(self):
        tick = self.after(Tetris.VITESSE, self.tick)
        if self.isBlocked() :
            for lig in range(Tetris.NBLIG):
                for col in range(Tetris.NBCOL):
                    if self.grille[lig][col]==1:self.grille[lig][col]=2
            if not self.fini():
                self.tirePiece()
                self.spawn()
        else:self.pieceTombe()

#mouvement à gauche
    def lateralgauche(self,event):
        if not self.cantMovegauche():
            for lig in range(Tetris.NBLIG)[::-1]:
                for col in range(Tetris.NBCOL):
                    if self.grille[lig][col]==1:
                        self.grille[lig][col]=0
                        self.grille[lig][col-1]=1

#mouvement à droite
    def lateraldroit(self,event):
        try:
            if not self.cantMovedroite():
                for lig in range(Tetris.NBLIG)[::-1]:
                    for col in range(Tetris.NBCOL)[::-1]:
                        if self.grille[lig][col]==1:
                            self.grille[lig][col]=0
                            self.grille[lig][col +1]=1
        except IndexError:
            pass # car on sera forcément en indexerror si on ne fais qu'aller à droite, donc ceci empêchera la console à avoir cette erreur

    def lignebrisee(self):
            for lig in range(Tetris.NBLIG)[::-1]:
                    for col in range(Tetris.NBCOL):
                        if 1 in all(self.grille[lig][col]):
                            self.grille[lig][col] = 0
                            self.score += 1

    def rotate(self,event):
        self.ori = (self.ori + 1) % len(self.piece)
        for lig in range(Tetris.NBLIG)[::-1]:
            for col in range(Tetris.NBCOL):
                if self.grille[lig][col] ==1:
                    self.grille[lig][col] =0
                    self.grille[lig][col] = self.piece[self.ori]
                    

#score = 1 ligne brisée = 1
#niveau si score = 5 on augmente self.VITESSE de 25
#pour les pieces je peux me servir d'un array dans lequel des le début de la chute de la première piece on posera dans la liste un spawn de piece, et on spawnera la piece de la liste lorsque la piece qui joue est en bas
    
if __name__=="__main__":
    Tetris().mainloop()
