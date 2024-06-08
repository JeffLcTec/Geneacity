import tkinter as tk
from PIL import Image, ImageTk
import sys
from prueba import nueva_partida, cargar_partida

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
    btn_nueva_partida = tk.Button(root, text="Partida nueva", **btn_style, command=lambda: nueva_partida(root))
    btn_cargar_partida = tk.Button(root, text="Cargar partida", **btn_style, command=cargar_partida())

    # Colocar los botones en el centro de la ventana
    canvas.create_window(600, 400, window=btn_nueva_partida)
    canvas.create_window(600, 500, window=btn_cargar_partida)

    # Ejecutar el bucle principal de la ventana
    return root

if __name__ == "__main__":
    menu_inicio()
