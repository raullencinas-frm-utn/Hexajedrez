from hexCoord import HexCoord

class HexCelda:
    """Una clase para agrupar una coordenada en el tablero y su estado correspondiente."""
    def __init__(self, coordenada: HexCoord, estado=None):
        """Constructor de una celda hexagonal."""
        self.coordenada = coordenada
        self.estado = estado
    
    def __str__(self) -> str:
        hash_str = self.estado + str(self.coordenada.p) + str(self.coordenada.q) + str(self.coordenada.r)
        return hash_str