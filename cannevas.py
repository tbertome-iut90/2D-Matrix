##Modules
import sys
import pygame
import numpy as np
import math

##Initialisation des couleurs
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

#-----------------Conditions initiales (au tout début du jeu)---------------
#------------------------------À COMPLÉTER----------------------------------

global t
t=0

   
#booleens de clavier
global keyup,keydown,keyright,keyleft,keyspace, keyplus, keyminus, keyz, keyq, keys, keyd, mouseButton
keyup,keydown,keyright,keyleft,keyspace,keyplus,keyminus,keyz,keyq,keys,keyd,mouseButton=False,False,False,False,False,False,False,False,False,False,False,False


# booleens gestion du jeu 
start = False

##Fenêtre
pygame.init()
screen = pygame.display.set_mode((1600,1000))

#Temps
clock = pygame.time.Clock()

# ===== DESSIN ===== #

def dessin(P,A,color):
  for ligne in range(len(P[0])-1):
    for colonne in range(ligne+1,len(P[0])):
      if A[ligne][colonne]:
        pygame.draw.line(screen,color,(P[0][ligne],P[1][ligne]),(P[0][colonne],P[1][colonne]),1)

# ===== TRANSFORMATIONS ===== #

def zoom(P,rapport,x,y,z):
  P = translation(P,-x,-y,-z)
  P *= rapport
  P = translation(P,x,y,z)
  return P

def translation(P,x,y,z):
  for col in range(len(P[0])):
    P[0][col] += x
    P[1][col] += y
    P[2][col] += z
  return P


def rotateX(P, angle, x , y, z):
  s = np.sin(np.radians(angle))
  c = np.cos(np.radians(angle))
  P = translation(P,-x,-y,-z)
  R = np.array([[1,0,0],
                [0,c,-s],
                [0,s,c]])
  P = np.dot(R,P)
  P = translation(P,x,y,z)
  return P

def rotateY(P, angle, x , y, z):
  s = np.sin(np.radians(angle))
  c = np.cos(np.radians(angle))
  P = translation(P,-x,-y,-z)
  R = np.array([[c,0,s],
                [0,1,0],
                [-s,0,c]])
  P = np.dot(R,P)
  P = translation(P,x,y,z)
  return P

def rotateZ(P, angle, x , y, z):
  s = np.sin(np.radians(angle))
  c = np.cos(np.radians(angle))
  P = translation(P,-x,-y,-z)
  R = np.array([[c,-s,0],
                [s,c,0],
                [0,0,1]])
  P = np.dot(R,P)
  P = translation(P,x,y,z)
  return P

def rotation(P, x, y, z, angle):
  P = translation(P, -800, -500, 0)
  s = np.sin(np.radians(angle))
  c = np.cos(np.radians(angle))
  R = np.array([[c + x**2*(1-c), x*y*(1-c)-z*s, x*z*(1-c)+y*s],
                [y*x*(1-c)+z*s, c + y**2*(1-c), y*z*(1-c)-x*s],
                [z*x*(1-c)-y*s, z*y*(1-c)+x*s, c + z**2*(1-c)]])
  P = np.dot(R, P)
  P = translation(P, 800, 500, 0)
  return P

# ===== CUBE ===== #

P_CUBE = np.array([[-1,-1,-1,-1,1,1,1,1],
                   [-1,-1,1,1,-1,-1,1,1],
                   [-1,1,-1,1,-1,1,-1,1]])

A_CUBE = np.array([[False]*8]*8)

for i in range(8):
  for j in range(i+1,8):
    distance = (P_CUBE[0][i]-P_CUBE[0][j])**2+(P_CUBE[1][i]-P_CUBE[1][j])**2+(P_CUBE[2][i]-P_CUBE[2][j])**2
    if distance == 4:
      A_CUBE[i][j] = True
      A_CUBE[j][i] = True

P_CUBE = zoom(P_CUBE,200, 0, 0, 0)
P_CUBE = translation(P_CUBE,800,500,0)
P_CUBE = rotateX(P_CUBE,30,800,500,0)
P_CUBE = rotateY(P_CUBE,30,800,500,0)

