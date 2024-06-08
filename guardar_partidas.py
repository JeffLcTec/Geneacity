import json

def guardar_partida(datos, archivo):
    """
    Guarda los datos en un archivo JSON.

    Args:
        datos (dict): Un diccionario con los datos a almacenar.
        archivo (str): El nombre del archivo JSON.

    Returns:
        None
    """
    try:
        with open(archivo, 'w') as f:
            json.dump(datos, f, indent=4)
        print(f"Los datos se han guardado en el archivo '{archivo}' correctamente.")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")

def crear_partida(jugador: dict, puntos: int, pos: tuple):
    """
    Crea una nueva partida con los datos del jugador.

    Args:
        jugador (dict): Diccionario con los datos del jugador.
        puntos (int): Puntuación del jugador.
        pos (tuple): Posición del jugador.

    Returns:
        None
    """
    partida = {"jugador": jugador, "Puntuacion": puntos, "Posicion": pos}

    try:
        with open("partidas.json", 'r') as archivo:
            try:
                partidas_guardadas = json.load(archivo)
            except json.JSONDecodeError:
                partidas_guardadas = {}
    except FileNotFoundError:
        partidas_guardadas = {}


    # Agregar la nueva partida
    partidas_guardadas[f"partida de {jugador["name"]}"] = partida

    # Guardar las partidas de nuevo en el archivo
    guardar_partida(partidas_guardadas, "partidas.json")

    print(f"Partida guardada como 'partida de {jugador["name"]}'.")

