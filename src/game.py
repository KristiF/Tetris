import pygame
import time
from tetromino import Tetromino
from grid import Grid
import random

class Game():
    def __init__(self):
        pygame.init()
        self.loadTetrominoes()
        self.screen = pygame.display.set_mode((380, 500))
        self.grid = Grid(20, 10, self.screen)
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
        shape = random.choice(('I', 'J', 'L', 'O', 'Z', 'S', 'T'))
        self.tetromino = Tetromino(self.grid, self.tetrominoes[shape])

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
        with open('assets/shapes.txt', encoding="utf-8") as file:
            for line in file:
                Tetromino = line[0]
                Shape = tuple(map(tuple, [[int(col) for col in row]
                                          for row in [row.split(',')
                                                      for row in line[-1:0:-1][::-1].strip(' ').split('|')]]))
                self.tetrominoes[Tetromino] = Shape

    def run(self):
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