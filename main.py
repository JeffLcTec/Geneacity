import pygame
import sys
from PIL import *
from utilidades import *
from API_request import geneacity_API_request as API
import random

# Inicializa Pygame
pygame.init()

# Configuración de la ventana
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Geneacity")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Bucle principal del juego
def personas_disponibles():
    disponibles = API("https://geneacity.life/API/getAvailableInhabitants/?x=60000&y=60000")
    return disponibles.json

def personajes(id):
    personita = API(f"https://geneacity.life/API/selectAvailableInhabitant/?id={id}")
    return personita.json

personajes_disponibles = personas_disponibles()
personas = []
rects = []
images = []

ventana_x = 50
ventana_y = 50

for p in personajes_disponibles["inhabitants"]:
    if p["name"] not in personas:
        personas.append(p)

# Cargar imágenes y crear rectángulos una vez
for e in personas:
    img = random.choice(skins)
    character_image = pygame.transform.scale(pygame.image.load(img).convert_alpha(), (100, 100))
    images.append(character_image)
    character_rect = character_image.get_rect(topleft=(ventana_x, ventana_y - 20))
    rects.append((character_rect, e))  # Guardar rectángulo y nombre del personaje

    ventana_x += 150
    if ventana_x > 650:
        ventana_x = 50
        ventana_y += 150  # Incrementa más para dejar espacio para el texto

def handle_character_click(character_name):
    import prueba 
    """jugador = API(f"https://geneacity.life/API/selectAvailableInhabitant/?id={'4491'}")"""
    prueba.game({'id': '4491', 'name': 'Daniela', 'gender': 'Female', 'age': '28'})# Aquí puedes llamar a la función que quieras para el personaje clickeado

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for rect, name in rects:
                if rect.collidepoint(mouse_pos):
                    handle_character_click(name)



    # Redibujar personajes y sus ventanas
    for i, (rect, name) in enumerate(rects):
        character_image = images[i]
        screen.blit(character_image, rect.topleft)
        window_rect = pygame.Rect(rect.x, rect.y + 130, 100, 30)
        pygame.draw.rect(screen, NEGRO, window_rect)
        font = pygame.font.Font(None, 36)
        text = font.render(str(name["name"]), True, BLANCO)
        screen.blit(text, (rect.x + 5, rect.y + 110))  # Ajusta la posición del texto

    # Actualizar la pantalla
    pygame.display.flip()