# ===== ICOZAEDRE ===== #

phi = (1+np.sqrt(5))/2

P_ICO = np.array([[phi,-phi,phi,-phi,1,1,-1,-1,0,0,0,0],
                  [1,1,-1,-1,0,0,0,0,phi,-phi,phi,-phi],
                  [0,0,0,0,phi,-phi,phi,-phi,1,1,-1,-1]])

A_ICO = np.array([[False]*12]*12)

for i in range(12):
  for j in range(i+1,12):
    distance = (P_ICO[0][i]-P_ICO[0][j])**2+(P_ICO[1][i]-P_ICO[1][j])**2+(P_ICO[2][i]-P_ICO[2][j])**2
    if distance <= 4:
      A_ICO[i][j] = True
      A_ICO[j][i] = True

P_ICO = zoom(P_ICO,50, 0, 0, 0)
P_ICO = translation(P_ICO,800,500,0)
P_ICO = rotateX(P_ICO,30,800,500,0)
P_ICO = rotateY(P_ICO,30,800,500,0)

# ===== DODÉCAÈDRE ===== #

P_DOD = np.array([[0,0,0,0,1/phi,-1/phi,1/phi,-1/phi,phi,-phi,phi,-phi,1,1,1,1,-1,-1,-1,-1],
                  [1/phi,-1/phi,1/phi,-1/phi,phi,phi,-phi,-phi,0,0,0,0,1,1,-1,-1,1,1,-1,-1],
                  [phi,phi,-phi,-phi,0,0,0,0,1/phi,1/phi,-1/phi,-1/phi,1,-1,1,-1,1,-1,1,-1]])

A_DOD = np.array([[False] * 20] * 20)

for i in range(20):
    for j in range(i + 1, 20):
        distance = (P_DOD[0, i] - P_DOD[0, j]) ** 2 + (P_DOD[1, i] - P_DOD[1, j]) ** 2 + (P_DOD[2, i] - P_DOD[2, j]) ** 2
        if distance <= 3:
            A_DOD[i, j] = True
            A_DOD[j, i] = True

P_DOD = zoom(P_DOD, 50, 0, 0, 0)
P_DOD = translation(P_DOD, 800, 500, 0)

# ===== COLLINE ===== #

def generate_2D_image(f, x_min, x_max, points):
  if points%2 != 0:
    points += 1
  n = (x_max - x_min)/(points - 1)
  P = np.array([[0.0] * points] * 3)
  for i in range(points):
    P[0, i] = x_min + i * n
    P[1, i] = f(P[0, i])

  A = np.array([[False] * points] * points)

  for i in range(points):
     for j in range(points):
        distance_x = abs(P[0, i] - P[0, j])
        if distance_x <= n + n/10 and distance_x > 0:
          A[i, j] = True
  return P, A

def f(x):
  return np.cos(x**2)

def to_3D(P_COL, A_COL, x, y, z, n):
  P_COL = translation(P_COL, -x, -y, -z)
  angle = 180/(n+1)

  NEW_P_COL = P_COL
  NEW_A_COL = np.array([[False] * (len(A_COL[0]) * (n+1))] * (len(A_COL[0]) * (n+1)))

  for k in range(1,n+1):
    P_COL = rotateY(P_COL, angle, 0, 0, 0)
    NEW_P_COL = np.concatenate((NEW_P_COL, P_COL), axis=1)

  for k in range(n+1):
    for i in range(len(A_COL[0])):
      for j in range(len(A_COL[0])):
        if A_COL[i, j]:
          NEW_A_COL[i + len(A_COL[0])*k, j + len(A_COL[0])*k] = True

  for k in range(n+2):
    for i in range(len(A_COL[0])):
      NEW_A_COL[(i + len(A_COL[0])*k)%len(NEW_A_COL[0]), (i + len(A_COL[0])*(k+1))%len(NEW_A_COL[0])] = True
  for i in range(len(A_COL[0])):
    NEW_A_COL[i, len(NEW_A_COL)-1-i] = True

  return NEW_P_COL, NEW_A_COL

