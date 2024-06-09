import tkinter as tk

class Persona:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.padre = None
        self.madre = None
        self.hijos = []

    def __str__(self) -> str:
        return f"({self.id}, {self.name})"


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
        ventana.update()
        raices = [persona for persona in self.personas.values() if persona.padre is None and persona.madre is None]
        y_start = 40  # Reducido
        level_spacing = 60  # Reducido
        sibling_spacing = 80  # Reducido

        # Para rastrear nodos ya dibujados y evitar duplicados
        self.nodos_dibujados = set()
        ancho_canvas = canvas.winfo_width()
        x_start = ancho_canvas // 2 - 50

        for i, raiz in enumerate(raices):
            self.__ver_arbol(canvas, x_start + i * sibling_spacing, y_start, raiz, level_spacing, sibling_spacing, is_root=True)
        
        label = tk.Label(ventana, text="Cierra para ver el vínculo!!!")
        label.pack(padx=20, pady=20)
        ventana.mainloop()

    def __ver_arbol(self, canvas: tk.Canvas, x, y, nodo: Nodo, level_spacing, sibling_spacing, is_root=False) -> None:
        # Dibuja el árbol recursivamente en el canvas
        if nodo in self.nodos_dibujados:
            return

        self.nodos_dibujados.add(nodo)
        radius = 20  # Reducido
        # Dibuja un óvalo para representar el nodo
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#00BB00", fill="white", width=2)  # Ajustado el ancho del borde
        # Dibuja el nombre de la persona en el nodo
        canvas.create_text(x, y, text=nodo.name, font=("Helvetica", 8))  # Tamaño de fuente reducido

        padre_x = None
        madre_x = None

        if nodo.padre and nodo.madre and not is_root:
            # Calcula las coordenadas para dibujar las líneas entre padres e hijos
            padre_x = x - sibling_spacing
            madre_x = x + sibling_spacing
            mid_x = (padre_x + madre_x) / 2
            parent_y = y - level_spacing + radius

            # Línea horizontal entre los padres
            canvas.create_line(padre_x + 25, parent_y, madre_x + 25, parent_y, fill="black", width=1)  # Ajustado
            # Línea vertical desde el punto medio al nodo del hijo
            canvas.create_line(mid_x + 25, parent_y, mid_x + 25, y - radius, fill="black", width=1)  # Ajustado
        elif is_root:
            # Asigna coordenadas a los padres si es el nodo raíz
            padre_x = x - sibling_spacing // 2
            madre_x = x + sibling_spacing // 2
            mid_x = x
            parent_y = y

        if nodo.hijos:
            # Dibuja una línea horizontal para conectar todos los hijos
            hijo_start_x = x + 25 - (len(nodo.hijos) - 1) * sibling_spacing // 2
            if len(nodo.hijos) == 2:
                hijo_end_x = x + (len(nodo.hijos) - 1) * sibling_spacing // 2
            else:
                hijo_end_x = x - 25 + (len(nodo.hijos) - 1) * sibling_spacing // 2
            canvas.create_line(hijo_start_x, y + level_spacing - radius, hijo_end_x, y + level_spacing - radius, fill="black", width=1)  # Ajustado

            child_y = y + level_spacing
            child_x = hijo_start_x

            for hijo in nodo.hijos:
                # Asigna coordenadas a los hijos
                hijo.padre_x = padre_x
                hijo.madre_x = madre_x
                # Dibuja una línea vertical desde la línea horizontal a cada hijo
                canvas.create_line(child_x, y + level_spacing - radius, child_x, child_y - radius, fill="black", width=1)  # Ajustado
                self.__ver_arbol(canvas, child_x, child_y, hijo, level_spacing, sibling_spacing)
                child_x += sibling_spacing

        # Dibuja a los hermanos del nodo
        if nodo.padre or nodo.madre:
            hermanos = []
            if nodo.padre:
                hermanos.extend(nodo.padre.hijos)
            if nodo.madre:
                hermanos.extend(nodo.madre.hijos)
            hermanos = [hermano for hermano in hermanos if hermano != nodo]

            sibling_y = y
            sibling_x = x + sibling_spacing

            for hermano in hermanos:
                if hermano not in self.nodos_dibujados:
                    canvas.create_line(x + radius, y, sibling_x - radius, sibling_y, fill="black", width=1)  # Ajustado
                    self.__ver_arbol(canvas, sibling_x, sibling_y, hermano, level_spacing, sibling_spacing)
                    sibling_x += sibling_spacing

        # Dibuja a los abuelos del nodo
        if nodo.padre:
            abuelo_paterno = nodo.padre.padre
            abuela_paterna = nodo.padre.madre
            if abuelo_paterno:
                self.__ver_arbol(canvas, x - sibling_spacing, y - level_spacing, abuelo_paterno, level_spacing, sibling_spacing)
            if abuela_paterna:
                self.__ver_arbol(canvas, x + sibling_spacing, y - level_spacing, abuela_paterna, level_spacing, sibling_spacing)
        if nodo.madre:
            abuelo_materno = nodo.madre.padre
            abuela_materna = nodo.madre.madre
            if abuelo_materno:
                self.__ver_arbol(canvas, x - sibling_spacing, y - level_spacing, abuelo_materno, level_spacing, sibling_spacing)
            if abuela_materna:
                self.__ver_arbol(canvas, x + sibling_spacing, y - level_spacing, abuela_materna, level_spacing, sibling_spacing)


    def obtener_ancestros(self, id_persona):
        ancestros = set()
        self._obtener_ancestros_recursivo(self.personas[id_persona], ancestros)
        return ancestros

    def _obtener_ancestros_recursivo(self, persona, ancestros):
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
        vinculo = ["Ego", "Padre/Madre", "Abuelo/Abuela", "Bisabuelo/Bisabuela", "Tatarabuelo/Tatarabuela"]
        ancestros[persona.id] = (persona.name, distancia, vinculo[min(distancia, len(vinculo) - 1)])
        self._obtener_ancestros_recursivo(persona.padre, ancestros, distancia + 1)
        self._obtener_ancestros_recursivo(persona.madre, ancestros, distancia + 1)


