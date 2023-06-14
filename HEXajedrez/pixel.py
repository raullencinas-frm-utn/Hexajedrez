import math

class PixelCoord:
    """Clase contenedora de coordenadas x,y en pixeles."""
    def __init__(self, x, y):
        """Constructor de el contenedor de coordenadas."""
        self.x = x
        self.y = y

    def __add__(self, other):
        """Sobrecarga de suma."""
        return PixelCoord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Sobrecarga de resta."""
        return PixelCoord(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """Sobrecarga de multiplicación."""
        return PixelCoord(self.x * other, self.y * other)

    def __truediv__(self, other):
        """Sobrecarga de división."""
        return PixelCoord(self.x / other, self.y / other)

    def __eq__(self, other):
        """Sobrecarga de igualdad."""
        return self.x == other.x and self.y == other.y

    def __round__(self, n=None):
        """Sobrecarga de redondeo."""
        PixelCoord(round(self.x), round(self.y))

    def __str__(self):
        """Metodo de mostrar como string."""
        return f"({self.x}, {self.y})"

    def __iter__(self):
        """Sobrecarga de iterador."""
        return iter([self.x, self.y])

    def __getitem__(self, item):
        """Sobrecarga para recibir item del mismo."""
        return [self.x, self.y][item]

    def __len__(self):
        """Sobrecarga de metodo que indica su longitud."""
        return 2

    def mag(self) -> float:
        """Método que potencia coordenadas."""
        return math.sqrt(self.x**2 + self.y**2)
