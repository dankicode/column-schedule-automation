
class Column:
    def __init__(self,
                 x: float,
                 y: float,
                 z: float,
                 level: str,
                 size: str,
                 reinforcement: str,
                 column_number: str,
                 fpc: float,
                 dead_load: float,
                 live_load: float,
                 wind_load: float,
                 seismic_load: float,
                 column_UID: int,
                 member_below: int,
                 column_above: int,
                 story_height: float,
                 grid_label: str,
                 ):
        self.x = x
        self.y = y
        self.z = z
        self.level = level
        self.size = size
        self.reinforcement = reinforcement
        self.column_number = column_number
        self.fpc = fpc
        self.dead_load = dead_load
        self.live_load = live_load
        self.wind_load = wind_load
        self.seismic_load = seismic_load
        self.column_UID = column_UID
        self.member_below = member_below
        self.column_above = column_above
        self.story_height = story_height
        self.grid_label = grid_label

    def calculate_load_combinations(self):
        pass