def determinar_vinculo(relacion_jugador, relacion_persona):
    if relacion_jugador == "Ego" and relacion_persona == "Ego":
        return "Misma persona"
    if relacion_jugador == "Padre/Madre" and relacion_persona == "Ego":
        return "Hijo/Hija"
    if relacion_jugador == "Ego" and relacion_persona == "Padre/Madre":
        return "Padre/Madre"
    if relacion_jugador == "Abuelo/Abuela" and relacion_persona == "Ego":
        return "Nieto/a"
    if relacion_jugador == "Ego" and relacion_persona == "Abuelo/Abuela":
        return "Abuelo/Abuela"
    if relacion_jugador == "Bisabuelo/Bisabuela" and relacion_persona == "Ego":
        return "Bisnieto/a"
    if relacion_jugador == "Ego" and relacion_persona == "Bisabuelo/Bisabuela":
        return "Bisabuelo/Bisabuela"
    if relacion_jugador == "Tatarabuelo/Tatarabuela" and relacion_persona == "Ego":
        return "Tataranieto/a"
    if relacion_jugador == "Ego" and relacion_persona == "Tatarabuelo/Tatarabuela":
        return "Tatarabuelo/Tatarabuela"
    if relacion_jugador == "Trastatarabuelo/Trastatarabuela" and relacion_persona == "Ego":
        return "Trastataranieto/a"
    if relacion_jugador == "Ego" and relacion_persona == "Trastatarabuelo/Trastatarabuela":
        return "Trastatarabuelo/Trastatarabuela"
    if relacion_jugador == "Pentabuelo/Pentabuela" and relacion_persona == "Ego":
        return "Pentanieto/a"
    if relacion_jugador == "Ego" and relacion_persona == "Pentabuelo/Pentabuela":
        return "Pentabuelo/Pentabuela"

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
        return "Trastataratío/Tataratío/Tataratía/Tía-Trastatarabuelo/Trastatarabuela"
    if relacion_jugador == "Trastatarabuelo/Trastatarabuela" and relacion_persona == "Padre/Madre":
        return "Trastatarasobrino/Tatarasobrino"
    if relacion_jugador == "Pentabuelo/Pentabuela" and relacion_persona == "Pentabuelo/Pentabuela":
        return "Primo/a quinto"
    if relacion_jugador == "Padre/Madre" and relacion_persona == "Pentabuelo/Pentabuela":
        return "Pentatío/Pentatía"
    if relacion_jugador == "Pentabuelo/Pentabuela" and relacion_persona == "Padre/Madre":
        return "Pentasobrino/Pentasobrina"
    if relacion_jugador == "Abuelo/Abuela" and relacion_persona == "Sobrino/a":
        return "Sobrino/a tercero"
    if relacion_jugador == "Padre/Madre" and relacion_persona == "Bisabuelo/Bisabuela":
        return "Tío/a tercero"
    return "Relación lejana"



