import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
 

##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################
 
# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

# transforme une liste de liste Python en TBL numpy équivalent à un tableau 2D en C
def CreateArray(L):
   T = np.array(L, dtype=np.int32)
   T = T.transpose()  ## ainsi,  on peut écrire TBL[x][y]
   return T

TBL = CreateArray([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 2, 2, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
# attention,  on utilise TBL[x][y] 
        
HAUTEUR = TBL.shape [1]      
LARGEUR = TBL.shape [0]  

# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
   GUM = np.zeros(TBL.shape, dtype=np.int32)
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            GUM[x][y] = 1
   return GUM
            
GUM = PlacementsGUM()

# création de la carte des distance
def CreateDistanceMap():
   distanceMap = np.zeros(GUM.shape, dtype=np.int64)
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1):
            distanceMap[x][y] = 1000
         elif (GUM[x][y] == 1):
            distanceMap[x][y] = 0
         else:
            distanceMap[x][y] = 100
   return distanceMap

DISTANCEMAP = CreateDistanceMap()

# création de la carte des distances des fantômes
def createGhostMap():
   ghostMap = np.zeros(TBL.shape, dtype=np.int64)
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if TBL[x][y] == 0:
            ghostMap[x][y] = 100
         else:
            ghostMap[x][y] = 1000
   return ghostMap

GHOSTSMAP = createGhostMap()

# Stats PacMan
score = 0            # Score
PacManPos = [5, 5]   # Position de PacMan
SuperPacMan = 0      # Temps de bonus de PacMan
superpacgums ={      # Position des super pacgommmes
(1, 1), (1, 9), (18, 1), (18, 9)}

# Ghost[x, y, color, direction(x,y)]
Ghosts  = []
Ghosts.append(  [8,  5 ,   "pink"  , (0 , 1)] )
Ghosts.append(  [9,  5 ,   "orange", (0 , 1)] )
Ghosts.append(  [10, 5 ,   "cyan"  , (0 , 1)] )
Ghosts.append(  [11, 5 ,   "red"   , (0 , 1)] )


##############################################################################
#
#  Debug : ne pas toucher (affichage des valeurs autours dans les cases

LTBL = 100
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]


