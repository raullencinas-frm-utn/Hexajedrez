from hexCoord import HexCoord

class HexCasilla:
    """Una clase para agrupar una coordenada en el tablero y su estado correspondiente."""
    def __init__(self, coordenada: HexCoord, estado=None):
        """Constructor de una casilla hexagonal."""
        self.coordenada = coordenada
        self.estado = estado