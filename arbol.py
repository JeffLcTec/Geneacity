import tkinter as tk


class Nodo:
    def __init__(self, id, name):
        """
        Inicializa un nodo con un identificador y un nombre.

        :param id: Identificador único del nodo.
        :param name: Nombre del nodo.
        """
        self.id = id
        self.name = name
        self.padre = None
        self.madre = None
        self.hijos = []

    def __str__(self) -> str:
        
        return f"({self.id}, {self.name})"

    def a_dict(self):
        """
        Convierte el nodo a un diccionario.

        return: 
            Diccionario con la información del nodo.
        """
        return {
            'id': self.id,
            'name': self.name,
            'padre': self.padre.id if self.padre else None,
            'madre': self.madre.id if self.madre else None,
            'hijos': [hijo.id for hijo in self.hijos]
        }

    @staticmethod
    def de_dict(diccionario):
        """
        Crea un nodo a partir de un diccionario.

        :param diccionario: Diccionario con la información del nodo.
        :return: Nodo creado a partir del diccionario.
        """
        persona = Nodo(diccionario['id'], diccionario['name'])
        # No establecemos padre, madre o hijos aún, porque pueden no haber sido creados.
        return persona

class ArbolGenealogico:
    def __init__(self):
        self.personas = {}
        self.nodos_dibujados = set()
        self.memo = {}

    def agregar_nodo(self, nodo):
        """
        Agrega un nodo al árbol.

        :param nodo: Nodo a agregar.
        """
        if nodo.id not in self.personas:
            self.personas[nodo.id] = nodo

    def establecer_padre(self, id_nodo, id_padre):
        """
        Establece el padre de un nodo.

        :param id_nodo: Identificador del nodo hijo.
        :param id_padre: Identificador del nodo padre.
        """
        if id_nodo in self.personas and id_padre in self.personas:
            if not any(hijo.id == id_nodo for hijo in self.personas[id_padre].hijos):
                self.personas[id_nodo].padre = self.personas[id_padre]
                self.personas[id_padre].hijos.append(self.personas[id_nodo])

    def establecer_madre(self, id_nodo, id_madre):
        """
        Establece la madre de un nodo.

        :param id_nodo: Identificador del nodo hijo.
        :param id_madre: Identificador del nodo madre.
        """
        if id_nodo in self.personas and id_madre in self.personas:
            if not any(hijo.id == id_nodo for hijo in self.personas[id_madre].hijos):
                self.personas[id_nodo].madre = self.personas[id_madre]
                self.personas[id_madre].hijos.append(self.personas[id_nodo])

    def a_dict(self):
        """
        Convierte el árbol genealógico a un diccionario.

        :return: Diccionario con la información del árbol.
        """
        return {
            'personas': {id: persona.a_dict() for id, persona in self.personas.items()}
        }

    @staticmethod
    def de_dict(diccionario):
        arbol = ArbolGenealogico()
        # Crear todas las personas primero
        for id, persona_dict in diccionario['personas'].items():
            arbol.agregar_nodo(Nodo.de_dict(persona_dict))
        # Luego establecer las relaciones
        for id, persona_dict in diccionario['personas'].items():
            persona = arbol.personas[id]
            if persona_dict['padre'] is not None:
                arbol.establecer_padre(id, persona_dict['padre'])
            if persona_dict['madre'] is not None:
                arbol.establecer_madre(id, persona_dict['madre'])
        return arbol

    def calcular_posicion_nueva_persona(self, id_padre, id_madre):
        """
        Calcula la posición de una nueva persona en el árbol.

        :param id_padre: Identificador del padre.
        :param id_madre: Identificador de la madre.
        :return: Tupla con la posición (x, y) de la nueva persona.
        """
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
        """
        Calcula las posiciones de todos los nodos en el árbol.

        :param screen: Ancho de la pantalla para centrar los nodos.
        :return: Diccionario con las posiciones de cada nodo.
        """
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
            """cuenta cuantos hijos tiene un nodo

    
            Returns:
                descendientes
            """
            if not nodo.hijos:
                return 1
            return sum(contar_descendientes(hijo) for hijo in nodo.hijos)

        def posicionar_hijos(nodo, x, y):
            """Establece las posiciones de los hijos

            Args:
                nodo (_type_): padre
                x (_type_): x
                y (_type_): y
            """
            hijos = nodo.hijos
            num_hijos = len(hijos)
            if num_hijos > 0:
                total_width = (num_hijos -1)* x_gap
                x_start = x - total_width // 2 + x_gap // 2
                for i, hijo in enumerate(hijos):
                    if hijo==None:
                        pass
                    else:
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
        """
        Dibuja el árbol genealógico en un canvas.

        :param canvas: Canvas de tkinter donde se dibujará el árbol.
        """
        for id_nodo, pos in self.posiciones.items():
            self.dibujar_nodo(canvas, id_nodo, pos)

    def dibujar_nodo(self, canvas, id_nodo, pos):
        """
        Dibuja un nodo en el canvas.

        :param canvas: Canvas de tkinter donde se dibujará el nodo.
        :param id_nodo: Identificador del nodo a dibujar.
        :param pos: Posición (x, y) donde se dibujará el nodo.
        """
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
        """
        Obtiene todos los ancestros de una persona.

        :param id_persona: Identificador de la persona.
        :return: Conjunto de ancestros.
        """
        ancestros = set()
        self._obtener_ancestros_recursivo(self.personas[id_persona], ancestros)
        return ancestros

    def _obtener_ancestros_recursivo(self, persona, ancestros):
        """
        Método recursivo para obtener ancestros de una persona.

        :param persona: Persona actual.
        :param ancestros: Conjunto de ancestros.
        """
        if persona is None:
            return
        ancestros.add((persona.id, persona.name))
        self._obtener_ancestros_recursivo(persona.padre, ancestros)
        self._obtener_ancestros_recursivo(persona.madre, ancestros)

    def obtener_ancestros_con_distancia(self, id_persona):
        """
        Obtiene todos los ancestros de una persona junto con su distancia.

        :param id_persona: Identificador de la persona.
        :return: Diccionario de ancestros con su distancia.
        """
        ancestros = {}
        self._obtener_ancestros_recursivo(self.personas[id_persona], ancestros, 0)
        return ancestros

    def _obtener_ancestros_recursivo(self, persona, ancestros, distancia):
        """
        Método recursivo para obtener ancestros de una persona junto con su distancia.

        :param persona: Persona actual.
        :param ancestros: Diccionario de ancestros con su distancia.
        :param distancia: Distancia actual.
        """
        if persona is None:
            return
        if persona.id in ancestros:
            return
        vinculo = ["Ego", "Padre/Madre", "Abuelo/Abuela", "Bisabuelo/Bisabuela", "Tatarabuelo/Tatarabuela","Trastatarabuelo/Trastatarabuela","Pentabuelo/Pentabuela"]
        ancestros[persona.id] = (persona.name, distancia, vinculo[min(distancia, len(vinculo) - 1)])
        self._obtener_ancestros_recursivo(persona.padre, ancestros, distancia + 1)
        self._obtener_ancestros_recursivo(persona.madre, ancestros, distancia + 1)

