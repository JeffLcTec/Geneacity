import tkinter as tk
puntaje_max = 1000
puntaje_actual = 0
class Persona:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.padre = None
        self.madre = None
        self.hijos = []

    def __str__(self) -> str:
        return f"({self.id}, {self.nombre})"


class Nodo:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.padre = None
        self.madre = None
        self.hijos = []

class ArbolGenealogico:
    def __init__(self):
        self.personas = {}
        self.nodos_dibujados = set()

    def agregar_nodo(self, nodo):
        if nodo.id not in self.personas:
            self.personas[nodo.id] = nodo

    def establecer_padre(self, id_nodo, id_padre):
        if id_nodo in self.personas and id_padre in self.personas:
            self.personas[id_nodo].padre = self.personas[id_padre]
            self.personas[id_padre].hijos.append(self.personas[id_nodo])

    def establecer_madre(self, id_nodo, id_madre):
        if id_nodo in self.personas and id_madre in self.personas:
            self.personas[id_nodo].madre = self.personas[id_madre]
            self.personas[id_madre].hijos.append(self.personas[id_nodo])

    def ver_arbol(self, canvas: tk.Canvas, ventana: tk.Tk) -> None:
        raices = [persona for persona in self.personas.values() if persona.padre is None and persona.madre is None]
        y_start = 80
        x_start = 105
        level_spacing = 100
        sibling_spacing = 200

        # Para rastrear nodos ya dibujados y evitar duplicados
        self.nodos_dibujados = set()

        for i, raiz in enumerate(raices):
            self.__ver_arbol(canvas, x_start + i * sibling_spacing, y_start, raiz, level_spacing, sibling_spacing, is_root=True)

        ventana.mainloop()

    def __ver_arbol(self, canvas: tk.Canvas, x, y, nodo: Nodo, level_spacing, sibling_spacing, is_root=False) -> None:
        if nodo in self.nodos_dibujados:
            return

        self.nodos_dibujados.add(nodo)
        radius = 40
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#00BB00", fill="white", width=3)
        canvas.create_text(x, y, text=nodo.name, font=("Helvetica", 12))

        if nodo.padre and nodo.madre and not is_root:
            padre_x = nodo.padre_x
            madre_x = nodo.madre_x
            mid_x = (padre_x + madre_x) / 2
            parent_y = y - level_spacing + radius

            # Línea horizontal entre los padres
            canvas.create_line(padre_x+100, parent_y, madre_x+100, parent_y, fill="black", width=2)
            # Línea vertical desde el punto medio al nodo del hijo
            canvas.create_line(mid_x+100, parent_y, mid_x+100, y - radius, fill="black", width=2)
        elif is_root:
            padre_x = x - sibling_spacing // 2
            madre_x = x + sibling_spacing // 2
            mid_x = x
            parent_y = y

        child_y = y + level_spacing
        child_x = x - (len(nodo.hijos) - 1) * sibling_spacing // 2

        for hijo in nodo.hijos:
            hijo.padre_x = padre_x
            hijo.madre_x = madre_x
            canvas.create_line(mid_x, y + radius, child_x, child_y - radius, fill="black", width=2)
            self.__ver_arbol(canvas, child_x+100, child_y+20, hijo, level_spacing, sibling_spacing)
            child_x += sibling_spacing
    def ver_arbol2(self, canvas: tk.Canvas, ventana: tk.Tk) -> None:
        raices = [nodo for nodo in self.nodos if nodo.padre is None and nodo.madre is None]
        y_start = 80
        
        level_spacing = 100
        sibling_spacing = 100

        # Para rastrear nodos ya dibujados y evitar duplicados
        self.nodos_dibujados = set()
        ancho_canvas = canvas.winfo_width()
        x_start= ancho_canvas//2 -50

        for i, raiz in enumerate(raices):
            self.__ver_arbol2(canvas, x_start + i * sibling_spacing, y_start, raiz, level_spacing, sibling_spacing, is_root=True)

        ventana.mainloop()
    def __ver_arbol2(self, canvas: tk.Canvas, x, y, nodo: Nodo, level_spacing, sibling_spacing, is_root=False) -> None:
        # Dibuja el árbol recursivamente en el canvas
        if nodo in self.nodos_dibujados:
            return

        self.nodos_dibujados.add(nodo)
        radius = 40
        # Dibuja un óvalo para representar el nodo
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#00BB00", fill="white", width=3)
        # Dibuja el nombre de la persona en el nodo
        canvas.create_text(x, y, text=nodo.name, font=("Helvetica", 12))

        if nodo.padre and nodo.madre and not is_root:
            # Calcula las coordenadas para dibujar las líneas entre padres e hijos
            padre_x = nodo.padre_x
            madre_x = nodo.madre_x
            mid_x = (padre_x + madre_x) / 2
            parent_y = y - level_spacing + radius

            # Línea horizontal entre los padres
            canvas.create_line(padre_x+50, parent_y, madre_x+50, parent_y, fill="black", width=2)
            # Línea vertical desde el punto medio al nodo del hijo
            canvas.create_line(mid_x+50, parent_y, mid_x+50, y - radius, fill="black", width=2)
        elif is_root:
            # Asigna coordenadas a los padres si es el nodo raíz
            padre_x = x - sibling_spacing // 2
            madre_x = x + sibling_spacing // 2
            mid_x = x
            parent_y = y

        if nodo.hijos:
            # Dibuja una línea horizontal para conectar todos los hijos
            hijo_start_x = x+50 - (len(nodo.hijos) - 1) * sibling_spacing // 2
            if len(nodo.hijos)==2:
                hijo_end_x = x + (len(nodo.hijos)-1) * sibling_spacing // 2
            else:
                hijo_end_x = x-50 + (len(nodo.hijos)-1) * sibling_spacing // 2
            canvas.create_line(hijo_start_x, y + level_spacing - radius, hijo_end_x, y + level_spacing - radius, fill="black", width=2)

            child_y = y + level_spacing
            child_x = hijo_start_x

            for hijo in nodo.hijos:
                # Asigna coordenadas a los hijos
                hijo.padre_x = padre_x
                hijo.madre_x = madre_x
                # Dibuja una línea vertical desde la línea horizontal a cada hijo
                canvas.create_line(child_x, y + level_spacing - radius, child_x, child_y - radius, fill="black", width=2)
                self.__ver_arbol2(canvas, child_x, child_y, hijo, level_spacing, sibling_spacing)
                child_x += sibling_spacing
    def obtener_ancestros(self, id_persona):
        ancestros = set()
        self._obtener_ancestros_recursivo(self.personas[id_persona], ancestros)
        return ancestros

    def _obtener_ancestros_recursivo(self, persona, ancestros):
        global puntaje_actual
        
        if persona is None:
            return
        
       
        ancestros.add((persona.id, persona.name))
    
        self._obtener_ancestros_recursivo(persona.padre, ancestros)
        self._obtener_ancestros_recursivo(persona.madre, ancestros)
    
    def obtener_ancestros_con_distancia(self, id_persona):
        ancestros = {}
        self._obtener_ancestros_recursivo(self.personas[id_persona], ancestros, 0)
        return ancestros

    def _obtener_ancestros_recursivo(self, persona, ancestros, distancia):
        if persona is None:
            return
        vinculo=""
        if distancia==0:
            vinculo="Ego"
        if distancia==1:
            vinculo="Padre/Madre"
        if distancia==2:
            vinculo="Abuelo/Abuela"
        if distancia==3:
            vinculo="Bisabuelo/abuela"
        if distancia==4:
            vinculo="TataraAbuelo/Abuela"
        if distancia==5:
            vinculo="TrastataraAbuelo/Abuela"
        

        ancestros[persona.id] = (persona.name, distancia,vinculo)
        self._obtener_ancestros_recursivo(persona.padre, ancestros, distancia + 1)
        self._obtener_ancestros_recursivo(persona.madre, ancestros, distancia + 1)

