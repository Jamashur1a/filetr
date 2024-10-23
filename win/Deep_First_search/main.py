import pygame
import time

pygame.init()

screen_size = 600
rows, cols = 20, 20
cell_size = screen_size // rows

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


screen = pygame.display.set_mode((screen_size, screen_size))

maze = [
    [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1],
    [0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1],
    [0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

start = (0, 0)
end = (18, 19)

def draw_grid():
    for row in range(rows):
        for col in range(cols):
            if row >= len(maze) or col >= len(maze[0]):
                continue

            color = WHITE if maze[row][col] == 1 else BLACK
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, BLUE, (col * cell_size, row * cell_size, cell_size, cell_size), 1)


def draw_path(path):
    for cell in path:
        x, y = cell
        pygame.draw.rect(screen, GREEN, (y * cell_size, x * cell_size, cell_size, cell_size))
        pygame.display.update()
        time.sleep(0.01)

def dfs(maze, start, end):
    stack = [start]
    visited = set()
    path = []
    
    while stack:
        current = stack.pop()

        if current in visited:
            continue

        path.append(current)
        visited.add(current)

        x,y = current
        neighbors = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]

        draw_path([current])

        if current == end:
            return path

        for nx, ny in neighbors:
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1 and (nx, ny) not in visited:
                stack.append((nx, ny))
    
    return None

def main():
    running = True
    path = []
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(WHITE)
        draw_grid()
        
        if not path:
            path = dfs(maze, start, end)

        pygame.display.update()
    

    pygame.quit()

if __name__ == "__main__":
    main()
