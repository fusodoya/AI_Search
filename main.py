import pygame
from pygame._sdl2.video import Window
from GUI.MazeScreen import MazeScreen
from GUI.MenuScreen import MenuScreen

# khởi tạo pygame
pygame.init()

# tạo cửa sổ giao diện trong pygame
screen = pygame.display.set_mode((500, 600), pygame.RESIZABLE)
pygame.display.set_caption("Project 1. Search")

# khai báo màu nền cho giao diện
BACKGROUND_COLOR = (100, 100, 100)

# biến vòng lặp game
running = True

#
Window.from_display_module().maximize()

mazeScreens = [
    MazeScreen(screen, f"input-{i:02d}.txt", f"output-{i:02d}.txt")
    for i in range(1, 11)
]
menuScreen = MenuScreen(screen, [mazeScreen.preview() for mazeScreen in mazeScreens])

runningMenuScreen = True
runningMazeScreen = False
input = 0
background = pygame.image.load("GUI/image_BackgroundIntro.png")
#

# game loop
while running:

    while runningMenuScreen:

        # vẽ màu nền
        screen.fill(BACKGROUND_COLOR)
        scale = max(
            screen.get_width() / background.get_width(),
            screen.get_height() / background.get_height(),
        )
        scalebackground = pygame.transform.scale(
            background,
            (int(background.get_width() * scale), int(background.get_height() * scale)),
        )
        screen.blit(scalebackground, (0, 0))

        # xử lý sự kiện
        for event in pygame.event.get():
            # sự kiện thoát
            if event.type == pygame.QUIT:
                runningMenuScreen = False
                running = False
            elif event.type > pygame.USEREVENT and event.type <= pygame.USEREVENT + 10:
                runningMenuScreen = False
                runningMazeScreen = True
                input = event.type - pygame.USEREVENT - 1
                mazeScreens[input].resize()
            elif event.type == pygame.USEREVENT + 11:
                mazeScreens[input].setAlgorithm("BFS")
            elif event.type == pygame.USEREVENT + 12:
                mazeScreens[input].setAlgorithm("DFS")
            elif event.type == pygame.USEREVENT + 13:
                mazeScreens[input].setAlgorithm("UCS")
            elif event.type == pygame.USEREVENT + 14:
                mazeScreens[input].setAlgorithm("A*")
            else:
                menuScreen.handleEvent(event)

        menuScreen.draw()

        # vẽ tất cả lên màn hình
        pygame.display.update()

    while runningMazeScreen:

        # vẽ màu nền
        screen.fill(BACKGROUND_COLOR)
        scale = max(
            screen.get_width() / background.get_width(),
            screen.get_height() / background.get_height(),
        )
        scalebackground = pygame.transform.scale(
            background,
            (int(background.get_width() * scale), int(background.get_height() * scale)),
        )
        screen.blit(scalebackground, (0, 0))

        # xử lý sự kiện
        for event in pygame.event.get():
            # sự kiện thoát
            if event.type == pygame.QUIT:
                runningMazeScreen = False
                running = False
            elif event.type == pygame.USEREVENT:
                runningMazeScreen = False
                runningMenuScreen = True
                menuScreen.resize()
            elif event.type == pygame.USEREVENT + 1:
                algorithm = mazeScreens[input].maze.algorithm
                input = (input - 1) % 10
                mazeScreens[input].setAlgorithm(algorithm)
                mazeScreens[input].resize()
            elif event.type == pygame.USEREVENT + 2:
                algorithm = mazeScreens[input].maze.algorithm
                input = (input + 1) % 10
                mazeScreens[input].setAlgorithm(algorithm)
                mazeScreens[input].resize()
            else:
                mazeScreens[input].handleEvent(event)

        mazeScreens[input].draw()

        # vẽ tất cả lên màn hình
        pygame.display.update()

# thoát chương trình
pygame.quit()
