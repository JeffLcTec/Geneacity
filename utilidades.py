import pygame
from arbol import *

jsons=[] #lista que almacena los jsons de la consulta del API
habitantes=[]
contadores = {'s': 1, 'w': 1, 'a': 1, 'd': 1} #Contadores usados para determinar la dirección y cual sprite colocar 

#sprites de animación del personaje
sprites = {
    's': ["sprites/2.png","sprites/2.png","sprites/2.png","sprites/2.png", "sprites/0.png","sprites/0.png","sprites/0.png","sprites/0.png", "sprites/2.png","sprites/2.png","sprites/2.png","sprites/2.png", "sprites/1.png","sprites/1.png","sprites/1.png","sprites/1.png"],
    'w': ["sprites/5.png","sprites/5.png","sprites/5.png","sprites/5.png", "sprites/3.png","sprites/3.png","sprites/3.png","sprites/3.png", "sprites/5.png","sprites/5.png","sprites/5.png","sprites/5.png", "sprites/4.png","sprites/4.png","sprites/4.png","sprites/4.png"], 
    'a': ["sprites/11.png","sprites/11.png","sprites/11.png","sprites/11.png", "sprites/9.png","sprites/9.png","sprites/9.png","sprites/9.png", "sprites/11.png","sprites/11.png","sprites/11.png","sprites/11.png", "sprites/10.png","sprites/10.png","sprites/10.png","sprites/10.png"],
    'd': ["sprites/8.png","sprites/8.png","sprites/8.png","sprites/8.png", "sprites/6.png","sprites/6.png","sprites/6.png","sprites/6.png", "sprites/8.png","sprites/8.png","sprites/8.png","sprites/8.png", "sprites/7.png","sprites/7.png","sprites/7.png","sprites/7.png"],
} 
skins=["imagenes_Proyecto3/personajes/p1.jpg","imagenes_Proyecto3/personajes/p2.jpg","imagenes_Proyecto3/personajes/p3.jpg","imagenes_Proyecto3/personajes/p4.jpg","imagenes_Proyecto3/personajes/p5.jpg"]
size = width, height =800, 800
screen = pygame.display.set_mode(size)

image = pygame.image.load("sprites/2.png").convert_alpha()  #variable con la imagen del personaje
image_rect = image.get_rect()
image_rect.center = (width // 2, height // 2)
casa_img = pygame.image.load("imagenes_Proyecto3/world/casa.png").convert_alpha() #imagen de la casa para optimizacion
casa_img = pygame.transform.scale(casa_img, (150, 150))
#posición x e y para colocar las imagenes del fondo y las casas (son las que hacen que las imagenes se muevan para dar el efecto de que es el personaje)
x=0
y=0

#posición x e y del jugador las cuales se necesitan para la consulta de las casas
jugadorx=width // 2
jugadory=height // 2
clock = pygame.time.Clock() 
speed = 25      

fondo= pygame.transform.scale(pygame.image.load("imagenes_Proyecto3/world/mundon.png"),(10000,10000)).convert_alpha()

tile_size = 1000  # tamaño de los mosaicos
tiles = []
for i in range(0, fondo.get_width(), tile_size):
    for j in range(0, fondo.get_height(), tile_size):
        tiles.append(fondo.subsurface((i, j, tile_size, tile_size)))
j_info_open=False
window_open= False
persona_info_open = False
esc_press=False
lockW=True
lockA=True
lockS=True
lockD=True

cont_casas=0
three_persona=ArbolGenealogico()
puntaje_max=1000
puntaje_actual=0
