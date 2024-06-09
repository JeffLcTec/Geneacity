import tkinter as tk
from tkinter import messagebox, font
import json
from PIL import Image, ImageTk
import sys
import prueba
from arbol import *
 

def cerrar_juego():
    """En caso de cerrar la ventana, se ejecutará esta función para cerrar el programa.
    """
    sys.exit()

def menu_inicio():
    
    def resize_image(image_path, width, height):
        try:
            image = Image.open(image_path)
            resized_image = image.resize((width, height), Image.LANCZOS)
            return ImageTk.PhotoImage(resized_image)
        except Exception as e:
            return None

    # Crear la ventana principal
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", cerrar_juego)
    root.geometry("1200x700")
    root.title("Menú de Inicio")

    # Variables para las imágenes redimensionadas
    fondo = resize_image("imagenes_Proyecto3/menu/fondomenu.png", 1200, 700)  # Redimensionar al tamaño de la ventana
    titulo = resize_image("imagenes_Proyecto3/menu/titulo.png", 800, 150)  # Redimensionar el título 

    root.fondo = fondo
    root.titulo = titulo

    # Crear un lienzo para colocar el fondo y el título
    canvas = tk.Canvas(root, width=1200, height=700)
    canvas.pack(fill="both", expand=True)

    # Colocar la imagen del fondo en el lienzo
    canvas.create_image(0, 0, image=root.fondo, anchor="nw")

    # Colocar la imagen del título en el lienzo
    canvas.create_image(600, 75, image=root.titulo, anchor="n")

    # Estilos de los botones
    btn_style = {
        "font": ("Helvetica", 18, "bold"),
        "fg": "#0C7AAA",
        "bg": "#000000",  # Fondo negro
        "activeforeground": "#00FF00",
        "activebackground": "#333333",
        "bd": 5,
        "relief": "ridge"
    }

    # Crear botones con estilo futurista
    btn_nueva_partida = tk.Button(root, text="Partida nueva", **btn_style, command=lambda: prueba.nueva_partida(root))
    btn_cargar_partida = tk.Button(root, text="Cargar partida", **btn_style, command=lambda:cargar_partida(root))
    btn_ver_historial = tk.Button(root, text="Ver historial", **btn_style, command=lambda:cargar_historial())

    # Colocar los botones en el centro de la ventana
    canvas.create_window(600, 400, window=btn_nueva_partida)
    canvas.create_window(600, 500, window=btn_cargar_partida)
    canvas.create_window(600, 600, window=btn_ver_historial)

    # Ejecutar el bucle principal de la ventana
    return root


def cargar_partida(ventana):
    try:
        with open('partida_pausada.json', 'r') as file:
            partida = json.load(file)
        jugador=partida["partida actual"]["jugador"]
        puntos=partida["partida actual"]["Puntuacion"]
        prueba.cargar_partida(jugador,puntos,ventana)
    except Exception:
        pass

def cargar_historial():
    """función encargada de leer el archivo json y determinar si hay partidas guardadas o no.
    """
    try:
        with open("partidas.json", 'r') as archivo:
            partidas_guardadas = json.load(archivo)
        mostrar_historial(partidas_guardadas)
    except FileNotFoundError:
        messagebox.showinfo("Error", "No se encontraron partidas guardadas.")

def mostrar_historial(partidas_guardadas):
    """función encargada de mostrar las partidas guardadas en la ventana.

    Args:
        partidas_guardadas (_type_): los diferentes datos almacenados en el archivo json
    """
    ventana_partidas = tk.Toplevel()
    ventana_partidas.geometry("400x540")
    ventana_partidas.title("Partidas Guardadas")

    etiqueta = tk.Label(ventana_partidas, text="Selecciona una partida:")
    etiqueta.pack()

    estilo_texto = font.Font(family="Arial", size=25)

    lista_partidas = tk.Listbox(ventana_partidas, selectmode=tk.SINGLE, font= estilo_texto)
    for partida in partidas_guardadas:
        lista_partidas.insert(tk.END, partida)
    lista_partidas.config(justify=tk.CENTER)
    lista_partidas.pack(fill="both", expand=True)

    def ver_historial():
        seleccion = lista_partidas.curselection()
        if seleccion:
            indice = seleccion[0]
            nombre_partida = lista_partidas.get(indice)
            partida_seleccionada = partidas_guardadas[nombre_partida]
            arbol_dict = partida_seleccionada['Arbol']
        arbol = dict_a_arbol(arbol_dict)
        ventana = tk.Tk()
        screen_width = ventana.winfo_screenwidth()
        arbol.posiciones = arbol.calcular_posiciones(screen_width)
        ventana.destroy()
        prueba.ver_familia(arbol,Ver=True)

    boton_cargar = tk.Button(ventana_partidas, text="ver puntuación", command=ver_historial)
    boton_cargar.pack(pady=10)
