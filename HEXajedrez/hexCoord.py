from __future__ import annotations  # Necesario para usar la clase como anotacion de tipo en sus propios miembros.
import math

class HexCoord:
    """
    Una clase contenedora sobre el concepto de una coordenada hexagonal.
    La clase proporciona sobrecargas de operadores como +, -, * y /, asi como == y !=.
    La clase tambien proporciona sobrecargas de funciones nativas como round(), hash() y abs().
    Esto permite una interfaz Pythonic con geometria hexagonal.
    """

    def __init__(self, p: float, q: float, r: float):
        """Constructor de contenedor de coordenadas axiales/hexagonales."""
        self.p, self.q, self.r = p, q, r

    def __add__(self, other: HexCoord) -> HexCoord:
        """Suma de vectores entre dos HexCoords."""
        return HexCoord(self.p + other.p, self.q + other.q, self.r + other.r)

    def __sub__(self, other: HexCoord) -> HexCoord:
        """Resta de vectores entre dos HexCoords."""
        return HexCoord(self.p - other.p, self.q - other.q, self.r - other.r)

    def __mul__(self, other: float) -> HexCoord:
        """Multiplicacion vectorial por una escalar"""
        return HexCoord(self.p * other, self.q * other, self.r * other)

    def __truediv__(self, other: float) -> HexCoord:
        """Division vectorial por una escalar."""
        return HexCoord(self.p / other, self.q / other, self.r / other)

    def __eq__(self, other: HexCoord) -> bool:
        """Comprobacion de igualdad de componentes."""
        if type(other) is not type(self):
            return False

        return self.p == other.p and self.q == other.q and self.r == other.r

    def __round__(self, n=None) -> HexCoord:
        """Redondear al HexCoord en el que se encuentra esta coordenada."""
        rp = round(self.p)
        rq = round(self.q)
        rr = round(self.r)

        p_diff = abs(self.p - rp)
        q_diff = abs(self.q - rq)
        r_diff = abs(self.r - rr)

        diff_list = [p_diff, q_diff, r_diff]

        if max(diff_list) == p_diff:
            rp = -(rq + rr)
        elif max(diff_list) == q_diff:
            rq = -(rp + rr)
        else:
            rr = -(rp + rq)

        return HexCoord(rp, rq, rr)

    def __str__(self) -> str:
        """Una representacion facil de usar."""
        return f"({self.p}, {self.q}, {self.r})"

    def __repr__(self) -> str:
        """La representacion de un codificador."""
        return f"HexCoord({self.p}, {self.q}, {self.r})"

    def __hash__(self) -> int:
        """Hashing unico que tiene en cuenta el orden de los valores."""
        return hash((self.p, self.q, self.r))

    def __abs__(self) -> HexCoord:
        """
        Asigne cada coordenada a sus valores absolutos.
        No se garantiza que sea una coordenada hexagonal valida geometricamente despues.
        """
        return HexCoord(abs(self.p), abs(self.q), abs(self.r))

    def __iter__(self) -> iter:
        
        """Retorna un iterador sobre los componentes de la coordenada."""
        return iter([self.p, self.q, self.r])

    def mag(self) -> float:
        return math.sqrt(self.p**2 + self.q**2 + self.r**2)
