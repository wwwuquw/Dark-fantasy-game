import pygame
from settings import*
from player import Player
from enemy import Enemy
from tile import Tile
from camera import Camera
class Level:
    def __init__(self, settings):
        self.screen = pygame.display.get_surface()
        self.newareasound = pygame.mixer.Sound("sounds/gaming/new-area2.mp3")
        self.newareasound.set_volume(0.1)
        self.bossoutsound = pygame.mixer.Sound("sounds/gaming/bossout.mp3")
        self.deathsound = pygame.mixer.Sound("sounds/gaming/dark-souls-death-myinstants39.com.mp3")
        self.visible = Camera()
        pygame.mixer.init()
        self.currenttext = None
        #self.visible = pygame.sprite.Group()
        self.settings = settings
        self.colidable = pygame.sprite.Group()
        self.enemys = pygame.sprite.Group()
        self.nextleveldoor = None
        self.currentlevel = 0
        self.backgroung = pygame.transform.scale(pygame.image.load(
            "images/sprites/floor/1673072348_grizly-club-p-tekstura-kamennogo-pola-pikselnaya-17.png"),
                                                 (len(self.settings.map[self.currentlevel][0]) * self.settings.tilewitth,
                                                 len(self.settings.map[self.currentlevel]) * self.settings.tilehight)).convert()
        self.player = Player((self.visible), self.settings.entitysize, (150, 150),self.colidable, self.enemys, self.settings.coldown)
        self.map()

    def map (self):
        self.currenttext = None
        self.newareasound.play()
        for i, row in enumerate(self.settings.map[self.currentlevel]):
            for j, col in enumerate(row):
                if col == "x":
                     Tile((j*32,i*32),(self.visible, self.colidable), self.settings.wallimage)
                elif col == "e":
                     Enemy((self.visible, self.enemys), self.settings.entitysize,(j * 32, i * 32), self.colidable, self.openthedoor, self.player, self.settings.goblinenemyimages, self.settings.coldown)
                elif col == "z":
                    self.nextleveldoor = Tile((j * 32, i * 32), (self.visible, self.colidable), self.settings.wallimage)

    def gameover(self, text):
        text = pygame.font.Font(None, 120).render(text, True, (255, 0 , 0)if text == "YOU DIED" else(255, 255, 0))
        background = text.get_rect(center = (800, 500))
        self.currenttext = text
        self.textbackground = background
        self.deathsound.play()






    def nextlevel(self):
        self.currentlevel += 1
        self.player.rect.topleft = (150,150)
        for sprite in self.visible.sprites():
            if sprite != self.player:
                sprite.kill()
        if self.currentlevel == len(self.settings.map):
            self.gameover("VICTORY ACHIEVED")
            self.bossoutsound.play()
        else:
            self.map()






    def openthedoor(self):
        if len(self.enemys) == 1:
            self.nextleveldoor.collidemethod = self.nextlevel
            self.nextleveldoor.image = self.settings.doorimage






    def run (self):
        if self.player.health < 1:
            self.gameover("YOU DIED")
        if self.currenttext:
            pygame.draw.rect(self.screen, (0, 0, 0), self.textbackground)
            self.screen.blit(self.currenttext, self.textbackground)
        else:
            self.visible.update()
            self.screen.blit(self.backgroung, - self.visible.offset)
            self.visible.draw(self.player)















