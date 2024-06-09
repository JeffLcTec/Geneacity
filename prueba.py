import pygame,sys
from API_request import geneacity_API_request
from utilidades import *
import random
from arbol import *
from PIL import *
import sys

def nueva_partida(ventana_menu: tk.Tk):
    ventana_menu.destroy()
    seleccionar_personaje()

def cargar_partida():
    pass


def seleccionar_personaje():
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
        disponibles = geneacity_API_request("https://geneacity.life/API/getAvailableInhabitants/?x=80000&y=80000")
        return disponibles.json

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
        jugador = geneacity_API_request(f"https://geneacity.life/API/selectAvailableInhabitant/?id=7076")
        game({'id': '7076', 'name': 'Berenjena', 'gender': 'Female', 'age': '26', 'marital_status': 'Single', 'alive': 'Alive', 'father': '4178', 'mother': '7066', 'house': '4112'})# Aquí puedes llamar a la función que quieras para el personaje clickeado

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

def buscar_parentezco(jugador,persona):
    arbol_j=three
    arbol_p= arbol_persona(persona)
    puntuacion= buscar_similitud(jugador,persona,arbol_j,arbol_p)

    return puntuacion
def arbol_persona(persona):
    three_persona.agregar_nodo(Persona(persona["id"],persona["name"]))
    if persona["father"] and persona["mother"]:
        padre=info_persona(info_persona(persona["id"])["father"])
        madre=info_persona(info_persona(persona["id"])["mother"])
        familiares=[three_persona.agregar_nodo(Persona(padre["id"], padre["name"])),three_persona.agregar_nodo(Persona(madre["id"], madre["name"]))]
        three_persona.establecer_padre(persona["id"],padre["id"])
        three_persona.establecer_madre(persona["id"],madre["id"]) 
        pass
        
    else:
        pass
    return three_persona
def arbol_jugador(persona, three):
    if persona["id"] not in three.personas:
        three.agregar_nodo(Nodo(persona["id"], persona["name"]))

    if persona["father"] and persona["mother"]:
        padre_id = persona["father"]
        madre_id = persona["mother"]

        if padre_id not in three.memo:
            padre = info_persona(padre_id)
            three.memo[padre_id] = padre
        else:
            padre = three.memo[padre_id]

        if madre_id not in three.memo:
            madre = info_persona(madre_id)
            three.memo[madre_id] = madre
        else:
            madre = three.memo[madre_id]

        if padre_id not in three.personas:
            three.agregar_nodo(Nodo(padre["id"], padre["name"]))
        if madre_id not in three.personas:
            three.agregar_nodo(Nodo(madre["id"], madre["name"]))

        three.establecer_padre(persona["id"], padre["id"])
        three.establecer_madre(persona["id"], madre["id"])

        arbol_jugador(padre, three)
        arbol_jugador(madre, three)

    return three
    
def ver_familia(three,Ver):
    global screen_width
    if Ver==True:
        ventana = tk.Tk()
        ventana.title("Árbol Genealógico")
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
        ventana.geometry(f"{screen_width}x{screen_height}+0+0")
        canvas = tk.Canvas(ventana, width=screen_width, height=screen_height, bg='lightblue')
        canvas.pack()
        three.dibujar_arbol(canvas)
        ventana.mainloop()
 
def imagen(contadores, imagen, direccion):
    """Función encargada de mover y generar la animación de movimiento del personaje

    Args:
        contadores (_type_): contador usado para determinar cual sprite colocar
        imagen (_type_): imagen del  sprite del personaje
        direccion (_type_): hacia que dirección se mueve el personaje

    """
    if direccion in contadores:
        contadores[direccion] += 1
        if contadores[direccion] > 16:
            contadores[direccion] = 1

        imagen = pygame.image.load(sprites[direccion][contadores[direccion] - 1]).convert_alpha()
        return contadores[direccion], imagen
def habitantest():
    habitantes_totales= geneacity_API_request("https://geneacity.life/API/getAvailableInhabitants/?x=10000&y=10000")    
    return habitantes_totales.json["inhabitants"]
def info_persona(id):

    respuesta= geneacity_API_request(f"https://geneacity.life/API/getInhabitantInformation/?id={id}")   #funcion en proceso
    return respuesta.json['inhabitant']
