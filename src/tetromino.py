import numpy

class Tetromino(object):
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

