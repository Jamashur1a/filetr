import random

class Generate_Map():
    def __init__(self):
        self.rows = None
        self.columns = None
        self.bombs = None
        self.game_map = None

    def Generate(self, rows, columns, bombs):
        self.rows = rows
        self.columns = columns
        self.bombs = bombs
        [[[] for _ in range(self.columns)] for _ in range(self.rows)]
        self.Place_Bombs()
        self.generate_info()

        return self.game_map


    def Place_Bombs(self):
        counted_bombs = 0
        while counted_bombs < self.bombs:
            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.columns - 1)
            if self.game_map[x][y] != 9:
                self.game_map[x][y] = 9
                counted_bombs += 1
        


    def generate_info(self):
        for rows in range(len(self.game_map)):
            for columns in range(len(self.game_map[0])):
                if self.game_map[rows][columns] == 9:
                    continue
                around_bombs = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if rows + x < 0 or rows + x >= len(self.game_map) or columns + y < 0 or columns + y >= len(self.game_map[0]):
                            continue
                        if self.game_map[rows + x][columns + y] == 9:
                            around_bombs += 1
                self.game_map[rows][columns] = around_bombs
