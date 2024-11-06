import pygame

from GUI.Maze import Maze
from GUI.general_graphic import font
from controller import Controller
import threading


class MazeScreen:
    def __init__(self, screen: pygame.Surface, inputFileName: str, outputFileName: str):
        self.screen = screen
        input = open(inputFileName, "r").read().split("\n")
        output = open(outputFileName, "r").read().split("\n")
        self.maze = Maze(input, output)
        self.running = False
        self.inputFileName = inputFileName
        self.outputFileName = outputFileName
        self.number = int(inputFileName.split(".")[0].split("input-")[1])
        self.width = 0
        self.height = 0
        self.isPause = False
        self.speed = 1
        self.time = 0
        self.font = font
        self.loadingImage = pygame.image.load("GUI/loading.png")
        self.angle = 0
        self.loading = False

    def preview(self):
        return self.maze.preview()

    def resize(self):
        if (self.width, self.height) == self.screen.get_size():
            return
        self.width, self.height = self.screen.get_size()
        self.headerHeight = self.height // 8 // 24 * 24
        self.footerHeight = self.height // 8 // 24 * 24
        self.mazeWidth, self.mazeHeight = self.maze.get_size(
            self.width, self.height - self.headerHeight - self.footerHeight
        )
        self.header = self.screen.subsurface(
            0,
            (self.height - self.headerHeight - self.mazeHeight - self.footerHeight)
            // 2,
            self.width,
            self.headerHeight,
        )
        self.maze.set_screen(
            self.screen.subsurface(
                (self.width - self.mazeWidth) // 2,
                (self.height - self.headerHeight - self.mazeHeight - self.footerHeight)
                // 2
                + self.headerHeight,
                self.mazeWidth,
                self.mazeHeight,
            )
        )
        self.footer = self.screen.subsurface(
            0,
            (self.height - self.footerHeight),
            self.width,
            self.footerHeight,
        )
        self.statitics = self.screen.subsurface(
            self.width // 4 * 3,
            0,
            self.width // 4,
            self.height // 5,
        )
        self.algorithmDisplay = self.screen.subsurface(
            self.width // 4 * 3,
            self.height // 8,
            self.width // 4,
            self.height // 8,
        )
        fontAlgorithm = pygame.font.Font(
            self.font, self.algorithmDisplay.get_height() // 3
        )
        self.BFS = fontAlgorithm.render("BFS", True, (255, 255, 255))
        self.BFSRect = self.BFS.get_rect(
            center=(
                self.width // 4 * 3 + self.width // 4 // 8,
                self.height // 5 + self.algorithmDisplay.get_height() // 4,
            )
        )
        self.DFS = fontAlgorithm.render("DFS", True, (255, 255, 255))
        self.DFSRect = self.DFS.get_rect(
            center=(
                self.width // 4 * 3 + self.width // 4 // 8 * 3,
                self.height // 5 + self.algorithmDisplay.get_height() // 4,
            )
        )
        self.UCS = fontAlgorithm.render("UCS", True, (255, 255, 255))
        self.UCSRect = self.UCS.get_rect(
            center=(
                self.width // 4 * 3 + self.width // 4 // 8 * 5,
                self.height // 5 + self.algorithmDisplay.get_height() // 4,
            )
        )
        self.AStar = fontAlgorithm.render("A*", True, (255, 255, 255))
        self.AStarRect = self.AStar.get_rect(
            center=(
                self.width // 4 * 3 + self.width // 4 // 8 * 7,
                self.height // 5 + self.algorithmDisplay.get_height() // 4,
            )
        )
        self.regenerate = fontAlgorithm.render("Regenerate output", True, (255, 69, 0))
        self.regenerateRect = self.regenerate.get_rect(
            center=(
                self.width // 4 * 3 + self.width // 4 // 2,
                self.height // 5 + self.algorithmDisplay.get_height() // 4 * 3,
            )
        )
        self.loadingImage = pygame.image.load("GUI/loading.png")
        self.loadingImage = pygame.transform.scale(
            self.loadingImage,
            (
                self.height // 12,
                self.height // 12,
            ),
        )
        self.fade = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)

    def setAlgorithm(self, algorithm: str):
        self.running = False
        self.algorithm = algorithm
        self.maze.setAlgorithm(algorithm)

    def draw(self):
        self.maze.draw()
        headerFont = pygame.font.Font(self.font, self.headerHeight // 2)
        title = headerFont.render(self.inputFileName, True, (255, 255, 255))
        self.screen.blit(
            title,
            title.get_rect(center=(self.width // 2, self.headerHeight // 3 * 2)),
        )
        footerFont = pygame.font.Font(self.font, self.footerHeight // 3)
        footerOffset = self.footer.get_offset()
        start = footerFont.render("Start", True, (50, 205, 50))
        self.startRect = start.get_rect(
            center=(self.width // 8, self.footerHeight // 3)
        )
        if (
            self.startRect.collidepoint(
                pygame.mouse.get_pos()[0] - footerOffset[0],
                pygame.mouse.get_pos()[1] - footerOffset[1],
            )
            and not self.loading
        ):
            start = footerFont.render("Start", True, (0, 255, 255))

        if self.isPause:
            pause = footerFont.render("Resume", True, (50, 205, 50))
            self.pauseRect = pause.get_rect(
                center=(self.width // 8 * 2, self.footerHeight // 3)
            )
            if (
                self.pauseRect.collidepoint(
                    pygame.mouse.get_pos()[0] - footerOffset[0],
                    pygame.mouse.get_pos()[1] - footerOffset[1],
                )
                and not self.loading
            ):
                pause = footerFont.render("Resume", True, (0, 255, 255))
        else:
            pause = footerFont.render("Pause", True, (50, 205, 50))
            self.pauseRect = pause.get_rect(
                center=(self.width // 8 * 2, self.footerHeight // 3)
            )
            if (
                self.pauseRect.collidepoint(
                    pygame.mouse.get_pos()[0] - footerOffset[0],
                    pygame.mouse.get_pos()[1] - footerOffset[1],
                )
                and not self.loading
            ):
                pause = footerFont.render("Pause", True, (0, 255, 255))
        back = footerFont.render("Back", True, (50, 205, 50))
        self.backRect = back.get_rect(
            center=(self.width // 8 * 3, self.footerHeight // 3)
        )
        if (
            self.backRect.collidepoint(
                pygame.mouse.get_pos()[0] - footerOffset[0],
                pygame.mouse.get_pos()[1] - footerOffset[1],
            )
            and not self.loading
        ):
            back = footerFont.render("Back", True, (0, 255, 255))
        next = footerFont.render("Next", True, (50, 205, 50))
        self.nextRect = next.get_rect(
            center=(self.width // 8 * 4, self.footerHeight // 3)
        )
        if (
            self.nextRect.collidepoint(
                pygame.mouse.get_pos()[0] - footerOffset[0],
                pygame.mouse.get_pos()[1] - footerOffset[1],
            )
            and not self.loading
        ):
            next = footerFont.render("Next", True, (0, 255, 255))
        restart = footerFont.render("Restart", True, (50, 205, 50))
        self.restartRect = restart.get_rect(
            center=(self.width // 8 * 5, self.footerHeight // 3)
        )
        if (
            self.restartRect.collidepoint(
                pygame.mouse.get_pos()[0] - footerOffset[0],
                pygame.mouse.get_pos()[1] - footerOffset[1],
            )
            and not self.loading
        ):
            restart = footerFont.render("Restart", True, (0, 255, 255))
        speed = footerFont.render(str(self.speed) + "x", True, (50, 205, 50))
        self.speedRect = speed.get_rect(
            center=(self.width // 8 * 6, self.footerHeight // 3)
        )
        if (
            self.speedRect.collidepoint(
                pygame.mouse.get_pos()[0] - footerOffset[0],
                pygame.mouse.get_pos()[1] - footerOffset[1],
            )
            and not self.loading
        ):
            speed = footerFont.render(str(self.speed) + "x", True, (0, 255, 255))
        self.footer.blit(speed, self.speedRect)
        menu = footerFont.render("Menu", True, (50, 205, 50))
        self.menuRect = menu.get_rect(
            center=(self.width // 8 * 7, self.footerHeight // 3)
        )
        if (
            self.menuRect.collidepoint(
                pygame.mouse.get_pos()[0] - footerOffset[0],
                pygame.mouse.get_pos()[1] - footerOffset[1],
            )
            and not self.loading
        ):
            menu = footerFont.render("Menu", True, (0, 255, 255))
        self.footer.blit(start, self.startRect)
        self.footer.blit(pause, self.pauseRect)
        self.footer.blit(back, self.backRect)
        self.footer.blit(next, self.nextRect)
        self.footer.blit(restart, self.restartRect)
        self.footer.blit(menu, self.menuRect)
        if self.running:
            if pygame.time.get_ticks() - self.time > 500 / self.speed:
                self.maze.next()
                self.time = pygame.time.get_ticks()
        previousMap = pygame.font.Font(self.font, self.footerHeight).render(
            "<", True, (255, 255, 255)
        )
        self.previousMapRect = previousMap.get_rect(
            center=(
                100,
                self.height // 2,
            )
        )
        if (
            self.previousMapRect.collidepoint(pygame.mouse.get_pos())
            and not self.loading
        ):
            previousMap = pygame.font.Font(self.font, self.footerHeight).render(
                "<", True, (255, 215, 0)
            )
        self.screen.blit(previousMap, self.previousMapRect)
        nextMap = pygame.font.Font(self.font, self.footerHeight).render(
            ">", True, (255, 255, 255)
        )
        self.nextMapRect = nextMap.get_rect(
            center=(
                (self.width - 100),
                self.height // 2,
            )
        )
        if self.nextMapRect.collidepoint(pygame.mouse.get_pos()) and not self.loading:
            nextMap = pygame.font.Font(self.font, self.footerHeight).render(
                ">", True, (255, 215, 0)
            )
        self.screen.blit(nextMap, self.nextMapRect)
        pygame.draw.rect(
            self.statitics,
            (255, 255, 255),
            self.statitics.get_rect(),
            0,
            10,
        )
        pygame.draw.rect(
            self.statitics,
            (0, 0, 0),
            self.statitics.get_rect(),
            3,
            10,
        )
        statiticsFont = pygame.font.Font(
            "GUI/Roboto-Medium.ttf", self.statitics.get_height() // 8
        )
        fontSize = self.statitics.get_height() // 8
        gap = fontSize // 2
        step = statiticsFont.render(
            " Step: "
            + str(self.maze.grid.step)
            + " / "
            + str(len(self.maze.grid.algorithm)),
            True,
            (0, 0, 0),
        )
        self.statitics.blit(step, step.get_rect(topleft=(gap, gap)))
        pushedWeight = statiticsFont.render(
            " Pushed weight: " + str(self.maze.grid.pushedWeight),
            True,
            (0, 0, 0),
        )
        self.statitics.blit(
            pushedWeight,
            pushedWeight.get_rect(
                topleft=(gap, gap + (fontSize + gap) * 1),
            ),
        )
        node = statiticsFont.render(self.maze.node, True, (0, 0, 0))
        self.statitics.blit(
            node,
            node.get_rect(
                topleft=(gap, gap + (fontSize + gap) * 2),
            ),
        )
        time = statiticsFont.render(self.maze.time, True, (0, 0, 0))
        self.statitics.blit(
            time,
            time.get_rect(
                topleft=(gap, gap + (fontSize + gap) * 3),
            ),
        )
        memory = statiticsFont.render(self.maze.memory, True, (0, 0, 0))
        self.statitics.blit(
            memory,
            memory.get_rect(
                topleft=(gap, gap + (fontSize + gap) * 4),
            ),
        )
        if self.algorithm == "BFS" or (
            self.BFSRect.collidepoint(pygame.mouse.get_pos()) and not self.loading
        ):
            BFS = pygame.font.Font(
                self.font, self.algorithmDisplay.get_height() // 3
            ).render("BFS", True, (255, 215, 0))
            self.screen.blit(BFS, self.BFSRect)
        else:
            self.screen.blit(self.BFS, self.BFSRect)
        if self.algorithm == "DFS" or (
            self.DFSRect.collidepoint(pygame.mouse.get_pos()) and not self.loading
        ):
            DFS = pygame.font.Font(
                self.font, self.algorithmDisplay.get_height() // 3
            ).render("DFS", True, (255, 215, 0))
            self.screen.blit(DFS, self.DFSRect)
        else:
            self.screen.blit(self.DFS, self.DFSRect)
        if self.algorithm == "UCS" or (
            self.UCSRect.collidepoint(pygame.mouse.get_pos()) and not self.loading
        ):
            UCS = pygame.font.Font(
                self.font, self.algorithmDisplay.get_height() // 3
            ).render("UCS", True, (255, 215, 0))
            self.screen.blit(UCS, self.UCSRect)
        else:
            self.screen.blit(self.UCS, self.UCSRect)
        if self.regenerateRect.collidepoint(pygame.mouse.get_pos()) or self.loading:
            regenerate = pygame.font.Font(
                self.font, self.algorithmDisplay.get_height() // 3
            ).render("Regenerate output", True, (255, 40, 0))
            self.screen.blit(regenerate, self.regenerateRect)
        else:
            self.screen.blit(self.regenerate, self.regenerateRect)
        if self.algorithm == "A*" or (
            self.AStarRect.collidepoint(pygame.mouse.get_pos()) and not self.loading
        ):
            AStar = pygame.font.Font(
                self.font, self.algorithmDisplay.get_height() // 3
            ).render("A*", True, (255, 215, 0))
            self.screen.blit(AStar, self.AStarRect)
        else:
            self.screen.blit(self.AStar, self.AStarRect)
        if not self.loading:
            if self.startRect.collidepoint(
                pygame.mouse.get_pos()[0] - footerOffset[0],
                pygame.mouse.get_pos()[1] - footerOffset[1],
            ):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif self.pauseRect.collidepoint(
                pygame.mouse.get_pos()[0] - footerOffset[0],
                pygame.mouse.get_pos()[1] - footerOffset[1],
            ):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif self.nextRect.collidepoint(
                pygame.mouse.get_pos()[0] - footerOffset[0],
                pygame.mouse.get_pos()[1] - footerOffset[1],
            ):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif self.backRect.collidepoint(
                pygame.mouse.get_pos()[0] - footerOffset[0],
                pygame.mouse.get_pos()[1] - footerOffset[1],
            ):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif self.restartRect.collidepoint(
                pygame.mouse.get_pos()[0] - footerOffset[0],
                pygame.mouse.get_pos()[1] - footerOffset[1],
            ):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif self.speedRect.collidepoint(
                pygame.mouse.get_pos()[0] - footerOffset[0],
                pygame.mouse.get_pos()[1] - footerOffset[1],
            ):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif self.menuRect.collidepoint(
                pygame.mouse.get_pos()[0] - footerOffset[0],
                pygame.mouse.get_pos()[1] - footerOffset[1],
            ):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif self.previousMapRect.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif self.nextMapRect.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif self.BFSRect.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif self.DFSRect.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif self.UCSRect.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif self.AStarRect.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif self.regenerateRect.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if self.loading:
            self.loading_screen()

    def start(self):
        self.time = pygame.time.get_ticks()
        self.running = True

    def pause(self):
        self.isPause = not self.isPause
        self.running = not self.running

    def generate(self):
        controller = Controller(str(self.number))
        controller.run()
        self.loading = False

    def handleEvent(self, event):
        if event.type == pygame.WINDOWRESIZED:
            self.resize()
        # sự kiện chuột
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # nhấn chuột trái
                # print(event.pos)  # in tọa độ chuột
                if not self.loading:
                    if self.startRect.collidepoint(
                        pygame.mouse.get_pos()[0] - self.footer.get_offset()[0],
                        pygame.mouse.get_pos()[1] - self.footer.get_offset()[1],
                    ):
                        self.start()
                        if self.isPause:
                            self.isPause = False
                    elif self.pauseRect.collidepoint(
                        pygame.mouse.get_pos()[0] - self.footer.get_offset()[0],
                        pygame.mouse.get_pos()[1] - self.footer.get_offset()[1],
                    ):
                        self.pause()
                    elif self.nextRect.collidepoint(
                        pygame.mouse.get_pos()[0] - self.footer.get_offset()[0],
                        pygame.mouse.get_pos()[1] - self.footer.get_offset()[1],
                    ):
                        self.running = False
                        self.maze.next()
                    elif self.backRect.collidepoint(
                        pygame.mouse.get_pos()[0] - self.footer.get_offset()[0],
                        pygame.mouse.get_pos()[1] - self.footer.get_offset()[1],
                    ):
                        self.running = False
                        self.maze.back()
                    elif self.restartRect.collidepoint(
                        pygame.mouse.get_pos()[0] - self.footer.get_offset()[0],
                        pygame.mouse.get_pos()[1] - self.footer.get_offset()[1],
                    ):
                        self.isPause = False
                        self.running = False
                        self.maze.restart()
                    elif self.speedRect.collidepoint(
                        pygame.mouse.get_pos()[0] - self.footer.get_offset()[0],
                        pygame.mouse.get_pos()[1] - self.footer.get_offset()[1],
                    ):
                        self.speed *= 2
                        if self.speed > 16:
                            self.speed = 1
                    elif self.menuRect.collidepoint(
                        pygame.mouse.get_pos()[0] - self.footer.get_offset()[0],
                        pygame.mouse.get_pos()[1] - self.footer.get_offset()[1],
                    ):
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT))
                    elif self.previousMapRect.collidepoint(pygame.mouse.get_pos()):
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))
                    elif self.nextMapRect.collidepoint(pygame.mouse.get_pos()):
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT + 2))
                    if self.BFSRect.collidepoint(pygame.mouse.get_pos()):
                        self.setAlgorithm("BFS")
                    elif self.DFSRect.collidepoint(pygame.mouse.get_pos()):
                        self.setAlgorithm("DFS")
                    elif self.UCSRect.collidepoint(pygame.mouse.get_pos()):
                        self.setAlgorithm("UCS")
                    elif self.AStarRect.collidepoint(pygame.mouse.get_pos()):
                        self.setAlgorithm("A*")
                    elif self.regenerateRect.collidepoint(pygame.mouse.get_pos()):
                        self.last_update_time = pygame.time.get_ticks()
                        self.loading = True
                        self.dot_index = 0
                        self.clock = pygame.time.Clock()
                        thread = threading.Thread(target=self.generate)
                        output = open(self.outputFileName, "r").read().split("\n")
                        self.maze.set_output(output)
                        self.maze.restart()
                        thread.start()

            if event.button == 3:
                self.maze.back()

    def loading_screen(self):
        self.fade.fill((0, 0, 0, 128))
        self.screen.blit(self.fade, (0, 0))

        loading = pygame.Surface((self.width // 3, self.height // 3))
        loadingRect = loading.get_rect(center=(self.width // 2, self.height // 2))
        pygame.draw.rect(self.screen, (255, 255, 255), loadingRect, 0, 10)
        pygame.draw.rect(self.screen, (0, 0, 0), loadingRect, 3, 10)
        rotated_image = pygame.transform.rotate(self.loadingImage, self.angle)
        rotated_rect = rotated_image.get_rect(
            center=(
                self.width // 2,
                self.height // 2 - self.loadingImage.get_height() // 4,
            )
        )
        self.screen.blit(rotated_image, rotated_rect)
        text = pygame.font.Font(self.font, loadingRect.height // 6).render(
            "Searching" + "." * self.dot_index, True, (0, 0, 0)
        )
        textRect = text.get_rect(
            center=(
                self.width // 2,
                self.height // 2 + loadingRect.height // 4,
            )
        )
        self.screen.blit(text, textRect)

        # Tăng góc xoay ảnh mỗi lần lặp
        self.angle = (self.angle - 30) % 360  # Xoay 30 độ mỗi lần

        # Cập nhật chỉ số dot_index sau mỗi 1/3 giây
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > 333:  # 333 ms ~ 1/3 giây
            self.dot_index = (self.dot_index + 1) % 4
            self.last_update_time = current_time

            # Giới hạn FPS để giảm tải
        self.clock.tick(10)  # 10 FPS để có khoảng thời gian quay hợp lý
