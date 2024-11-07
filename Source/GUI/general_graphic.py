import pygame

sheet = pygame.image.load("GUI/sheet.png")
wall = sheet.subsurface(4 + (24 + 4) * 6, 4 + (24 + 4) * 2, 24, 24)
freeSpace = sheet.subsurface(4, 4 + (24 + 4) * 2, 24, 24)
stone = sheet.subsurface(4, 4 + (24 + 4), 24, 24)
AresUp = [
    sheet.subsurface(4 + (24 + 4), 4, 24, 24),
    sheet.subsurface(4, 4, 24, 24),
    sheet.subsurface(4 + (24 + 4) * 2, 4, 24, 24),
]
AresLeft = [
    sheet.subsurface(4 + (24 + 4) * 7, 4, 24, 24),
    sheet.subsurface(4 + (24 + 4) * 6, 4, 24, 24),
    sheet.subsurface(4 + (24 + 4) * 8, 4, 24, 24),
]
AresDown = [pygame.transform.flip(ares, False, True) for ares in AresUp]
AresRight = [pygame.transform.flip(ares, True, False) for ares in AresLeft]
AresPushUp = [
    sheet.subsurface(4 + (24 + 4) * 4, 4, 24, 24),
    sheet.subsurface(4 + (24 + 4) * 3, 4, 24, 24),
    sheet.subsurface(4 + (24 + 4) * 5, 4, 24, 24),
]
AresPushLeft = [
    sheet.subsurface(4 + (24 + 4) * 10, 4, 24, 24),
    sheet.subsurface(4 + (24 + 4) * 9, 4, 24, 24),
    sheet.subsurface(4 + (24 + 4) * 11, 4, 24, 24),
]
AresPushDown = [pygame.transform.flip(ares, False, True) for ares in AresPushUp]
AresPushRight = [pygame.transform.flip(ares, True, False) for ares in AresPushLeft]
Ares = [
    AresUp,
    AresLeft,
    AresDown,
    AresRight,
    AresPushUp,
    AresPushLeft,
    AresPushDown,
    AresPushRight,
]
switchPlace = sheet.subsurface(4 + (24 + 4), 4 + (24 + 4) * 2, 24, 24)
stonePlacedOnSwitch = sheet.subsurface(4 + (24 + 4), 4 + (24 + 4), 24, 24)
other = sheet.subsurface(4, 4 + (24 + 4) * 3, 24, 24)
componentSize = 24
font = "GUI/MinecraftBold.otf"
