from math import sqrt
from dataclasses import dataclass
from shapely.geometry import Point

class PositionalConstants:
    ONE_METER_X = 0.00001425
    ONE_METER_Y = 0.000008989
    # ONE_METER_X = 0
    # FIELD_SIZE_X = 0
    # SIZE_X = 0
    # WIDTH_X = 0

    # ONE_METER_Y = 0
    # FIELD_SIZE_Y = 0
    # SIZE_Y = 0
    # HEIGHT_Y = 0
    # FIELD_DIAGONAL = 0
    # SOURCE = 0

    def __init__(self, source, cell_count_x, cell_size_x, cell_count_y, cell_size_y):
        self.SOURCE = source
        
        self.FIELD_SIZE_X = cell_size_x * self.ONE_METER_X
        self.SIZE_X = cell_count_x
        self.WIDTH_X = self.FIELD_SIZE_X * self.SIZE_X
        self.WIDTH_X_meter = cell_size_x * self.SIZE_X
        
        self.FIELD_SIZE_Y = cell_size_y * self.ONE_METER_Y
        self.SIZE_Y = cell_count_y
        self.HEIGHT_Y = self.FIELD_SIZE_Y * self.SIZE_Y
        self.HEIGHT_Y_meter = cell_size_y * self.SIZE_Y
        
        self.FIELD_DIAGONAL = int(sqrt(self.FIELD_SIZE_X**2 + self.FIELD_SIZE_Y**2))
    
    def get_middle(self):
        return [self.SOURCE.x + self.WIDTH_X / 2, self.SOURCE.y + self.HEIGHT_Y / 2]
    
    def get_max_distance(self):
        print(self.WIDTH_X)
        print(self.HEIGHT_Y)
        return sqrt(self.WIDTH_X_meter**2 + self.HEIGHT_Y_meter**2)


# SOURCE = Point(50.054153, 14.347182)
# SOURCE = Point(14.445755, 50.085048)
# SOURCE = Point(14.443862, 50.085356) # Zizkov, Karlin
# SOURCE = Point(14.38857, 50.10448) # CVUT campus
# SOURCE = Point(14.37269, 50.05504) # Radlice
# SOURCE = Point(14.42898, 50.08839)  # Namesti Republiky
# SOURCE = Point(14.42108, 50.06247) #Vysehrad
