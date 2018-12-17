class ENAMap:
    def __init__(self, squares_x, squares_y, meters_per_square):
        self.squares_x = squares_x
        self.squares_y = squares_y
        self.meters_per_square = meters_per_square
        self.squares = [[Square(x * meters_per_square, y * meters_per_square) for x in range(self.squares_y)] for y in range(self.squares_x)]

    def __repr__(self):
        return "\n".join(["|".join([str(sq) for sq in sqlist]) for sqlist in self.squares])

    def set_square_coverage(self, x, y, coverage):
        self.squares[x][y].coverage = coverage

    def add_square_feature(self, x, y, feature):
        self.squares[x][y].add_feature(feature)

class Square:
    def __init__(self, pos_x, pos_y, coverage=None):
        self.x = pos_x # real x position
        self.y = pos_y # real y position
        self.coverage = coverage
        self.features = []

    def __repr__(self):
        return f'{self.x}, {self.y} {self.coverage}'

    def add_feature(self, feature):
        self.features.append(feature)
