import pygame
import time
import numpy
import random

LIGHT_BLUE = (0, 191, 255)
YELLOW = (255, 246, 0)
PURPLE = (241, 25, 252)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 114, 0)



class grid(object):
    def __init__(self, rows, cols, screen):
        self.rows = rows
        self.cols = cols
        self.grid = [[0] * self.rows for col in range(self.cols)][::-1]
        self.screen = screen

    def draw(self):
        for row in range(self.rows):
            for col in range(self.cols):
                color = (255, 255, 255)
                if abs(self.grid[col][row]) == 1:
                    color = LIGHT_BLUE
                if abs(self.grid[col][row]) == 2:
                    color = PURPLE
                if abs(self.grid[col][row]) == 3:
                    color = YELLOW
                if abs(self.grid[col][row]) == 4:
                    color = GREEN
                if abs(self.grid[col][row]) == 5:
                    color = RED
                if abs(self.grid[col][row]) == 6:
                    color = BLUE
                if abs(self.grid[col][row]) == 7:
                    color = ORANGE
                pygame.draw.rect(self.screen, color, [20 * col + 3, 20 * row + 3, 19, 19])

    def addTetromino(self, Tet, Offsets):
        try:
            for row in range(len(Tet)):
                for col in range(len(Tet[row])):
                    if Tet[row][col] > 0:
                        self.grid[col + Offsets[0]][row + Offsets[1]] = Tet[row][col]
        except:
            pass
            #print(Offsets)

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

class tetromino(object):
    def __init__(self, grid, shape):
        self.grid = grid
        self.offsets = [3, 0]
        self.shape = shape
        self.locked = False
        self.getValue()

    def getValue(self):
        for x in range(len(self.shape)):
            for y in range(len(self.shape)):
                if self.shape[x][y] != 0:
                    self.value = self.shape[x][y]

    def getCoords(self):
        self.coords = []
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x] > 0:
                    self.coords.append([x+self.offsets[0], y+self.offsets[1]])
        return self.coords

    def lock(self):
        self.getCoords()
        self.grid.changeGrid(self.coords, -self.value)

    def loseHeight(self):
        self.getCoords()
        if self.grid.checkCollision(self.coords, self.value):
            self.locked = True
            self.lock()
            return True
        self.offsets[1] += 1
        return False

    def draw(self):
        self.grid.clearGrid()
        self.grid.addTetromino(self.shape, self.offsets)

    def wallKick(self):
        self.getCoords()
        newCoords =[]
        for pos in self.coords:
            x = pos[0]
            y = pos[1]
            if x < 0:
                x += abs(-pos[0])+1
                self.offsets[0] += abs(-pos[0])+1
            if x >= self.grid.cols:
                x -= abs(pos[0]-self.grid.cols)+1
                self.offsets[0] -= abs(pos[0]-self.grid.cols)+1
            if y >= self.grid.rows:
                y -= abs(pos[1] - self.grid.rows) - 1
                self.offsets[1] -= abs(pos[1] - self.grid.rows) - 1
            newCoords.append([x, y])
        self.coords = newCoords[:]

    def shift(self, direction):
        if self.locked: return
        self.direction = direction

        if direction in (-1, 1):
            if not self.grid.checkEdge(self.getCoords(), direction, self.value):
                self.offsets[0] += direction
                return True
        if direction == 90:
            self.shape = numpy.rot90(self.shape, axes=(0, -1))
        if direction == -90:
            self.shape = numpy.rot90(self.shape, k=-1)

        self.wallKick()

    def shift_new(self):
        pass

class game(object):
    def __init__(self):
        pygame.init()
        self.loadTetrominoes()
        self.screen = pygame.display.set_mode((380, 500))
        self.grid = grid(20, 10, self.screen)
        self.starttime = time.time()
        self.timeChange = 1
        self.clock = pygame.time.Clock()
        self.softDrop = False
        self.randTetromino()
        self.font = pygame.font.SysFont('arial', 16)
        self.pause = False
        self.pos = []
        self.holding = False
        self.score = 0


    def randTetromino(self):
        shape = 'J'
        #shape = random.choice(('I', 'J', 'L', 'O', 'Z', 'S', 'T'))
        self.tetromino = tetromino(self.grid, self.tetrominoes[shape])

    def checkForEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return (True)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.pos = pygame.mouse.get_pos()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.softDrop = True

                if event.key == pygame.K_UP:
                    self.tetromino.shift(-90)
                if event.key == pygame.K_z:
                    self.tetromino.shift(90)
                if event.key == pygame.K_LEFT:
                    self.tetromino.shift(-1)
                if event.key == pygame.K_RIGHT:
                    self.tetromino.shift(1)
                if event.key == pygame.K_SPACE:
                    if not self.pause:
                        self.pause = True
                    else:
                        self.pause = False
                if event.key == pygame.K_LSHIFT:
                    if not self.holding:
                        self.holding = True
                        self.holdedTetromino = self.tetromino
                        self.randTetromino()
                    if self.holding:
                        temp_tet = self.tetromino
                        self.tetromino = self.holdedTetromino
                        self.holdedTetromino = temp_tet
                    self.holdedTetromino.offsets = [3, 0]

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.softDrop = False


    def drawScore(self):
        score = self.font.render('Score: {0}'.format(self.score), 100, (255, 255, 255))
        self.screen.blit(score, (10, 410))


    def checkTimer(self):
        if time.time() - self.starttime > self.timeChange:
            self.starttime = time.time()
            return True
        return

    def loadTetrominoes(self):
        self.tetrominoes = {}
        with open('Tetrominoes.txt') as file:
            for line in file:
                Tetromino = line[0]
                Shape = tuple(map(tuple, [[int(col) for col in row]
                                          for row in [row.split(',')
                                                      for row in line[-1:0:-1][::-1].strip(' ').split('|')]]))
                self.tetrominoes[Tetromino] = Shape

    def main(self):
        while True:
            if self.checkForEvents():
                break
            self.clock.tick(60)
            if self.softDrop:
                self.timeChange = 0.05
            else:
                self.timeChange = 1


            self.screen.fill((0, 0, 0))

            self.tetromino.draw()
            self.grid.draw()
            self.drawScore()
            self.score += self.grid.checkRows()
            if not self.pause and not self.grid.hasLost():
                if self.checkTimer():
                    if self.tetromino.loseHeight():
                        self.randTetromino()
            pygame.display.flip()
        pygame.quit()

test = game()
test.main()