# info peut etre une valeur / un string vide / un string...
def SetInfo1(x, y, info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL1[x][y] = info
   
def SetInfo2(x, y, info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL2[x][y] = info
   


##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################



ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR+1) * ZOOM  
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("ESIEE - PACMAN by Antonin and Zackary :v")


# gestion de la pause

PAUSE_FLAG = False
LOST_FLAG = False
WIN_FLAG = False

# On passe en pause/dé-pause si la barre d'espace est appuyée
def keydown(e):
   global PAUSE_FLAG
   if e.char == ' ' : 
      PAUSE_FLAG = not PAUSE_FLAG 
 
Window.bind("<KeyPress>",  keydown)


# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top",  fill="both",  expand=True)
F.grid_rowconfigure(0,  weight=1)
F.grid_columnconfigure(0,  weight=1)


# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0,  column=0,  sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
    
def WindowAnim():
    PlayOneTurn()
    Window.after(333, WindowAnim)

Window.after(100, WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial',  size=22,  weight="bold",  slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1,  width = screeenWidth,  height = screenHeight )
canvas.place(x=0, y=0)
canvas.configure(background='black')
 
 
#  FNT AFFICHAGE


def To(coord):
   return coord * ZOOM + ZOOM 
   
# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5, 10, 15, 10, 5]


def Affiche(PacmanColor, message):
   global anim_bouche
   global SuperPacMan
   global anim_blink

   if SuperPacMan > 0:
      PacmanColor = "#39FF15"
   
   def CreateCircle(x, y, r, coul):
      canvas.create_oval(x-r, y-r, x+r, y+r,  fill=coul,  width  = 0)
   
   canvas.delete("all")
      
      
   # murs
   
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx, yy, xxx, yy, width = EPAISS, fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x) 
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx, yy, xx, yyy, width = EPAISS, fill="blue")

   # pacgums
   global superpacgums

   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[x][y] == 1):
            xx = To(x) 
            yy = To(y)
            e = 5
            color = "orange"
            if (x,y) in superpacgums: # s'il s'agit d'une superpacgum, on lui donne une autre taille et couleur
               e = 12
               color = "white"
            canvas.create_oval(xx-e, yy-e, xx+e, yy+e, fill=color)
            
   #extra info
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) 
         yy = To(y) - 11
         txt = TBL1[x][y]
         canvas.create_text(xx, yy,  text = txt,  fill ="white",  font=("Purisa",  8)) 
         
   #extra info 2
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) + 10
         yy = To(y) 
         txt = TBL2[x][y]
         canvas.create_text(xx, yy,  text = txt,  fill ="yellow",  font=("Purisa",  8)) 
         
  
   # dessine pacman
   xx = To(PacManPos[0]) 
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche]
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e, yy-e,  xx+e, yy+e,  fill = PacmanColor)
   canvas.create_polygon(xx, yy, xx+e, yy+ouv_bouche, xx+e, yy-ouv_bouche,  fill="black")  # bouche
   
  
   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0]) 
      yy = To(P[1])
      e = 16
      
      coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx, dec+yy-e+6, e, coul)
      canvas.create_rectangle(dec+xx-e, dec+yy-e, dec+xx+e+1, dec+yy+e,  fill=coul,  width  = 0)
      
      # oeil gauche
      CreateCircle(dec+xx-7, dec+yy-8, 5, "white")
      CreateCircle(dec+xx-7, dec+yy-8, 3, "black")
       
      # oeil droit
      CreateCircle(dec+xx+7, dec+yy-8, 5, "white")
      CreateCircle(dec+xx+7, dec+yy-8, 3, "black")
      
      dec += 3
      
   # texte  
   global LOST_FLAG
   global WIN_FLAG
   
   if LOST_FLAG:
      canvas.create_text(screeenWidth // 2,  screenHeight- 50 ,  text = "GAME OVER",  fill ="yellow",  font = PoliceTexte)
   elif WIN_FLAG:
      canvas.create_text(screeenWidth // 2,  screenHeight- 50 ,  text = "YOU WIN!",  fill ="yellow",  font = PoliceTexte)
   else:
      canvas.create_text(screeenWidth // 2,  screenHeight- 50 ,  text = "PAUSE : PRESS SPACE",  fill ="yellow",  font = PoliceTexte)

   canvas.create_text(screeenWidth // 2,  screenHeight- 20 ,  text = message,  fill ="yellow",  font = PoliceTexte)

 
AfficherPage(0)
            
#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################

      
def PacManPossibleMove():
   L = []
   x, y = PacManPos
   if ( TBL[x  ][y-1] == 0 ): L.append((0, -1))
   if ( TBL[x  ][y+1] == 0 ): L.append((0,  1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1, 0))
   if ( TBL[x-1][y  ] == 0 ): L.append((-1, 0))
   return L


def GhostsPossibleMove(x, y):
   L = []

   # Si on est dans le spawn des fantomes, on peut s'y balader ou en sortir
   if ( TBL[x  ][y  ] == 2 ):
      if ( TBL[x  ][y-1] != 1 ): L.append((0, -1))
      if ( TBL[x  ][y+1] != 1 ): L.append((0,  1))
      if ( TBL[x+1][y  ] != 1 ): L.append(( 1, 0))
      if ( TBL[x-1][y  ] != 1 ): L.append((-1, 0))
   
   # En dehors du spawn, on n'en rentre pas à nouveau
   else:
      if ( TBL[x  ][y-1] == 0 ): L.append((0, -1))
      if ( TBL[x  ][y+1] == 0 ): L.append((0,  1))
      if ( TBL[x+1][y  ] == 0 ): L.append(( 1, 0))
      if ( TBL[x-1][y  ] == 0 ): L.append((-1, 0))

   return L

def detectCorridor(possibleMove):
   # On vérifie qu'il n'y a que deux déplacements possibles
   if len(possibleMove) !=2:
      return False
   else:
      # On vérifie que ces déplacements sont de direction opposée (leur somme doit faire 0)
      if (possibleMove[0][0] + possibleMove[1][0] == 0 and possibleMove[0][1] + possibleMove[1][1] == 0):
         return True
      return False


def IAPacman():
   global PacManPos,  Ghosts, SuperPacMan
   # deplacement Pacman
   (x, y) = PacManPos

   # carte des fantomes
   ghostCases =  [
      [x, y-1, GHOSTSMAP[x][y-1]],
      [x-1, y, GHOSTSMAP[x-1][y]],
      [x, y+1, GHOSTSMAP[x][y+1]],
      [x+1, y, GHOSTSMAP[x+1][y]],
   ]

   # carte des gommes
   gumCases =  [
      [x, y-1, DISTANCEMAP[x][y-1]],
      [x-1, y, DISTANCEMAP[x-1][y]],
      [x, y+1, DISTANCEMAP[x][y+1]],
      [x+1, y, DISTANCEMAP[x+1][y]],
   ]

   # décrémenter le temps restant de bonus à chaque tour
   if (SuperPacMan > 0):
      SuperPacMan -= 1

   # mode chasse aux fantomes (s'il y a assez de bonus et qu'il existe des fantomes sur la map)
   neightborDistance = np.array([neightborCase[2] for neightborCase in ghostCases])
   if (SuperPacMan > 2 and np.min(neightborDistance) < 99):
      index = np.argmin(neightborDistance)

   # mode recherche de gommes
   elif GHOSTSMAP[x][y] > 3:
      neightborDistance = np.array([neightborCase[2] for neightborCase in gumCases])
      index = np.argmin(neightborDistance)

   # mode fuite
   else:
      neightborDistance = []
      for ghostCase in ghostCases:
         if not np.equal(ghostCase[2], 1000):
            neightborDistance.append(ghostCase[2])
         else:
            neightborDistance.append(-1)

      neightborDistance = np.array(neightborDistance)
      index = np.argmax(neightborDistance)
   PacManPos[0] = ghostCases[index][0]
   PacManPos[1] = ghostCases[index][1]

def IAGhosts():
   # deplacement Fantome
   for F in Ghosts:
      # On génère la liste des déplacements possibles
      L = GhostsPossibleMove(F[0], F[1])
      
      # S'il s'agit d'un couloir, on retire la case précédente à la liste des déplacements possibles
      if (detectCorridor(L)):
         previousTile = (-F[3][0],-F[3][1])
         if (previousTile in L):
            L.remove(previousTile)

      # On choisit une direction au hasard parmi les déplacements possibles et on l'applique
      choix = random.randrange(len(L))
      F[0] += L[choix][0]
      F[1] += L[choix][1] 

      # On set la direction choisie
      F[3] = (L[choix][0], L[choix][1])


def killGhost(ghost):
   global score
   score += 2000
   ghost[0] = random.randint(8, 11)
   ghost[1] = 5

# TODO : à commenter
def updateDistanceMap():
   SaveDISTANCE = np.array(0)
   while not np.array_equal(SaveDISTANCE, DISTANCEMAP):
      SaveDISTANCE = np.copy(DISTANCEMAP)
      for x in range(1, DISTANCEMAP.shape[0]-1):
         for y in range(1, DISTANCEMAP.shape[1]-1):
            if (DISTANCEMAP[x][y] != 1000 and DISTANCEMAP[x][y] != 0):
               neightborCases =  [
                  DISTANCEMAP[x][y-1],
                  DISTANCEMAP[x-1][y],
                  DISTANCEMAP[x][y+1],
                  DISTANCEMAP[x+1][y],
               ]
               DISTANCEMAP[x][y] = min(neightborCases) + 1

# TODO : à commenter
def updateGhostMap():
   SaveDISTANCE = np.array(0)
   while not np.array_equal(SaveDISTANCE, GHOSTSMAP):
      SaveDISTANCE = np.copy(GHOSTSMAP)
      for x in range(1, GHOSTSMAP.shape[0]-1):
         for y in range(1, GHOSTSMAP.shape[1]-1):
            if [x, y] in [[ghost[0], ghost[1]] for ghost in Ghosts if Ghosts] and not np.equal(GHOSTSMAP[x][y],1000 ):
               GHOSTSMAP[x][y] = 0
            elif not np.equal(GHOSTSMAP[x][y], 1000):
               neightborCases =  [
                  GHOSTSMAP[x][y-1],
                  GHOSTSMAP[x-1][y],
                  GHOSTSMAP[x][y+1],
                  GHOSTSMAP[x+1][y],
               ]
               min_neighbor = min(neightborCases)
               if not np.equal(min_neighbor, 100):
                  GHOSTSMAP[x][y] = min_neighbor + 1


def eatPacGum():
   global score
   global superpacgums
   global SuperPacMan

   # si il y a une gomme à la position de pacman, on la retire
   x, y = PacManPos[0], PacManPos[1]
   if GUM[x][y] == 1:
      GUM[x][y] = 0
      DISTANCEMAP[x][y] = 100
      # Super Pac Gomme : On donne 23 secondes de bonus et + 500 score
      if (x,y) in superpacgums:
         score += 500
         SuperPacMan = 23
      # Pac Gomme : + 100 score
      else:
         score += 100
      updateDistanceMap()

# Renvoie le fantome s'il y a une collision avec, None sinon
def detectCollision():
   for F in Ghosts:
      if PacManPos == [F[0],F[1]]:
         return F
   return None
      

#  Boucle principale de votre jeu appelée toutes les 500ms

iteration = 0
def PlayOneTurn():
   global SuperPacMan
   global iteration
   global PAUSE_FLAG
   global LOST_FLAG
   global WIN_FLAG

   # Debug
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         # SetInfo1(x, y, DISTANCEMAP[x][y])
         # SetInfo2(x, y, GHOSTSMAP[x][y])
         pass
   
   # Le jeu alterène les cours de pacman et des fantomes s'il n'y est ni en pause, ni gagné ou perdu
   if not PAUSE_FLAG and not LOST_FLAG and not WIN_FLAG : 
      iteration += 1
      if iteration % 2 == 0 :   IAPacman()
      else:                     IAGhosts()

      # En cas de collision avec un fantôme...
      ghost = detectCollision()
      if(ghost != None):
         # On tue le fantome si on est en mode Super
         if SuperPacMan > 0:
            killGhost(ghost)
         # On meurt sinon
         else:
            LOST_FLAG = True
      eatPacGum()
      updateGhostMap()

      # On finit la partie si toutes les gommes ont étées mangées
      WIN_FLAG = not np.any(GUM == 1)


   Affiche(PacmanColor = "yellow",  message = f"score : {score}")  
 
 
###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()