# Geneacity

A 2D city-simulation game where family trees are the core mechanic. Built in Python as a university project.

## What it does

- Pick an inhabitant of the city and walk around a tiled map (WASD) with sprite animation
- Request nearby houses and open each resident's info panel (name, age, marital status, gender)
- **Similarity:** compares your family tree with another person's and scores the shared ancestors
- **Marriage and reproduction:** unions and children update your family tree
- **Family tree viewer:** full-screen visualization of the tree (Tkinter canvas)
- **Save / load:** game state, including the tree, is stored as JSON; pause and resume supported

## Tech

Python · Pygame · Tkinter · Pillow · requests

Data comes from a REST API; the family tree is a custom graph structure (`arbol.py`) with ancestor lookup, kinship labels and serialization.

## Project structure

| File | Role |
|---|---|
| `main.py` / `menu.py` | Entry point and start menu |
| `juego.py` | Main game loop and UI |
| `arbol.py` | Genealogical tree (nodes, ancestors, kinship, similarity) |
| `API_request.py` | HTTP client for the game API |
| `guardar_partidas.py` | Save / load logic |
| `utilidades.py` | Shared sprites and helpers |

## Run it

```bash
pip install pygame pillow requests
python main.py
```
