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
    except Exception as e:
        print(f"Error al guardar el archivo {archivo}: {e}")

def guardar_partida_pausada(partida, archivo):
    """
    Guarda una única partida en un archivo JSON.

    Args:
        partida (dict): Diccionario con los datos de la partida.
        archivo (str): El nombre del archivo JSON.

    Returns:
        None
    """
    try:
        with open(archivo, 'w') as f:
            json.dump(partida, f, indent=4)
    except Exception as e:
        print(f"Error al guardar el archivo {archivo}: {e}")

def crear_partida(jugador: dict, puntos: int, arbol:dict):
    """
    Crea una nueva partida con los datos del jugador.

    Args:
        jugador (dict): Diccionario con los datos del jugador.
        puntos (int): Puntuación del jugador.

    Returns:
        None
    """
    partida = {"jugador": jugador, "Puntuacion": puntos, "Arbol": arbol}

    try:
        with open("partidas.json", 'r') as archivo:
            try:
                partidas_guardadas = json.load(archivo)
            except json.JSONDecodeError:
                partidas_guardadas = {}
    except FileNotFoundError:
        partidas_guardadas = {}

    try:
        with open("partida_pausada.json", 'r') as archivo:
            try:
                partida_pausada = json.load(archivo)
            except json.JSONDecodeError:
                partida_pausada = {}
    except FileNotFoundError:
        partida_pausada = {}

    # Agregar la nueva partida
    partidas_guardadas[f"partida de {jugador['name']}"] = partida
    partida_pausada["partida actual"] = partida

    # Guardar las partidas de nuevo en el archivo
    guardar_partida(partidas_guardadas, "partidas.json")

    # Guardar la partida pausada en un archivo separado
    guardar_partida_pausada(partida_pausada, "partida_pausada.json")
