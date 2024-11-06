import pygame

from .general_graphic import font


class MenuScreen:
    def __init__(self, screen: pygame.Surface, mazeScreens: list[pygame.Surface]):
        self.screen = screen
        self.mazeScreens = mazeScreens
        self.width = 0
        self.height = 0
        self.scaledMazeScreens: list[pygame.Surface] = [None] * 10
        self.scaledMazeScreenRects: list[pygame.Rect] = [None] * 10
        self.font = font
        self.selectedInput = 0
        self.selectedAlgorithm = "BFS"

    def resize(self):
        if (self.width, self.height) == self.screen.get_size():
            return
        self.width, self.height = self.screen.get_size()
        self.headerHeight = self.height // 8 // 24 * 24
        self.mazeHeight = min(
            (self.height - self.headerHeight) // 4 // 24 * 24,
            self.width // 5 // 2 // 24 * 24,
        )
        self.mazeWidth = self.mazeHeight * 2
        self.gapWidth = (self.width - self.mazeWidth * 4) // 5
        self.gapHeight = (self.height - self.headerHeight - self.mazeHeight * 3) // 3
        for i in range(10):
            scale = min(
                self.mazeWidth / self.mazeScreens[i].get_width(),
                self.mazeHeight / self.mazeScreens[i].get_height(),
            )
            self.scaledMazeScreens[i] = pygame.transform.scale_by(
                self.mazeScreens[i], scale
            )
            self.scaledMazeScreenRects[i] = self.scaledMazeScreens[i].get_rect(
                center=(
                    self.gapWidth
                    + (self.mazeWidth + self.gapWidth) * (i % 4)
                    + self.mazeWidth // 2,
                    self.headerHeight
                    + (self.mazeHeight + self.gapHeight) * (i // 4)
                    + self.mazeHeight // 2,
                )
            )
        font = pygame.font.Font(self.font, self.headerHeight // 2)
        self.BFS = font.render("BFS", True, (255, 255, 255))
        self.BFSRect = self.BFS.get_rect(
            center=(
                self.gapWidth
                + (self.mazeWidth + self.gapWidth) * 2
                + (self.mazeWidth * 2 + self.gapWidth) // 8,
                self.headerHeight
                + (self.mazeHeight + self.gapHeight) * 2
                + self.gapHeight // 4,
            )
        )
        self.DFS = font.render("DFS", True, (255, 255, 255))
        self.DFSRect = self.DFS.get_rect(
            center=(
                self.gapWidth
                + (self.mazeWidth + self.gapWidth) * 2
                + (self.mazeWidth * 2 + self.gapWidth) // 8 * 3,
                self.headerHeight
                + (self.mazeHeight + self.gapHeight) * 2
                + self.gapHeight // 4,
            )
        )
        self.UCS = font.render("UCS", True, (255, 255, 255))
        self.UCSRect = self.UCS.get_rect(
            center=(
                self.gapWidth
                + (self.mazeWidth + self.gapWidth) * 2
                + (self.mazeWidth * 2 + self.gapWidth) // 8 * 5,
                self.headerHeight
                + (self.mazeHeight + self.gapHeight) * 2
                + self.gapHeight // 4,
            )
        )
        self.A = font.render("A*", True, (255, 255, 255))
        self.ARect = self.A.get_rect(
            center=(
                self.gapWidth
                + (self.mazeWidth + self.gapWidth) * 2
                + (self.mazeWidth * 2 + self.gapWidth) // 8 * 7,
                self.headerHeight
                + (self.mazeHeight + self.gapHeight) * 2
                + self.gapHeight // 4,
            )
        )
        self.start = pygame.font.Font(self.font, self.headerHeight // 3 * 2).render(
            "Start", True, (50, 205, 50)
        )
        self.startRect = self.start.get_rect(
            center=(
                self.gapWidth
                + (self.mazeWidth + self.gapWidth) * 2
                + (self.mazeWidth * 2 + self.gapWidth) // 2,
                self.headerHeight
                + (self.mazeHeight + self.gapHeight) * 2
                + self.gapHeight * 1.25,
            )
        )

    def draw(self):
        title = pygame.font.Font(self.font, self.headerHeight // 2).render(
            "Ares's adventure", True, (255, 69, 0)
        )
        self.screen.blit(
            title, title.get_rect(center=(self.width // 2, self.headerHeight // 2))
        )
        font = pygame.font.Font(self.font, self.headerHeight // 4)
        for i in range(10):
            self.screen.blit(
                self.scaledMazeScreens[i],
                self.scaledMazeScreenRects[i],
            )
            if i == self.selectedInput or self.scaledMazeScreenRects[i].collidepoint(
                pygame.mouse.get_pos()
            ):
                pygame.draw.rect(
                    self.screen,
                    (255, 215, 0),
                    self.scaledMazeScreenRects[i],
                    1,
                )
            text = font.render(f"input-{i+1:02d}.txt", True, (255, 255, 255))
            self.screen.blit(
                text,
                text.get_rect(
                    center=(
                        self.gapWidth
                        + (i % 4) * (self.mazeWidth + self.gapWidth)
                        + self.mazeWidth // 2,
                        self.headerHeight
                        + (i // 4) * (self.mazeHeight + self.gapHeight)
                        + self.mazeHeight
                        + self.gapHeight // 4,
                    )
                ),
            )
        algorithmFont = pygame.font.Font(self.font, self.headerHeight // 2)
        if self.selectedAlgorithm == "BFS" or self.BFSRect.collidepoint(
            pygame.mouse.get_pos()
        ):
            BFS = algorithmFont.render("BFS", True, (255, 215, 0))
            self.screen.blit(BFS, self.BFSRect)
        else:
            self.screen.blit(self.BFS, self.BFSRect)
        if self.selectedAlgorithm == "DFS" or self.DFSRect.collidepoint(
            pygame.mouse.get_pos()
        ):
            DFS = algorithmFont.render("DFS", True, (255, 215, 0))
            self.screen.blit(DFS, self.DFSRect)
        else:
            self.screen.blit(self.DFS, self.DFSRect)
        if self.selectedAlgorithm == "UCS" or self.UCSRect.collidepoint(
            pygame.mouse.get_pos()
        ):
            UCS = algorithmFont.render("UCS", True, (255, 215, 0))
            self.screen.blit(UCS, self.UCSRect)
        else:
            self.screen.blit(self.UCS, self.UCSRect)
        if self.selectedAlgorithm == "A*" or self.ARect.collidepoint(
            pygame.mouse.get_pos()
        ):
            A = algorithmFont.render("A*", True, (255, 215, 0))
            self.screen.blit(A, self.ARect)
        else:
            self.screen.blit(self.A, self.ARect)
        if self.startRect.collidepoint(pygame.mouse.get_pos()):
            start = pygame.font.Font(self.font, self.headerHeight // 3 * 2).render(
                "Start", True, (0, 255, 255)
            )
            self.screen.blit(start, self.startRect)
        else:
            self.screen.blit(self.start, self.startRect)
        isCursor = False
        for i in range(10):
            if self.scaledMazeScreenRects[i].collidepoint(pygame.mouse.get_pos()):
                isCursor = True
        if self.BFSRect.collidepoint(pygame.mouse.get_pos()):
            isCursor = True
        if self.DFSRect.collidepoint(pygame.mouse.get_pos()):
            isCursor = True
        if self.UCSRect.collidepoint(pygame.mouse.get_pos()):
            isCursor = True
        if self.ARect.collidepoint(pygame.mouse.get_pos()):
            isCursor = True
        if self.startRect.collidepoint(pygame.mouse.get_pos()):
            isCursor = True
        if isCursor:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handleEvent(self, event: pygame.event.Event):
        # sự kiện chuột
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # nhấn chuột trái
                # print(event.pos)  # in tọa độ chuột
                for i in range(10):
                    if self.scaledMazeScreenRects[i].collidepoint(event.pos):
                        self.selectedInput = i
                if self.BFSRect.collidepoint(event.pos):
                    self.selectedAlgorithm = "BFS"
                if self.DFSRect.collidepoint(event.pos):
                    self.selectedAlgorithm = "DFS"
                if self.UCSRect.collidepoint(event.pos):
                    self.selectedAlgorithm = "UCS"
                if self.ARect.collidepoint(event.pos):
                    self.selectedAlgorithm = "A*"
                if self.startRect.collidepoint(event.pos):
                    if self.selectedInput is not None and self.selectedAlgorithm != "":
                        pygame.event.post(
                            pygame.event.Event(
                                pygame.USEREVENT + self.selectedInput + 1
                            )
                        )
                        if self.selectedAlgorithm == "BFS":
                            pygame.event.post(pygame.event.Event(pygame.USEREVENT + 11))
                        elif self.selectedAlgorithm == "DFS":
                            pygame.event.post(pygame.event.Event(pygame.USEREVENT + 12))
                        elif self.selectedAlgorithm == "UCS":
                            pygame.event.post(pygame.event.Event(pygame.USEREVENT + 13))
                        elif self.selectedAlgorithm == "A*":
                            pygame.event.post(pygame.event.Event(pygame.USEREVENT + 14))
        if event.type == pygame.WINDOWRESIZED or event.type == pygame.VIDEORESIZE:
            self.resize()
