import math

from pixel import PixelCoord
from hexcoord import HexCoord

class HexPixelAdapter:
    """Una clase que proporciona métodos auxiliares para convertir fácilmente entre `PixelCoord`s y `HexCoord`s."""
    def __init__(self, dimensiones: PixelCoord, origen: PixelCoord, radio: float):
        self.dimensiones: PixelCoord = dimensiones
        self.origen: PixelCoord = origen
        self.radioHexagonal: float = radio

    def hex_to_pixel(self, coordenada: HexCoord) -> PixelCoord:
        """Convierte de `HexCoord` a `PixelCoord`."""
        x: float = self.radioHexagonal * 1.5 * coordenada.p + self.origen.x
        y: float = self.radioHexagonal * (math.sqrt(3) * 0.5 * coordenada.p + math.sqrt(3) * coordenada.r) + self.origen.y

        return PixelCoord(x, y)

    def pixel_to_hex(self, coordenada: PixelCoord) -> HexCoord:
        """Convierte de `PixelCoord` a `HexCoord`."""

        coordenada -= self.origen

        p: float = 2 / 3 * coordenada.x / self.radioHexagonal
        r: float = (-1 / 3 * coordenada.x + math.sqrt(3) / 3 * coordenada.y) / self.radioHexagonal

        return HexCoord(p, -p - r, r)

    def get_vertices(self, coordenada: HexCoord) -> list[PixelCoord]:
        """Obtiene los vértices `PixelCoord` de un hexadecimal en cualquier `HexCoord`."""
        x, y = self.hex_to_pixel(coordenada)
        angulo: float = math.pi / 3

        return [PixelCoord(
            self.radioHexagonal * math.cos(angulo * i) + x,
            self.radioHexagonal * math.sin(angulo * i) + y
        ) for i in range(6)]