def Info_casas(lista,x,y):
    """FUncion para realizar consultas al API de las personas de las casas
    
    Args:
        lista (list): lista que almacena las casas.
        x (int): posición x de la casa.
        y (int): posición y de la casa.
         
           """
    for casas in lista:
        for casa in casas['houses']:
            if int(casa['x'])==x and int(casa['y'])==y: #verifica si la x,y de cada casa es igual a la enviada
                id = casa['id']
                lista_habitantes=geneacity_API_request(f"https://geneacity.life/API/getHousesResidents/?houseId={id}")
                try:    
                    return(lista_habitantes.json['residents'])
                except KeyError:
                    return []
def matricidio(jugador, pareja):
    x= random.randint(20,9500)
    y= random.randint(20,9500)
    geneacity_API_request(f"https://geneacity.life/API/createInhabitantUnion/?idInhabitant1={jugador["id"]}&idInhabitant2={pareja["id"]}&newHouseXPostition={x}&newHouseYPostition={y}")
    print(f"Felicidades, te has casado, tu nueva vivienda está en ({x},{y})")
def reproduccion(jugador,nombre,root,three):
        child = geneacity_API_request(f"https://geneacity.life/API/createChildren/?name={nombre}&idInhabitant={jugador["id"]}&gender=Male&age=20")
        child= child.json["childId"]["id"]
        print(f"Felicidades, acabas de tener un/una hijo/a bien bonito/a llamado {nombre}")
        child = info_persona(child)
        three.agregar_nodo(Persona(child["id"], child["name"]))
        three.establecer_padre(child["id"],child["father"])
        three.establecer_madre(child["id"],child["mother"])
        root.destroy()
        return three

def request_casas(lista, jx, jy):
    """Función optimizada para realizar las consultas de casas al API, evitando duplicados.

    Args:
        lista (list): lista que almacena los jsons de la consulta del API.
        jx (int): posición x del jugador.
        jy (int): posición y del jugador.

    Returns:
        list: lista actualizada de jsons.
    """
    # Realizar la consulta al API
    consulta = geneacity_API_request(f'https://geneacity.life/API/getHouses/?x={jx}&y={jy}')
    nuevo_json = consulta.json
    
    # Extraer las coordenadas de las casas en la respuesta
    nuevas_casas = {(casa['x'], casa['y']) for casa in nuevo_json.get('houses', [])}

    # Evitar añadir duplicados verificando si las casas ya están en la lista
    for casas_json in lista:
        casas_existentes = {(casa['x'], casa['y']) for casa in casas_json.get('houses', [])}
        # Actualizar el conjunto de nuevas casas eliminando las que ya están presentes
        nuevas_casas.difference_update(casas_existentes)
    
    # Solo agregar nuevas casas si hay casas únicas en la respuesta actual
    if nuevas_casas:
        lista.append(nuevo_json)
    
    return lista

            
