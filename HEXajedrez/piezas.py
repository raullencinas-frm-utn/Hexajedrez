import pygame


class Piezas:

    nombres = ("peon", "torre", "caballo", "alfil", "rey", "dama")

    def __init__(self, colores: str):
        """Constructor de una pieza."""
        self.colores = colores

    def piezasImagenes(self, colores: str) -> dict[str, pygame.Surface]:
        """Devuelve un diccionario con las imagenes de las piezas del color ingresado."""
        return {
            nombresDePiezas: pygame.transform.scale(
                pygame.image.load(
                    f"img/{nombresDePiezas}.png").convert_alpha(),
                (60, 60)
            )
            for nombresDePiezas in [f"{color}_{nombre}" for color in self.colores for nombre in self.nombres]
        }

    def movimientos(self) -> dict[str, list]:
        """Devuelve un diccionario de los movimientos de las piezas en coordenadas axiales / hexagonales."""
        movimientos = {**dict.fromkeys([f"{color}_alfil" for color in self.colores], [
            (2, -1, -1), (-2, 1, 1),
            (-1, 2, -1), (1, -2, 1),
            (-1, -1, 2), (1, 1, -2)
        ]),

            **dict.fromkeys([f"{color}_torre" for color in self.colores], [
                (0, 1, -1), (0, -1, 1),
                (1, 0, -1), (-1, 0, 1),
                (1, -1, 0), (-1, 1, 0)
            ]),

            **dict.fromkeys([f"{color}_rey" for color in self.colores], [
                (0, 1, -1), (0, -1, 1),
                (1, 0, -1), (-1, 0, 1),
                (1, -1, 0), (-1, 1, 0),
                (2, -1, -1), (-2, 1, 1),
                (-1, 2, -1), (1, -2, 1),
                (-1, -1, 2), (1, 1, -2)
            ]),

            **dict.fromkeys([f"{color}_dama" for color in self.colores], [
                (0, 1, -1), (0, -1, 1),
                (1, 0, -1), (-1, 0, 1),
                (1, -1, 0), (-1, 1, 0),
                (2, -1, -1), (-2, 1, 1),
                (-1, 2, -1), (1, -2, 1),
                (-1, -1, 2), (1, 1, -2)
            ]),

            **dict.fromkeys([f"{color}_caballo" for color in self.colores], [
                (2, 1, -3), (3, -1, -2),
                (-1, 3, -2), (1, 2, -3),
                (-2, 3, -1), (-3, 2, 1),
                (-3, 1, 2), (-2, -1, 3),
                (-1, -2, 3), (1, -3, 2),
                (2, -3, 1), (3, -2, -1)
            ]),

            "b_peon": [
            (0, 1, -1),
            (-1, 1, 0),
            (1, 0, -1)
        ]
        }
        if self.colores.endswith("r"):
            movimientos["n_peon"] = [(1, -1, 0), (0, -1, 1), (1, 0, -1)]
            movimientos["r_peon"] = [(-1, 0, 1), (0, -1, 1), (-1, 1, 0)]
        else:
            movimientos["n_peon"] = [(0, -1, 1), (1, -1, 0), (-1, 0, 1)]

        return movimientos
