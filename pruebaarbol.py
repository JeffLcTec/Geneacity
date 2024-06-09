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
        raices = [persona for persona in self.personas.values() if persona.padre is None and persona.madre is None]
        y_start = 80
        x_start = 200  # Ajustar la posición inicial X para acomodar múltiples raíces
        level_spacing = 100
        sibling_spacing = 100

        # Para rastrear nodos ya dibujados y evitar duplicados
        self.nodos_dibujados = set()

        for i, raiz in enumerate(raices):
            self.__ver_arbol(canvas, x_start + i * sibling_spacing, y_start, raiz, level_spacing, sibling_spacing, is_root=True)

    def __ver_arbol(self, canvas: tk.Canvas, x, y, nodo: Nodo, level_spacing, sibling_spacing, is_root=False) -> None:
        if nodo in self.nodos_dibujados:
            return

        self.nodos_dibujados.add(nodo)
        radius = 40
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline="#00BB00", fill="white", width=3)
        canvas.create_text(x, y, text=nodo.name, font=("Helvetica", 12))

        # Calcular las posiciones de los padres
        if nodo.padre and nodo.madre and not is_root:
            padre_x = x - sibling_spacing // 2
            madre_x = x + sibling_spacing // 2
            mid_x = x
            parent_y = y - level_spacing + radius

            # Línea horizontal entre los padres
            canvas.create_line(padre_x, parent_y, madre_x, parent_y, fill="black", width=2)
            # Línea vertical desde el punto medio al nodo del hijo
            canvas.create_line(mid_x, parent_y, mid_x, y - radius, fill="black", width=2)

        elif is_root:
            padre_x = x - sibling_spacing // 2
            madre_x = x + sibling_spacing // 2
            mid_x = x
            parent_y = y

        # Calcular las posiciones de los hijos
        if nodo.hijos:
            hijo_start_x = x - (len(nodo.hijos) - 1) * sibling_spacing // 2
            child_y = y + level_spacing

            for hijo in nodo.hijos:
                child_x = hijo_start_x + nodo.hijos.index(hijo) * sibling_spacing
                canvas.create_line(x, y + radius, child_x, child_y - radius, fill="black", width=2)
                self.__ver_arbol(canvas, child_x, child_y, hijo, level_spacing, sibling_spacing)

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


# Ejemplo de uso
root = tk.Tk()
root.title("Árbol Genealógico")
canvas = tk.Canvas(root, width=1000, height=800)
canvas.pack()

arbol = ArbolGenealogico()

# Crear nodos de ejemplo
nodo1 = Nodo(1, "Persona 1")
nodo2 = Nodo(2, "Persona 2")
nodo3 = Nodo(3, "Hijo 1 de Persona 1 y Persona 2")
nodo4 = Nodo(4, "Hijo 2 de Persona 1 y Persona 2")
nodo5 = Nodo(5, "Hijo 1 de Hijo 1")
nodo6 = Nodo(6, "Hijo 2 de Hijo 1")

# Agregar nodos al árbol
arbol.agregar_nodo(nodo1)
arbol.agregar_nodo(nodo2)
arbol.agregar_nodo(nodo3)
arbol.agregar_nodo(nodo4)
arbol.agregar_nodo(nodo5)
arbol.agregar_nodo(nodo6)

# Establecer relaciones
arbol.establecer_padre(3, 1)
arbol.establecer_madre(3, 2)
arbol.establecer_padre(4, 1)
arbol.establecer_madre(4, 2)
arbol.establecer_padre(5, 3)
arbol.establecer_madre(5, 4)
arbol.establecer_padre(6, 3)
arbol.establecer_madre(6, 4)

# Ver el árbol
arbol.ver_arbol(canvas, root)

root.mainloop()
