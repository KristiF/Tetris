import pygame
from constants import COLORS, DEFAULT_COLOR

class Grid:
    def __init__(self, rows, cols, screen):
        self.rows = rows
        self.cols = cols
        self.grid = [[0] * self.rows for col in range(self.cols)][::-1]
        self.screen = screen

    def draw(self):
        for row in range(self.rows):
            for col in range(self.cols):
                value = abs(self.grid[col][row])
                color = COLORS.get(value, DEFAULT_COLOR)
                pygame.draw.rect(self.screen, color, [20 * col + 3, 20 * row + 3, 19, 19])

    def addTetromino(self, Tet, Offsets):
        try:
            for row in range(len(Tet)):
                for col in range(len(Tet[row])):
                    if Tet[row][col] > 0:
                        self.grid[col + Offsets[0]][row + Offsets[1]] = Tet[row][col]
        except:
            pass

    def changeGrid(self, coords, newVar):
        for pos in coords:
            self.grid[pos[0]][pos[1]] = newVar


    def clearGrid(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] > 0:
                    self.grid[row][col] = 0

    def checkCollision(self, coords, value):
        for pos in coords:
            x = pos[0]
            y = pos[1]
            if y == self.rows-1 or self.grid[x][y+1] not in (0, value): return True

    def checkEdge(self, coords, direction, value):
        for pos in coords:
            x = pos[0] + direction
            y = pos[1]
            if x < 0 or x >= self.cols or self.grid[x][y] not in  (0, value):
                return True
        return False

    def clearRows(self, rows):
        for row in rows:
            for col in range(self.cols):
                self.grid[col][row] = 0
            for x in range(self.cols):
                self.grid[x][self.rows-1] = self.grid[x][self.rows-2]
            for y in range(self.rows-2, 0, -1):
                for x in range(self.cols):
                    self.grid[x][y] = self.grid[x][y-1]

    def checkRows(self):
        clearedRows = []
        for y in range(20):
            filledRows = 0
            for x in range(10):
                if self.grid[x][y] < 0:
                    filledRows += 1
                if filledRows == 10:
                    clearedRows.append(y)
        if clearedRows != []:
            clearedRows.sort()
            self.clearRows(clearedRows)
            return(len(clearedRows))
        return 0

    def hasLost(self):
        for x in range(self.cols):
            if self.grid[x][0] < 0:
                return True
        return False