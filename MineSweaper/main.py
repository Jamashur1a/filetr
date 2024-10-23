import pygame
import random
import Data_Manager
import Generate_Map

class MineSweeper:
    def __init__(self,game_mode):
        pygame.init()
        self.filled_text = 0
        self.bomb_index = 9
        self.rows = None
        self.cols = None
        self.filled_text = 0
        self.screen_width = None
        self.screen_height = None
        self.game_mode = game_mode
        self.opened_cells = None
        self.opened_cells_count = None

        self.flags = None
        self.falgs_count = None

        self.data_manager = Data_Manager.DataManager() 
        self.game_data = None

        self.Map_Generator = Generate_Map.Generate_Map()
        self.Start_Game()

        self.rect_size = self.screen_width / self.rows



        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()


        self.click_count = 0

    def Start_Game(self):
        self.game_data = self.data_manager.load()


        if self.game_mode > len(self.game_data["game_modes"]):
             return "Error: Invalid game mode"
        
        self.rows = self.game_data["game_modes"][str(self.game_mode)]["rows"]
        self.cols = self.game_data["game_modes"][str(self.game_mode)]["columns"]
        self.bomb = self.game_data["game_modes"][str(self.game_mode)]["bombs"]
        self.screen_width = self.game_data["game_params"]["width"]
        self.screen_height = self.game_data["game_params"]["height"]


        self.game_map = [[[] for _ in range(self.cols)] for _ in range(self.rows)]
        

        self.opened_cells = set()
        self.opened_cells_count = 0
        self.flags = set()
        self.falgs_count = 0
        self.Changes_in_Game = True
        self.generate_bombs(self.game_map)
        self.generate_info(self.game_map)
        
        #self.vizualize(self.game_map)    

    def vizualize(self, game_map):
        for columns in range(len(game_map[0])):
            for row in range(len(game_map)):
                if game_map[row][columns] == 0:
                    print(self.filled_text, " ", end="")
                if game_map[row][columns] == self.bomb_index:
                    print('*', " ", end="")
                if game_map[row][columns] > 0 and game_map[row][columns] < 9:
                    print(game_map[row][columns], " ", end="")
            print(end="\n")

    def generate_bombs(self, game_map):
        counted_bombs = 0
        while counted_bombs < self.bomb:
            x = random.randint(0, self.rows - 1)
            y = random.randint(0, self.cols - 1)
            if game_map[x][y] != self.bomb_index:
                game_map[x][y] = self.bomb_index
                counted_bombs += 1

    def generate_info(self, game_map):
        for rows in range(len(game_map)):
            for columns in range(len(game_map[0])):
                if game_map[rows][columns] == self.bomb_index:
                    continue
                around_bombs = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if rows + x < 0 or rows + x >= len(game_map) or columns + y < 0 or columns + y >= len(game_map[0]):
                            continue
                        if game_map[rows + x][columns + y] == self.bomb_index:
                            around_bombs += 1
                game_map[rows][columns] = around_bombs

    def run(self):
        pygame.display.set_caption("Mine Sweeper")
        while True:
            self.update()
            self.display()
            self.clock.tick(60)

    def display(self):
        if self.Changes_in_Game:
            self.screen.fill((150, 150, 150))
            self.Show_Opened_Cells()
            self.Display_Flags()
            self.Draw_Grid()
            pygame.display.flip()
            self.Changes_in_Game = False
        fps = int(self.clock.get_fps())
        pygame.display.set_caption(f"Mine Sweeper - {fps} FPS")

    def update(self):
        self.Input_Handler()

    def Display_Flags(self):
        font_size = int(self.rect_size)
        font = pygame.font.Font(None, font_size)
        
        for flag in self.flags:
            text_surface = font.render('F', False, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(flag[0] * self.rect_size + self.rect_size // 2, flag[1] * self.rect_size + self.rect_size // 2))
            self.screen.blit(text_surface, text_rect)

    def Draw_Grid(self):
        for x in range(0, self.screen_width, int(self.rect_size)):
            pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, self.screen_height))
        for y in range(0, self.screen_height, int(self.rect_size)):
            pygame.draw.line(self.screen, (0, 0, 0), (0, y), (self.screen_width, y))

    def mouse_fixed_position(self):
        x, y = pygame.mouse.get_pos()
        rect_size = self.screen_width / self.cols
        return int(x / rect_size), int(y / rect_size)

    def Reveal_Cells(self):
        for row in range(len(self.game_map)):
            for column in range(len(self.game_map[0])):
                self.Process_Reveal((row, column))

    def Process_Reveal(self, Map_position):
        font_size = int(self.rect_size)
        font = pygame.font.Font(None, font_size)
        info = self.game_map[Map_position[0]][Map_position[1]]
        if info == self.bomb_index:
            color = (255, 0, 0)
            text = ""
        elif info > 0 and info < 9:
            color = (255, 255, 255)
            text = str(info)
        elif info == 0:
            color = (255, 255, 255)
            text = ""
        pos_xy = (Map_position[0] * self.rect_size, Map_position[1] * self.rect_size)
        self.Draw_Cell(pos_xy, self.rect_size, color, 1)
        if text:
            text_surface = font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(pos_xy[0] + self.rect_size / 2, pos_xy[1] + self.rect_size / 2))
            self.screen.blit(text_surface, text_rect)

    def Show_Opened_Cells(self):
        for i in self.opened_cells:
            self.Process_Reveal(i)

    def Draw_Cell(self, Position, Size, Color, width):
        pygame.draw.rect(self.screen, Color, (Position[0], Position[1], Size, Size))

    def Draw_Outline(self, Position, Size, Color, width):
        pygame.draw.rect(self.screen, Color, (Position[0], Position[1], Size, Size), width)

    def Draw_Mouse_Outline(self):
        mouse_xy = (self.mouse_fixed_position()[0] * self.rect_size, self.mouse_fixed_position()[1] * self.rect_size)
        self.Draw_Outline(mouse_xy, self.rect_size, (0, 0, 0), 3)

    def Input_Handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.Changes_in_Game = True
                if event.button == pygame.BUTTON_LEFT:
                    self.Process_Click()
                elif event.button == pygame.BUTTON_RIGHT:
                    self.Place_Flag()

    def Place_Flag(self):
        mouse_xy = self.mouse_fixed_position()

        if mouse_xy  in self.flags:
            self.flags.remove(mouse_xy)
            return
        
        if mouse_xy in self.opened_cells or len(self.flags) >= self.bomb:
            return
        
        if mouse_xy in self.flags:
            self.flags.remove(mouse_xy)
        else:
            self.flags.add(mouse_xy)

    def Process_Click(self):
        mouse_xy = self.mouse_fixed_position()
        map_Value = self.game_map[mouse_xy[0]][mouse_xy[1]]

        if mouse_xy in self.flags:
            return

        if mouse_xy in self.opened_cells and 0 < map_Value < 9 and mouse_xy not in self.flags:
            self.Open_Safe_Cells(mouse_xy)
            return

        if map_Value == self.bomb_index:
            self.Start_Game()
            return

        if 0 < map_Value < 9:
            self.opened_cells.add((mouse_xy[0], mouse_xy[1]))

        if map_Value == 0:
            self.flood_fill((mouse_xy[0], mouse_xy[1]))


    def flood_fill(self, position):
        grid_constant_x = len(self.game_map)
        grid_constant_y = len(self.game_map[0])
        
        already_opened = set()
        position_to_check = set([position])

        while position_to_check:
            x, y = position_to_check.pop()

            if (x, y) in already_opened or x < 0 or x >= grid_constant_x or y < 0 or y >= grid_constant_y or (x, y) in self.flags:
                continue

            if self.game_map[x][y] > 0:
                self.opened_cells.add((x, y))
                already_opened.add((x, y))
                continue

            self.opened_cells.add((x, y))
            already_opened.add((x, y))

            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)]
            position_to_check.update(neighbors)

    def Open_Safe_Cells(self, position):
        x, y = position
        is_in_bound = lambda x, y: 0 <= x < self.rows and 0 <= y < self.cols

        surrounding_cells = {(x + i, y + j) for i in range(-1, 2) for j in range(-1, 2) if is_in_bound(x + i, y + j)}

        flag_count = sum(1 for cell in surrounding_cells if cell in self.flags)

        if flag_count != self.game_map[x][y]:
            return

        for cell in surrounding_cells:
            if cell in self.flags or cell in self.opened_cells:
                continue

            map_value = self.game_map[cell[0]][cell[1]]

            if map_value == 0:
                self.flood_fill(cell)
            elif map_value == self.bomb_index:
                self.Start_Game()
                return
            else:
                self.opened_cells.add(cell)
        


            


if __name__ == "__main__":
    game = MineSweeper(2)
    game.run()