def buscar_similitud(jugador, persona, arbol1, arbol2):
    puntaje_actual = 0
    ancestros_jugador = arbol1.obtener_ancestros_con_distancia(jugador["id"])
    ancestros_persona = arbol2.obtener_ancestros_con_distancia(persona["id"])
    
    # Utilizar conjuntos para encontrar ancestros comunes
    ancestros_comunes_ids = set(ancestros_jugador.keys()).intersection(ancestros_persona.keys())
    
    ancestros_comunes = []
    for ancestro_id in ancestros_comunes_ids:
        vinculo_jugador = determinar_vinculo(ancestros_jugador[ancestro_id][2], ancestros_persona[ancestro_id][2])
        vinculo_persona = determinar_vinculo(ancestros_persona[ancestro_id][2], ancestros_jugador[ancestro_id][2])
        ancestros_comunes.append((vinculo_jugador, vinculo_persona))

        # Limitar el número de ancestros comunes a 3
        if len(ancestros_comunes) ==2:
            break

    # Determinar el puntaje y la relación basada en el primer ancestro común encontrado
    if ancestros_comunes:
        vinculo_jugador, vinculo_persona = ancestros_comunes[0]

        if vinculo_persona == "Padre/Madre":
            puntaje_actual += 5
        elif vinculo_persona == "Hijo/Hija":
            puntaje_actual += 5
        elif vinculo_persona == "Hermano/a":
            puntaje_actual += 10
        elif vinculo_persona == "Nieto/a":
            puntaje_actual += 10
        elif vinculo_persona == "Abuelo/Abuela":
            puntaje_actual += 10
        elif vinculo_persona == "Bisabuelo/Bisabuela":
            puntaje_actual += 15
        elif vinculo_persona == "Bisnieto/a":
            puntaje_actual += 15
        elif vinculo_persona == "Tío/Tía":
            puntaje_actual += 15
        elif vinculo_persona == "Sobrino/a":
            puntaje_actual += 15
        elif vinculo_persona == "Primo/a":
            puntaje_actual += 20
        elif vinculo_persona == "Tío abuelo/Tía abuela":
            puntaje_actual += 20
        elif vinculo_persona == "Sobrino nieto/Sobrina nieta":
            puntaje_actual += 20
        elif vinculo_persona == "Tatarabuelo/Tatarabuela":
            puntaje_actual += 20
        elif vinculo_persona == "Tataranieto/a":
            puntaje_actual += 20
        elif vinculo_persona == "Primo/a segundo":
            puntaje_actual += 25
        elif vinculo_persona == "Tío bisabuelo/Tía bisabuela":
            puntaje_actual += 25
        elif vinculo_persona == "Sobrino bisnieto/Sobrina bisnieta":
            puntaje_actual += 25
        elif vinculo_persona == "Trastatarabuelo/Trastatarabuela":
            puntaje_actual += 25
        elif vinculo_persona == "Trastataranieto/a":
            puntaje_actual += 25
        elif vinculo_persona == "Primo/a tercero":
            puntaje_actual += 30
        elif vinculo_persona == "Tío tatarabuelo/Tía tatarabuela":
            puntaje_actual += 30
        elif vinculo_persona == "Sobrino tataranieto/Sobrina tataranieta":
            puntaje_actual += 30
        elif vinculo_persona == "Pentabuelo/Pentabuela":
            puntaje_actual += 30
        elif vinculo_persona == "Pentanieto/a":
            puntaje_actual += 30
        elif vinculo_persona == "Tío/a tercero":
            puntaje_actual += 30
        elif vinculo_persona == "Sobrino/a tercero":
            puntaje_actual += 30
        else:
            pass

        print("Ancestros comunes encontrados:")
        print(f"Eres el {vinculo_jugador} de esta persona!!")
        print(f"Esta persona es tu {vinculo_persona}!!")
        print(puntaje_actual)
        tupla = (puntaje_actual, f"Es tu {vinculo_persona}")
    else:
        print("No se encontraron ancestros comunes.")
        tupla = (puntaje_actual, "No tiene ningun vinculo.")
    
    return tupla