def nodo_a_dict(nodo, visitados):
    """
    Convierte un nodo a un diccionario.

    :param nodo: Nodo a convertir.
    :param visitados: Conjunto de nodos ya visitados.
    :return: Diccionario con la información del nodo.
    """
    if not nodo or nodo.id in visitados:
        return None

    visitados.add(nodo.id)

    return {
        "id": nodo.id,
        "name": nodo.name,
        "padre": nodo.padre.id if nodo.padre else None,
        "madre": nodo.madre.id if nodo.madre else None,
        "hijos": [nodo_a_dict(hijo, visitados) for hijo in nodo.hijos]
    }

def arbol_a_dict(arbol):
    """
    Convierte un árbol genealógico a un diccionario.

    :param arbol: Árbol genealógico a convertir.
    :return: Diccionario con la información del árbol.
    """
    visitados = set()
    return {id: nodo_a_dict(nodo, visitados) for id, nodo in arbol.personas.items()}

def dict_a_nodo(nodo_dict, nodos):
    """
    Crea un nodo a partir de un diccionario.

    :param nodo_dict: Diccionario con la información del nodo.
    :param nodos: Diccionario de nodos ya creados.
    :return: Nodo creado a partir del diccionario.
    """
    if not nodo_dict:
        return None

    if nodo_dict['id'] in nodos:
        return nodos[nodo_dict['id']]

    nodo = Nodo(nodo_dict['id'], nodo_dict['name'])
    nodos[nodo_dict['id']] = nodo

    if nodo_dict['padre']:
        nodo.padre = dict_a_nodo(nodo_dict['padre'], nodos)
        nodo.padre.hijos.append(nodo)

    if nodo_dict['madre']:
        nodo.madre = dict_a_nodo(nodo_dict['madre'], nodos)
        nodo.madre.hijos.append(nodo)

    for hijo_dict in nodo_dict['hijos']:
        hijo = dict_a_nodo(hijo_dict, nodos)
        nodo.hijos.append(hijo)

    return nodo

def dict_a_arbol(arbol_dict):
    """
    Crea un árbol genealógico a partir de un diccionario.

    :param arbol_dict: Diccionario con la información del árbol.
    :return: Árbol genealógico creado a partir del diccionario.
    """
    arbol = ArbolGenealogico()
    nodos = {}

    for id, nodo_dict in arbol_dict.items():
        dict_a_nodo(nodo_dict, nodos)

    arbol.personas = nodos
    return arbol

def determinar_vinculo(relacion_jugador, relacion_persona):
    """
    Determina el vínculo entre dos personas basado en su relación.

    :param relacion_jugador: Relación del jugador.
    :param relacion_persona: Relación de la otra persona.
    :return: Vínculo determinado.
    """
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
    """
    Busca la similitud entre dos personas en dos árboles genealógicos.

    :param jugador: Diccionario con la información del jugador.
    :param persona: Diccionario con la información de la otra persona.
    :param arbol1: Primer árbol genealógico.
    :param arbol2: Segundo árbol genealógico.
    :return: Tupla con el puntaje, la relación y el nodo de la persona.
    """
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
        if vinculo_persona=="Relacionnlejana":
            tupla = (puntaje_actual, f"tiene una {vinculo_persona}",arbol2.personas[persona["id"]])
        else:
            tupla = (puntaje_actual, f"Es tu {vinculo_persona}",arbol2.personas[persona["id"]])
    else:
        print("No se encontraron ancestros comunes.")
        tupla = (puntaje_actual, "No tiene ningun vinculo o se desconoce.",None)
    
    return tupla