def game(jugador):
    global screen_width
    from PIL import Image
    from arbol import ArbolGenealogico,Persona,Nodo
    from utilidades import current_frame,frame_count,frame_actual,frames,ventana_parentezco,puntaje_actual, j_info_open,jsons, habitantes, contadores, sprites, skins, size, screen, image, image_rect, casa_img, x, y, jugadorx, jugadory, clock, speed, fondo, tile_size, tiles, window_open, persona_info_open, esc_press, lockW, lockA, lockS, lockD, cont_casas
    from guardar_partidas import guardar_partida, crear_partida
    import time
    global three
    tiempo =0
    jugador=info_persona(jugador["id"])
    pygame.init()
    arbol_jugador(jugador,three)
    ventana = tk.Tk()
    screen_width = ventana.winfo_screenwidth()
    three.posiciones = three.calcular_posiciones(screen_width)
    ventana.destroy()
    while True:
        
        screen.fill([48, 126, 201])

        # Dibuja solo los mosaicos visibles
        pablito=0
        jaime=0
        for tile in tiles:
            tile_rect = tile.get_rect()  
            tile_rect.topleft = (tile.get_rect().x + x+pablito, tile.get_rect().y + y+jaime)
            jaime+=1000
            if jaime>=10000:
                jaime=0
                pablito+=1000
            if screen.get_rect().colliderect(tile_rect):
                screen.blit(tile, tile_rect)

        screen.blit(pygame.transform.scale(image, (40, 70)), (image_rect))

        #coloca las casas en las coordenadas que estas tengan dentro del diccionario
        keys = pygame.key.get_pressed()
        for casas in jsons:
            try:
                for casa in casas['houses']:
                    casa_x = int(casa['x'])
                    casa_y = int(casa['y'])
                    screen.blit(casa_img, (casa_x+x, casa_y+y))
                
            except Exception: #except utilizado por que algunos jsons vienen vacios al no tener casar alrededor en el momento de las consulta
                pass   
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    jsons = request_casas(jsons, jugadorx, jugadory)
                if event.key == pygame.K_ESCAPE:
                    esc_press = True  # marcar que la tecla ESC se ha presionado

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    esc_press = False

            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if j_info_open:
                    if arbol.collidepoint(event.pos):
                        ver_familia(three,Ver=True) 
                if ventana_j.collidepoint(event.pos):
                    jinfo=info_persona(jugador["id"])
                    j_info_open=True
                try:
                    if hijo.collidepoint(event.pos):
                        root = tk.Tk()
                        root.title("Entrada de Texto")
                        root.geometry("400x300")
                        label_prompt = tk.Label(root, text="Ingresa un nombre", font=("Helvetica", 14))
                        label_prompt.pack(pady=20)

                        # Crear y configurar el campo de entrada (Entry)
                        entry = tk.Entry(root, font=("Helvetica", 14))
                        entry.pack(pady=20)
                        # Crear un botón para mostrar el valor del campo de entrada
                        button = tk.Button(root, text="Confirmar", command=lambda: reproduccion(jugador, entry.get(),root,three))
                        button.pack(pady=10)

                        # Crear una etiqueta para mostrar el texto ingresado
                        label = tk.Label(root, text="", font=("Helvetica", 14))
                        label.pack(pady=20)

                        # Ejecutar el bucle principal de la aplicación
                        root.mainloop()
                except:
                    pass
                if not window_open and not persona_info_open:
                    
                
                    mouse_x, mouse_y = event.pos #posicion del click
                    # Verificar cada casa para ver si el clic fue sobre ella
                    for casas in jsons:
                        for casa in casas['houses']:
                            casa_x = int(casa['x'])+x
                            casa_y = int(casa['y'])+y
                            casa_rect = casa_img.get_rect(topleft=(casa_x, casa_y)) #posicion de la imagen de la casa
                            
                            if casa_rect.collidepoint(mouse_x, mouse_y) : 
                                habitantes=Info_casas(jsons,casa_x-x,casa_y-y)
                                window_open=True

                elif window_open and not persona_info_open:
                    mouse_x, mouse_y = event.pos
                    for i, p in enumerate(habitantes):
                        persona=p["name"]
                        ventana_x = 130
                        ventana_y = 80 + i * 50
                        window_rect = pygame.Rect(ventana_x, ventana_y, 100, 30)
                        if window_rect.collidepoint(mouse_x, mouse_y):
                            if persona in [p['name'] for p in habitantes]:
                                persona_seleccionada = info_persona(p['id'])
                                persona_info_open=True
                elif persona_info_open:
                    if arbol_p.collidepoint(event.pos):
                        retorno= buscar_parentezco(jugador,persona_seleccionada)
                        puntaje_actual+=retorno[0]
                        parentezco=retorno[1]
                        ventana_parentezco=True 
                        if retorno[2]==None:
                            pass
                        else:
                            three.agregar_nodo(retorno[2])
                            padre=retorno[2].padre
                            madre=retorno[2].madre
                            three.establecer_padre(retorno[2].id, padre.id)
                            three.establecer_madre(retorno[2].id, madre.id)   

                            nueva_pos = three.calcular_posicion_nueva_persona(padre.id, madre.id)
                            if nueva_pos:
                                three.posiciones[retorno[2].id] = nueva_pos
                        pass
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                        person_info_open = False
                    try:
                        if casarse.collidepoint(event.pos):
                            matricidio(jugador,persona_seleccionada)
                    except:
                        pass
            if event.type == pygame.KEYUP:
                lockS,lockA,lockD,lockW=True,True,True,True

        
        

        if esc_press: #cierra la ventana de las personas 
            if persona_info_open:
                persona_info_open=False
            elif window_open:
                window_open=False
            elif j_info_open:
                j_info_open=False
            esc_press=False

            

        if keys[pygame.K_s] and lockS:
            lockA,lockD,lockW=False,False,False
            screen.blit(pygame.transform.scale(image,(40, 70)), image_rect)
            contadores["s"], image = imagen(contadores, image, "s")
            y-=speed        
            jugadory+=speed
            cont_casas+=1
            """if cont_casas>=40:
                cont_casas=0
                jsons=request_casas(jsons, jugadorx, jugadory)       
                jsons=request_casas(jsons, jugadorx, jugadory+800)"""
            
            
        if not window_open and not persona_info_open:   
            if keys[pygame.K_w] and lockW:
                lockA,lockD,lockS=False,False,False
                screen.blit(pygame.transform.scale(image,(40, 70)), image_rect)
                contadores["w"], image = imagen(contadores, image, "w")
                y+=speed
                jugadory-=speed
                cont_casas+=1
                """ if cont_casas>=40:
                    cont_casas=0
                    jsons=request_casas(jsons, jugadorx, jugadory)       
                    jsons=request_casas(jsons, jugadorx, jugadory-800)"""
                
            if keys[pygame.K_a] and lockA:       
                lockS,lockD,lockW=False,False,False
                screen.blit(pygame.transform.scale(image,(40, 70)), image_rect)
                contadores["a"], image = imagen(contadores, image, "a")
                x+=speed
                jugadorx-=speed
                cont_casas+=1
                """if cont_casas>=40:
                    cont_casas=0
                    jsons=request_casas(jsons, jugadorx, jugadory)       
                    jsons=request_casas(jsons, jugadorx-800, jugadory)"""
                
            if keys[pygame.K_d] and lockD:
                lockA,lockS,lockW=False,False,False
                screen.blit(pygame.transform.scale(image,(40, 70)), image_rect)
                contadores["d"], image = imagen(contadores, image, "d")
                x-=speed 
                jugadorx+=speed
                cont_casas+=1
                """ if cont_casas>=40:
                    cont_casas=0
                    jsons=request_casas(jsons, jugadorx, jugadory)       
                    jsons=request_casas(jsons, jugadorx+800, jugadory)"""

        if window_open: #verifica si se toco una casa, esta variable se pone en true
            speed=0    
            screen.blit(pygame.transform.scale(pygame.image.load("imagenes_Proyecto3/interiorcasa2.png").convert_alpha(),(600,600)),(95,-10)) 
            ventana_x=130
            ventana_y=80
            personas=[]
            for p in habitantes: #por el momento almacena solo los nombres de las personas
                personas.append(p['name'])
                # Dibuja un rectángulo que simula una ventana
            for e in personas:
                window_rect = pygame.Rect(ventana_x, ventana_y, 120, 30)  # Tamaño y posición de la ventana simulada
                pygame.draw.rect(screen, (255, 255, 255), window_rect)  # Dibuja un rectángulo blanco
                font = pygame.font.Font(None, 36)
                text = font.render(str(e), True, (0, 0, 0))
                screen.blit(text, (ventana_x, ventana_y))  # pone una ventana con el nombre de la persona
                ventana_y+=50
            if keys[pygame.K_ESCAPE]: #cierra la ventana de las personas 
                persona_info_open=False
        if persona_info_open: #verifica si se toco una persona, esta variable se pone en true
            speed=0    
            ventana_x=150
            ventana_y=300
            screen.blit(pygame.transform.scale(pygame.image.load("imagenes_Proyecto3/agenda.png").convert_alpha(),(600,600)),(80,100)) 
            font = pygame.font.Font(None, 36)
            # Información de la persona seleccionada
            info_lines = [
                f"Name: {persona_seleccionada['name']}",
                f"Age: {persona_seleccionada['age']}",
                # Agregar más detalles según los datos disponibles
                f"Estado civil: {persona_seleccionada["marital_status"]}",
                f"Genero: {persona_seleccionada['gender']}"
            ]   # Renderizar y blitear cada línea de información
            for i, line in enumerate(info_lines):
                text = font.render(line, True, (0,0,0))
                screen.blit(text, (ventana_x+10, ventana_y+10 + i * 50))
            arbol_p=pygame.Rect(300,500,200,50)
            pygame.draw.rect(screen,  (94, 76, 72), arbol_p)
            text = font.render("Ver Similitud", True, (255,255,255))
            screen.blit(text,(325,513))
            if persona_seleccionada["marital_status"]=="Single" and jugador["marital_status"]=="Single" and not persona_seleccionada["gender"]==jugador["gender"] and not jugador["id"]==persona_seleccionada["id"] and int(jugador["age"])>25 and int(persona_seleccionada["age"])>25:
                casarse = pygame.Rect(300, 570, 200, 50)
                pygame.draw.rect(screen, (94, 76, 72), casarse)
                text = font.render("Casarse", True, (255,255,255))
                screen.blit(text,(350,580))
            
        if j_info_open:
                    jinfo_lines = [
                    f"Name: {jinfo['name']}",
                    f"Age: {jinfo['age']}",
                    f"Estado civil: {jinfo["marital_status"]}",
                    f"Genero: {jinfo['gender']}"
                    f"Casa: {jinfo["house"]}"]
                    infoj=pygame.Rect(100,100,600,600)
                    arbol=pygame.Rect(300,500,200,50)
                    screen.blit(pygame.transform.scale(pygame.image.load("imagenes_Proyecto3/agenda.png").convert_alpha(),(600,600)),(80,100)) 
                    
                    font = pygame.font.Font(None, 36)
                    posx,posy=200,300
                    for i, line in enumerate(jinfo_lines):
                        
                        text = font.render(line, True, (0,0,0))
                        screen.blit(text, (posx,posy))
                        posy+=40
                    pygame.draw.rect(screen, (94, 76, 72), arbol)
                    text = font.render("Ver Arbol", True, (255,255,255))
                    screen.blit(text,(343,510))
        if jugador["marital_status"]=="Married":
                hijo=pygame.Rect(100,0,150,30)
                font = pygame.font.Font(None, 36)
                pygame.draw.rect(screen, (0,0,0), hijo)
                screen.blit(pygame.transform.scale(pygame.image.load("imagenes_Proyecto3/marco.png").convert_alpha(),(152,40)),hijo.topleft) 
                text = font.render("reproducirse", True, (255,255,255))
                screen.blit(text,(102,2))
        
        if ventana_parentezco==True:
                while tiempo<=4000:
                    tiempo+=1
                    resultado = pygame.Rect(170, 553, 470, 50)
                    pygame.draw.rect(screen, (94, 76, 72), resultado)
                    font = pygame.font.Font(None, 20)
                    text = font.render(f"Esta persona {parentezco}!!", True, (255,255,255))
                    screen.blit(text,(195,566))
                    pygame.display.update()
                tiempo=0
                ventana_parentezco=False        
            
       
        ventana_j=pygame.Rect(0,0,100,100)
        screen.blit(pygame.transform.scale(pygame.image.load("imagenes_Proyecto3/cuadrado.png").convert_alpha(),(100,100)),ventana_j.topleft) 
        screen.blit(pygame.transform.scale(image, (80, 80)),(11,10))    
        posicionJ=pygame.Rect(0,100,100,20)
        screen.blit(pygame.transform.scale(pygame.image.load("imagenes_Proyecto3/marco.png").convert_alpha(),(102,30)),posicionJ.topleft) 
        if jugadorx>9999 or jugadory>9999:
            font = pygame.font.Font(None, 25)
            text = font.render(f"{jugadorx},{jugadory}", True, (0,0,0))
            screen.blit(text,(2,105)) 
        elif jugadorx>999 or jugadory>999:
                    font = pygame.font.Font(None, 30)
                    text = font.render(f"{jugadorx},{jugadory}", True, (0,0,0))
                    screen.blit(text,(2,105)) 
        else:
            font = pygame.font.Font(None, 35)
            text = font.render(f"{jugadorx},{jugadory}", True, (0,0,0))
            screen.blit(text,(2,105))    
        #screen.blit(pygame.transform.scale(pygame.image.load("imagenes_Proyecto3/guardado.png").convert_alpha(),(100,100)),(700,0)) 
        puntuacion=pygame.Rect(350,0,100,20)
        screen.blit(pygame.transform.scale(pygame.image.load("imagenes_Proyecto3/marco.png").convert_alpha(),(102,30)),puntuacion.topleft) 
        font = pygame.font.Font(None, 36)
        text = font.render(f"{puntaje_actual}", True, (0,0,0))
        screen.blit(text,(390,0))        
        if not window_open:
            speed=25
        if tiempo==700:
            tiempo=0
            jugador=info_persona(jugador["id"])
            while current_frame<frame_count:
                

                # Limpiar la ventana
                  # Fondo blanco

                # Actualizar la imagen de la animación
                screen.blit((frames[int(current_frame)]), (700, 0))  # Ajusta la posición según sea necesario

                # Actualizar el frame actual
                current_frame += animation_speed
                

                # Actualizar la ventana
                pygame.display.update()
            current_frame=0
            crear_partida(jugador,puntaje_actual,(jugadorx,jugadory))

        tiempo+=1
        pygame.display.update()
        clock.tick(40)
