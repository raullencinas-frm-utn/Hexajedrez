import math

class PixelCoord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return PixelCoord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return PixelCoord(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return PixelCoord(self.x * other, self.y * other)

    def __truediv__(self, other):
        return PixelCoord(self.x / other, self.y / other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __round__(self, n=None):
        PixelCoord(round(self.x), round(self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __iter__(self):
        return iter([self.x, self.y])

    def __getitem__(self, item):
        return [self.x, self.y][item]

    def __len__(self):
        return 2

    def mag(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)
