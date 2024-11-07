import pygame
from GUI.Grid import Grid
from GUI.general_graphic import (
    wall,
    freeSpace,
    stone,
    Ares,
    switchPlace,
    stonePlacedOnSwitch,
    other,
    componentSize,
)

roboto = "GUI/Roboto-Medium.ttf"


class Maze:
    def __init__(self, input: list[str], output: list[str]):
        self.grid = Grid(input)
        self.output = output
        self.width = 0
        self.height = 0

    def set_output(self, output: list[str]):
        self.output = output
        self.setAlgorithm(self.algorithm)

    def setAlgorithm(self, algorithm: str):
        self.restart()
        if algorithm == "BFS":
            self.algorithm = "BFS"
            self.grid.setAlgorithm(self.output[2])
            statitics = self.output[1]
        elif algorithm == "DFS":
            self.algorithm = "DFS"
            self.grid.setAlgorithm(self.output[5])
            statitics = self.output[4]
        elif algorithm == "UCS":
            self.algorithm = "UCS"
            self.grid.setAlgorithm(self.output[8])
            statitics = self.output[7]
        elif algorithm == "A*":
            self.algorithm = "A*"
            self.grid.setAlgorithm(self.output[11])
            statitics = self.output[10]
        parts = statitics.split(",")
        self.node = parts[2]
        self.time = parts[3]
        self.memory = parts[4]

    def restart(self):
        self.grid.restart()

    def get_size(self, screenWidth: int, screenHeight: int):
        self.componentSize = min(
            int(screenHeight / self.grid.n),
            int(screenWidth / self.grid.m),
        )
        if self.componentSize / 24 >= 1:
            self.componentSize = int(self.componentSize / 24) * 24
        elif self.componentSize / 12 >= 1:
            self.componentSize = 12
        elif self.componentSize / 8 >= 1:
            self.componentSize = 8
        elif self.componentSize / 6 >= 1:
            self.componentSize = 6
        elif self.componentSize / 4 >= 1:
            self.componentSize = 4
        elif self.componentSize / 3 >= 1:
            self.componentSize = 3
        elif self.componentSize / 2 >= 1:
            self.componentSize = 2
        elif self.componentSize >= 1:
            self.componentSize = 1
        else:
            print(self.componentSize)
            exit()
        return [
            self.componentSize * self.grid.m,
            self.componentSize * self.grid.n,
        ]

    def set_screen(self, screen: pygame.Surface):
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.scaledWall = pygame.transform.scale(
            wall, (self.componentSize, self.componentSize)
        )
        self.scaledFreeSpace = pygame.transform.scale(
            freeSpace, (self.componentSize, self.componentSize)
        )
        self.scaledStone = pygame.transform.scale(
            stone, (self.componentSize, self.componentSize)
        )
        self.scaledAres = [
            [
                pygame.transform.scale(ares, (self.componentSize, self.componentSize))
                for ares in direction
            ]
            for direction in Ares
        ]
        self.scaledSwitchPlace = pygame.transform.scale(
            switchPlace, (self.componentSize, self.componentSize)
        )
        self.scaledStonePlacedOnSwitch = pygame.transform.scale(
            stonePlacedOnSwitch, (self.componentSize, self.componentSize)
        )
        self.scaledOther = pygame.transform.scale(
            other, (self.componentSize, self.componentSize)
        )

    def preview(self):
        surface = pygame.Surface(
            (self.grid.m * componentSize, self.grid.n * componentSize),
            flags=pygame.SRCALPHA,
        )
        font = pygame.font.Font(roboto, componentSize // 4)
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if self.grid[i][j] == "#":
                    surface.blit(
                        wall,
                        (
                            j * componentSize,
                            i * componentSize,
                        ),
                    )
                elif self.grid[i][j] == " ":
                    surface.blit(
                        freeSpace,
                        (
                            j * componentSize,
                            i * componentSize,
                        ),
                    )
                elif self.grid[i][j][0] == "$":
                    surface.blit(
                        stone,
                        (
                            j * componentSize,
                            i * componentSize,
                        ),
                    )
                    pygame.draw.circle(
                        surface,
                        (255, 255, 255),
                        (
                            j * componentSize + componentSize // 2,
                            i * componentSize + componentSize // 2,
                        ),
                        componentSize // 4,
                    )
                    pygame.draw.circle(
                        surface,
                        (0, 0, 0),
                        (
                            j * componentSize + componentSize // 2,
                            i * componentSize + componentSize // 2,
                        ),
                        componentSize // 4,
                        2,
                    )
                    weight = font.render(self.grid[i][j][1:], True, (0, 0, 0))
                    surface.blit(
                        weight,
                        weight.get_rect(
                            center=(
                                j * componentSize + componentSize // 2,
                                i * componentSize + componentSize // 2,
                            )
                        ),
                    )
                elif self.grid[i][j] == "@":
                    surface.blit(
                        freeSpace,
                        (
                            j * componentSize,
                            i * componentSize,
                        ),
                    )
                    surface.blit(
                        Ares[self.grid.state][0],
                        (
                            j * componentSize,
                            i * componentSize,
                        ),
                    )
                elif self.grid[i][j] == ".":
                    surface.blit(
                        switchPlace,
                        (
                            j * componentSize,
                            i * componentSize,
                        ),
                    )
                elif self.grid[i][j][0] == "*":
                    surface.blit(
                        stonePlacedOnSwitch,
                        (
                            j * componentSize,
                            i * componentSize,
                        ),
                    )
                    pygame.draw.circle(
                        surface,
                        (255, 255, 255),
                        (
                            j * componentSize + componentSize // 2,
                            i * componentSize + componentSize // 2,
                        ),
                        componentSize // 4,
                    )
                    pygame.draw.circle(
                        surface,
                        (0, 0, 0),
                        (
                            j * componentSize + componentSize // 2,
                            i * componentSize + componentSize // 2,
                        ),
                        componentSize // 4,
                        2,
                    )
                    weight = font.render(self.grid[i][j][1:], True, (0, 0, 0))
                    surface.blit(
                        weight,
                        weight.get_rect(
                            center=(
                                j * componentSize + componentSize // 2,
                                i * componentSize + componentSize // 2,
                            )
                        ),
                    )
                elif self.grid[i][j] == "+":
                    surface.blit(
                        switchPlace,
                        (
                            j * componentSize,
                            i * componentSize,
                        ),
                    )
                    surface.blit(
                        self.scaledAres[self.grid.state][0],
                        (
                            j * componentSize,
                            i * componentSize,
                        ),
                    )
                elif self.grid[i][j] == "o":
                    pass
                    # surface.blit(
                    #     other,
                    #     (
                    #         j * componentSize,
                    #         i * componentSize,
                    #     ),
                    # )
        return surface

    def draw(self):
        self.font = pygame.font.Font(roboto, self.componentSize // 4)
        mazeWidth = self.grid.m * self.componentSize
        mazeHeight = self.grid.n * self.componentSize
        mazeLeft = (self.width - mazeWidth) / 2
        mazeTop = (self.height - mazeHeight) / 2
        action = self.grid.action
        if action == "u":
            scaledAres = self.scaledAres[0]
        elif action == "l":
            scaledAres = self.scaledAres[1]
        elif action == "d":
            scaledAres = self.scaledAres[2]
        elif action == "r":
            scaledAres = self.scaledAres[3]
        elif action == "U":
            scaledAres = self.scaledAres[4]
        elif action == "L":
            scaledAres = self.scaledAres[5]
        elif action == "D":
            scaledAres = self.scaledAres[6]
        elif action == "R":
            scaledAres = self.scaledAres[7]
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if self.grid[i][j] == "#":
                    self.screen.blit(
                        self.scaledWall,
                        (
                            mazeLeft + j * self.componentSize,
                            mazeTop + i * self.componentSize,
                        ),
                    )
                elif self.grid[i][j] == " ":
                    self.screen.blit(
                        self.scaledFreeSpace,
                        (
                            mazeLeft + j * self.componentSize,
                            mazeTop + i * self.componentSize,
                        ),
                    )
                elif self.grid[i][j][0] == "$":
                    self.screen.blit(
                        self.scaledStone,
                        (
                            mazeLeft + j * self.componentSize,
                            mazeTop + i * self.componentSize,
                        ),
                    )
                    pygame.draw.circle(
                        self.screen,
                        (255, 255, 255),
                        (
                            mazeLeft + j * self.componentSize + self.componentSize // 2,
                            mazeTop + i * self.componentSize + self.componentSize // 2,
                        ),
                        self.componentSize // 4,
                    )
                    pygame.draw.circle(
                        self.screen,
                        (0, 0, 0),
                        (
                            mazeLeft + j * self.componentSize + self.componentSize // 2,
                            mazeTop + i * self.componentSize + self.componentSize // 2,
                        ),
                        self.componentSize // 4,
                        2,
                    )
                    weight = self.font.render(self.grid[i][j][1:], True, (0, 0, 0))
                    self.screen.blit(
                        weight,
                        weight.get_rect(
                            center=(
                                mazeLeft
                                + j * self.componentSize
                                + self.componentSize // 2,
                                mazeTop
                                + i * self.componentSize
                                + self.componentSize // 2,
                            )
                        ),
                    )
                elif self.grid[i][j] == "@":
                    self.screen.blit(
                        self.scaledFreeSpace,
                        (
                            mazeLeft + j * self.componentSize,
                            mazeTop + i * self.componentSize,
                        ),
                    )
                    self.screen.blit(
                        scaledAres[self.grid.state],
                        (
                            mazeLeft + j * self.componentSize,
                            mazeTop + i * self.componentSize,
                        ),
                    )
                elif self.grid[i][j] == ".":
                    self.screen.blit(
                        self.scaledSwitchPlace,
                        (
                            mazeLeft + j * self.componentSize,
                            mazeTop + i * self.componentSize,
                        ),
                    )
                elif self.grid[i][j][0] == "*":
                    self.screen.blit(
                        self.scaledStonePlacedOnSwitch,
                        (
                            mazeLeft + j * self.componentSize,
                            mazeTop + i * self.componentSize,
                        ),
                    )
                    pygame.draw.circle(
                        self.screen,
                        (255, 255, 255),
                        (
                            mazeLeft + j * self.componentSize + self.componentSize // 2,
                            mazeTop + i * self.componentSize + self.componentSize // 2,
                        ),
                        self.componentSize // 4,
                    )
                    pygame.draw.circle(
                        self.screen,
                        (0, 0, 0),
                        (
                            mazeLeft + j * self.componentSize + self.componentSize // 2,
                            mazeTop + i * self.componentSize + self.componentSize // 2,
                        ),
                        self.componentSize // 4,
                        2,
                    )
                    weight = self.font.render(self.grid[i][j][1:], True, (0, 0, 0))
                    self.screen.blit(
                        weight,
                        weight.get_rect(
                            center=(
                                mazeLeft
                                + j * self.componentSize
                                + self.componentSize // 2,
                                mazeTop
                                + i * self.componentSize
                                + self.componentSize // 2,
                            )
                        ),
                    )
                elif self.grid[i][j] == "+":
                    self.screen.blit(
                        self.scaledSwitchPlace,
                        (
                            mazeLeft + j * self.componentSize,
                            mazeTop + i * self.componentSize,
                        ),
                    )
                    self.screen.blit(
                        scaledAres[self.grid.state],
                        (
                            mazeLeft + j * self.componentSize,
                            mazeTop + i * self.componentSize,
                        ),
                    )
                elif self.grid[i][j] == "o":
                    pass
                    # self.screen.blit(
                    #     self.scaledOther,
                    #     (
                    #         mazeLeft + j * self.componentSize,
                    #         mazeTop + i * self.componentSize,
                    #     ),
                    # )

    def next(self):
        self.grid.next()

    def back(self):
        self.grid.back()
