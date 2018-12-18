from util import Selectors
import math


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

    def check_squares(self):
        selectors = Selectors()
        ap_squares = self.get_squares_with_APs()
        print(ap_squares)
        for square in [square for sublist in self.squares for square in sublist]:
            if square.coverage:
                # print(square, min([square.distance(ap) for ap in ap_squares]))
                square.check = ap_squares and selectors.get_by_repr(square.coverage).check > min([square.distance(ap) for ap in ap_squares])

    def get_uncovered_squares(self):
        return [square for sublist in self.squares for square in sublist if not square.check]

    def get_squares_with_APs(self):
        return [square for sublist in self.squares for square in sublist if "A" in square.features]

    def count_uncharted_squares(self):
        return sum([1 for sublist in self.squares for square in sublist if not square.coverage])


class Square:
    def __init__(self, pos_x, pos_y, coverage=None):
        self.x = pos_x  # real x position
        self.y = pos_y  # real y position
        self.coverage = coverage
        self.features = []
        self.check = False

    def __repr__(self):
        return f'{self.x}, {self.y} {self.coverage}'

    def add_feature(self, feature):
        self.features.append(feature)

    def distance(self, square):
        return math.sqrt( (square.x - self.x)**2 + (square.y - self.y)**2)