P_COL, A_COL = generate_2D_image(f, -10, 10, 50)
NEW_P_COL = np.array([[0.0] * len(P_COL[0])*2] * 3)
NEW_A_COL = np.array([[False] * len(NEW_P_COL[0])*2] * len(NEW_P_COL[0])*2)
NEW_P_COL, NEW_A_COL = to_3D(P_COL, A_COL, 0, 0, 0, 10)
NEW_P_COL = zoom(NEW_P_COL, 50, 0, 0, 0)
NEW_P_COL = translation(NEW_P_COL, 800, 500, 0)
NEW_P_COL = rotateZ(NEW_P_COL, -45, 800, 500, 0)
NEW_P_COL = rotateY(NEW_P_COL, 30, 800, 500, 0)

##Boucle principale
while True:
    #Gestion du temps
    clock.tick(60)
    t+=1/60

    #Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
              keyspace=True
            if event.key == pygame.K_UP:
              keyup=True
            if event.key == pygame.K_DOWN:
              keydown=True
            if event.key == pygame.K_RIGHT:
              keyright=True
            if event.key == pygame.K_LEFT:
              keyleft=True
            if event.key == pygame.K_KP_PLUS:
              keyplus=True
            if event.key == pygame.K_KP_MINUS:
              keyminus=True
            if event.key == pygame.K_z:
              keyz=True
            if event.key == pygame.K_q:
              keyq=True
            if event.key == pygame.K_s: 
              keys=True
            if event.key == pygame.K_d:
              keyd=True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseButton = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
              keyspace=False
            if event.key == pygame.K_UP:
              keyup=False
            if event.key == pygame.K_DOWN:
              keydown=False
            if event.key == pygame.K_RIGHT:
              keyright=False
            if event.key == pygame.K_LEFT:
              keyleft=False
            if event.key == pygame.K_KP_PLUS:
              keyplus=False
            if event.key == pygame.K_KP_MINUS:
              keyminus=False
            if event.key == pygame.K_z:
              keyz=False
            if event.key == pygame.K_q:
              keyq=False
            if event.key == pygame.K_s:
              keys=False
            if event.key == pygame.K_d:
              keyd=False
            if event.key == pygame.MOUSEBUTTONUP:
              mouseButton = False
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseButton = False

              
    #Clearscreen
    screen.fill(BLACK)

    #Create text and text rectangle
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('To start press space', True, WHITE, BLACK)
    textRect = text.get_rect()
    textRect.center = (800, 500)


#----------------------- Jeu -----------------------------

    #Démarrage
    if not start:
        t = 0
        #Affichage du texte
        screen.blit(text, textRect)      
    
    if keyspace and not start:
        start = True
    
    if start:
      if mouseButton:
        pos = pygame.mouse.get_pos()
        # Récupérer le vecteur de déplacement de la souris depuis le dernier appel
        # Calculer le vecteur perpendiculaire à ce vecteur de déplacement passant par le centre de l'écran
        # Calculer l'angle de rotation à partir de ce vecteur
        # Appliquer la rotation à la figure
      if keyup:
        NEW_P_COL = rotateX(NEW_P_COL,2,800,500,0)
      if keydown:
        NEW_P_COL = rotateX(NEW_P_COL,-2,800,500,0)
      if keyright:
        NEW_P_COL = rotateY(NEW_P_COL,2,800,500,0)
      if keyleft:
        NEW_P_COL = rotateY(NEW_P_COL,-2,800,500,0)
      if keyplus:
        NEW_P_COL = zoom(NEW_P_COL,1.02,800,500,0)
      if keyminus:
        NEW_P_COL = zoom(NEW_P_COL,0.98,800,500,0)
      if keyz:
        NEW_P_COL = translation(NEW_P_COL,0,2,0)
      if keys:
        NEW_P_COL = translation(NEW_P_COL,0,-2,0)
      if keyq:
        NEW_P_COL = translation(NEW_P_COL,2,0,0)
      if keyd:
        NEW_P_COL = translation(NEW_P_COL,-2,0,0)
      dessin(NEW_P_COL,NEW_A_COL,GREEN)
      # dessin(P_ICO,A_ICO,RED)

    #Mise à  jour de l'écran
    pygame.display.update()