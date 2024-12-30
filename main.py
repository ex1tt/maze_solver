import pygame
from pygame.locals import *
from collections import deque

# example matrix...
mazeSmall = [
        [0,1,0,1,1],
        [0,0,0,0,1],
        [0,1,1,0,0],
        [0,1,0,1,0],
        [0,0,0,1,2]
        ]

mazeMedium = [
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 2]
    ]

mazeLarge = [
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]
    ]

class Maze:

    def __init__(self, matrix, screenWidth):

        self.matrix = matrix
        self.tile_size = int(screenWidth / len(matrix))
        self.totalPath = []

        # count of how many nodes visited during search...
        self.count = 0

    # draw the maze without path
    def draw(self, screen):

        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[0])):

                tile = pygame.Rect(col*self.tile_size, row*self.tile_size, self.tile_size, self.tile_size)
                
                # path white
                if(self.matrix[row][col] == PATH): 
                    pygame.draw.rect(screen, (255, 255, 255), tile)
                # wall black
                elif(self.matrix[row][col] == WALL):
                    pygame.draw.rect(screen, (0, 0, 0), tile)
                # end green
                elif(self.matrix[row][col] == END):
                    pygame.draw.rect(screen, (0,255,0), tile)

    # preform a search on maze and return the path, (also keeps track of total paths)
    def search(self, sX,sY, typeOfSearch) -> list:

        typeOfSearch = typeOfSearch.lower()

        if(typeOfSearch not in {"bfs", "dfs"}):
            return []
        
        container = deque([(sX, sY, [(sY,sX)])])
        visited = set((sX,sY))
        self.totalPath, self.count = [], 0

        # loop while container is non empty
        while(container):
            
            self.count +=1
            # pop x, y and the current path variables from container...
            currentX, currentY, currentPath = container.pop() if typeOfSearch == "dfs" else container.popleft()

            # append the current path onto the total
            self.totalPath.append(currentPath)

            # if current node == end square (2), return the path
            if(self.matrix[currentX][currentY] == 2):
                return currentPath

            # check all vertical and horizontal adjacent neighbour nodes...
            for dx, dy in [(1,0), (0,1), (-1,0), (0,-1)]:

                nx = currentX + dx
                ny = currentY + dy

                # if neighbour is inside maze, unvisited and not a wall tile -> append to container and visited array
                if(nx >=0 and nx < len(self.matrix) 
                and ny >=0 and ny < len(self.matrix) 
                and self.matrix[nx][ny] != 1 
                and (nx, ny) not in visited):

                    container.append((nx, ny, currentPath + [(ny, nx)]))
                    visited.add((nx, ny))

        # return empty array if no path found (stack is empty)
        return []


# initialize pygame
pygame.init()

# setting fps and pygame clock
FPS = 30
FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
PATH, WALL, END = 0, 1, 2

# define pygame screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Solver")

# create a maze instance
maze = Maze(mazeLarge, SCREEN_WIDTH)

# search maze
maze.search(0,0, "bfs")

totalPath = maze.totalPath
path = []
pathIndex = 0

# Game loop
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    # Clear the screen by filling it with black before drawing again
    DISPLAYSURF.fill((0, 0, 0))

    maze.draw(DISPLAYSURF)

    # loop through the path and draw each node within said array to display surf
    for tupl in path:
        x,y = tupl

        tile = pygame.Rect(x*maze.tile_size, y*maze.tile_size, maze.tile_size, maze.tile_size)
        pygame.draw.rect(DISPLAYSURF, (0, 255, 0), tile)

    # ensures path index does not exceed no. of path arrays inside totalPath array
    if (pathIndex < len(totalPath)):
        
        # set path to the total path at index path index (next path the algorithm took)
        path = totalPath[pathIndex]
        # increment path index by 1
        pathIndex +=1

    # Update the display
    pygame.display.update()

    # Frame rate control
    FramePerSec.tick(FPS)
