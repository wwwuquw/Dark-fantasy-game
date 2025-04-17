import pygame,sys
from settings import*
from level import Level


pygame.init()
screen=pygame.display.set_mode((1600,1000))
pygame.display.set_caption("Beveled")
clock=pygame.time.Clock()
settings=Settings()
level=Level(settings)
screenimage = pygame.transform.scale(pygame.image.load("images/sprites/screenimage/1611531566_preview_Image-Wiki-background-Darkest-Dungeon-Wiki-FANDOM-.jpg"),(1600,1000)).convert()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0,0,0))
    screen.blit(screenimage, (0, 0))
    level.run()


    pygame.display.update()
    clock.tick()






