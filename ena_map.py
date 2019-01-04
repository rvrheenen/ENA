from util import Selectors, Settings
import math


class ENAMap:
    def __init__(self, squares_x, squares_y, meters_per_square):
        self.squares_x = squares_x
        self.squares_y = squares_y
        self.meters_per_square = meters_per_square
        self.squares = [[Square(y * meters_per_square, x * meters_per_square) for x in range(self.squares_y)] for y in range(self.squares_x)]

    def __repr__(self):
        return "\n".join(["|".join([str(sq) for sq in sqlist]) for sqlist in self.squares])

    def set_square_coverage(self, x, y, coverage):
        self.squares[x][y].coverage = coverage

    def add_square_feature(self, x, y, feature):
        self.squares[x][y].add_feature(feature)

    def check_squares(self):
        selectors = Selectors()
        ap_squares = self.get_squares_with_APs()
        for square in [square for sublist in self.squares for square in sublist]:
            if square.coverage:
                if selectors.get_by_repr(square.coverage).hasattr("check"):
                    square.check = ap_squares and selectors.get_by_repr(square.coverage).check > min([square.distance(ap) for ap in ap_squares])
                else:
                    square.check = True

    def get_uncovered_squares(self):
        return [square for sublist in self.squares for square in sublist if not square.check]

    def get_squares_with_APs(self):
        return [square for sublist in self.squares for square in sublist if "A" in square.features]

    def get_squares_with_uplinks(self):
        return [square for sublist in self.squares for square in sublist if "U" in square.features]

    def get_squares_with_cables(self):
        return [square for sublist in self.squares for square in sublist if "C" in [feat[:1] for feat in square.features]]

    def count_uncharted_squares(self):
        return sum([1 for sublist in self.squares for square in sublist if not square.coverage])

    def calculate_gear(self, format=False):
        settings = Settings()
        needed_slack = settings.getfloat("DISTANCES", "needed_slack")
        possible_cables = [3, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        gear = {
            "small switch" : 0,
            "large switch" : 0,
            "access point": 0,
            "cables": {c:0 for c in possible_cables},
        }

        uplink_squares = self.get_squares_with_uplinks()
        uplinks = [0 for _ in uplink_squares]  # list of amount of connections per uplink

        for ap in self.get_squares_with_APs():  # for all our Access Points
            closest_up = -1
            closet_dist = 99999999
            for i, upsq in enumerate(uplink_squares):  # find the closest uplink
                dist = ap.manhattan_distance(upsq) + needed_slack
                if dist < closet_dist:
                    closet_dist = dist
                    closest_up = i
            uplinks[closest_up] += 1  # add 1 to connection counter of the closest uplink
            gear['cables'][[c for c in possible_cables if c > closet_dist][0]] += 1  # add needed cable
            gear['access point'] += 1  # add access point

        for cab in self.get_squares_with_cables():  # for all cable squares
            closest_up = -1
            closet_dist = 99999999
            for i, upsq in enumerate(uplink_squares):  # find closest uplink
                dist = ap.manhattan_distance(upsq) + needed_slack
                if dist < closet_dist:
                    closet_dist = dist
                    closest_up = i
            uplinks[closest_up] += 1  # add 1 to connection counter of the closest uplink
            gear['cables'][[c for c in possible_cables if c > closet_dist][0]] += 1  # add needed cable
            cables_needed_at_point = [int(feat[1:]) for feat in cab.features if feat[:1] == 'C'][0]
            if cables_needed_at_point > 1:
                gear['small switch'] += 1  # add small switch
                gear['cables'][5] += cables_needed_at_point  # add 5m cables

        for i, connections in enumerate(uplinks):
            if connections > 0:
                gear['large switch'] += 1
                gear['cables'][3] += 1

        return self.format_gear(gear) if format else gear

    def format_gear(self, gear):
        string = ""
        for k, v in gear.items():
            if type(v) == int:
                string += f'{k}: {v}\n'
            elif type(v) == dict:
                string += f'{k}:\n'
                for length, amount in v.items():
                    if amount > 0:
                        string += f'  {length}m: {amount}\n'
        return string


class Square:
    def __init__(self, pos_x, pos_y, coverage=None):
        self.x = pos_x  # real x position
        self.y = pos_y  # real y position
        self.coverage = coverage
        self.features = []
        self.check = False

    def __repr__(self):
        return f'{self.x}, {self.y} {self.coverage} {"y" if self.check else "n"} {self.features}'

    def add_feature(self, feature):
        self.features.append(feature)

    def distance(self, square):
        return math.sqrt( (square.x - self.x)**2 + (square.y - self.y)**2)

    def manhattan_distance(self, square):
        return abs(square.x - self.x) + abs(square.y-self.y)