def determinar_vinculo(relacion_jugador, relacion_persona):
    if relacion_jugador == "Ego" and relacion_persona == "Ego":
        return "Misma persona"
    if relacion_jugador == "Padre/Madre" and relacion_persona == "Ego":
        return "Hijo/Hija"
    if relacion_jugador == "Ego" and relacion_persona == "Padre/Madre":
        return "Padre/Madre"
    if relacion_jugador == "Padre/Madre" and relacion_persona == "Padre/Madre":
        return "Hermano/a"
    if relacion_jugador == "Abuelo/Abuela" and relacion_persona == "Abuelo/Abuela":
        return "Primo/a"
    if relacion_jugador == "Padre/Madre" and relacion_persona == "Abuelo/Abuela":
        return "Tío/Tía"
    if relacion_jugador == "Abuelo/Abuela" and relacion_persona == "Padre/Madre":
        return "Sobrino/a"
    if relacion_jugador == "Bisabuelo/Bisabuela" and relacion_persona == "Bisabuelo/Bisabuela":
        return "Primo/a segundo"
    if relacion_jugador == "Padre/Madre" and relacion_persona == "Bisabuelo/Bisabuela":
        return "Tío abuelo/Tía abuela"
    if relacion_jugador == "Bisabuelo/Bisabuela" and relacion_persona == "Padre/Madre":
        return "Sobrino nieto/Sobrina nieta"
    if relacion_jugador == "Tatarabuelo/Tatarabuela" and relacion_persona == "Tatarabuelo/Tatarabuela":
        return "Primo/a tercero"
    if relacion_jugador == "Padre/Madre" and relacion_persona == "Tatarabuelo/Tatarabuela":
        return "Tataratío/Tataratía"
    if relacion_jugador == "Tatarabuelo/Tatarabuela" and relacion_persona == "Padre/Madre":
        return "Tatarasobrino/Tatarasobrina"
    if relacion_jugador == "Trastatarabuelo/Trastatarabuela" and relacion_persona == "Trastatarabuelo/Trastatarabuela":
        return "Primo/a cuarto"
    if relacion_jugador == "Padre/Madre" and relacion_persona == "Trastatarabuelo/Trastatarabuela":
        return "Trastataratío/Trastataratía"
    if relacion_jugador == "Trastatarabuelo/Trastatarabuela" and relacion_persona == "Padre/Madre":
        return "Trastatarasobrino/Trastatarasobrina"
    # Agregar más reglas según sea necesario
    return "Relación lejana"



def buscar_similitud(jugador, persona, arbol1, arbol2):
    ancestros_jugador = arbol1.obtener_ancestros_con_distancia(jugador["id"])
    ancestros_persona = arbol2.obtener_ancestros_con_distancia(persona["id"])
    ancestros_comunes=[]
    while len(ancestros_comunes)<3:
        for ancestro_id in ancestros_jugador.keys():
            if ancestro_id in ancestros_persona:
                    ancestros_comunes.append(determinar_vinculo(ancestros_jugador[ancestro_id][2], ancestros_persona[ancestro_id][2]))
                    ancestros_comunes.append(determinar_vinculo(ancestros_persona[ancestro_id][2],ancestros_jugador[ancestro_id][2]))
    if ancestros_comunes:
        print("Ancestros comunes encontrados:")
        print(f"Eres el {ancestros_comunes[0]} de esta persona!!")
        print(f"Esta persona es tu {ancestros_comunes[1]}!!")
    else:
        print("No se encontraron ancestros comunes.")




