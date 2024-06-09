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
        self.memo = {}

    def agregar_nodo(self, nodo):
        if nodo.id not in self.personas:
            self.personas[nodo.id] = nodo

    def establecer_padre(self, id_nodo, id_padre):
        if id_nodo in self.personas and id_padre in self.personas:
            if not any(hijo.id == id_nodo for hijo in self.personas[id_padre].hijos):
                self.personas[id_nodo].padre = self.personas[id_padre]
                self.personas[id_padre].hijos.append(self.personas[id_nodo])

    def establecer_madre(self, id_nodo, id_madre):
        if id_nodo in self.personas and id_madre in self.personas:
            if not any(hijo.id == id_nodo for hijo in self.personas[id_madre].hijos):
                self.personas[id_nodo].madre = self.personas[id_madre]
                self.personas[id_madre].hijos.append(self.personas[id_nodo])

    def calcular_posicion_nueva_persona(self, id_padre, id_madre):
        if id_padre in self.posiciones and id_madre in self.posiciones:
            x_padre, y_padre = self.posiciones[id_padre]
            x_madre, y_madre = self.posiciones[id_madre]
            num_hijos = max(len(self.personas[id_padre].hijos), len(self.personas[id_madre].hijos))
            x_nuevo = (x_padre + x_madre) // 2
            if y_madre>y_padre:
                y_nuevo = y_madre + 50
            else:
                y_nuevo = y_padre +50
            if num_hijos > 0:
                x_nuevo -= (num_hijos-1) * 50
            return x_nuevo, y_nuevo
        return None

    def calcular_posiciones(self,screen):
        posiciones = {}
        y_step = 50
        x_center = screen//2
        x_gap = 100  # Espacio horizontal entre los nodos hijos
        y_start = 50  # Y inicial para los padres

        # Encuentra los nodos que no tienen padres ni madres, es decir, los ancestros iniciales
        padres = [nodo for nodo in self.personas.values() if not nodo.padre and not nodo.madre]

        if len(padres) >= 2:
            posiciones[padres[0].id] = (x_center - x_gap // 2, y_start)
            posiciones[padres[1].id] = (x_center + x_gap // 2, y_start)

        def contar_descendientes(nodo):
            if not nodo.hijos:
                return 1
            return sum(contar_descendientes(hijo) for hijo in nodo.hijos)

        def posicionar_hijos(nodo, x, y):
            hijos = nodo.hijos
            num_hijos = len(hijos)
            if num_hijos > 0:
                total_width = (num_hijos -1)* x_gap
                x_start = x - total_width // 2 + x_gap // 2
                for i, hijo in enumerate(hijos):
                    if hijo.id in posiciones:
                        y_nuevo = y + y_step
                        if y_nuevo<posiciones[hijo.id][1]:
                            y_nuevo=posiciones[hijo.id][1]
                        posiciones[hijo.id] = (posiciones[hijo.id][0], y_nuevo)
                        posicionar_hijos(hijo, posiciones[hijo.id][0], y_nuevo)
                        break
                    y_nuevo = y + y_step
                    x_nuevo = x_start + i * 50
                    
                    posiciones[hijo.id] = (x_nuevo, y_nuevo)
                    posicionar_hijos(hijo, x_nuevo, y_nuevo)

        for padre in padres:
            posicionar_hijos(padre, *posiciones[padre.id])

        return posiciones




    def dibujar_arbol(self, canvas):
        for id_nodo, pos in self.posiciones.items():
            self.dibujar_nodo(canvas, id_nodo, pos)

    def dibujar_nodo(self, canvas, id_nodo, pos):
        nodo = self.personas[id_nodo]
        x, y = pos
        canvas.create_oval(x-20, y-20, x+20, y+20, fill='white')
        canvas.create_text(x, y, text=nodo.name)
        if nodo.padre and nodo.padre.id in self.posiciones:
            x_padre, y_padre = self.posiciones[nodo.padre.id]
            canvas.create_line(x, y-20, x_padre, y_padre+20)
        if nodo.madre and nodo.madre.id in self.posiciones:
            x_madre, y_madre = self.posiciones[nodo.madre.id]
            canvas.create_line(x, y-20, x_madre, y_madre+20)

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
        if persona.id in ancestros:
            return
        vinculo = ["Ego", "Padre/Madre", "Abuelo/Abuela", "Bisabuelo/Bisabuela", "Tatarabuelo/Tatarabuela","Trastatarabuelo/Trastatarabuela","Pentabuelo/Pentabuela"]
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
        tupla = (puntaje_actual, f"Es tu {vinculo_persona}",arbol2.personas[persona["id"]])
    else:
        print("No se encontraron ancestros comunes.")
        tupla = (puntaje_actual, "No tiene ningun vinculo o se desconoce.",None)
    
    return tupla






