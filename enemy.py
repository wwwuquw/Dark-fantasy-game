import pygame
from settings import*

class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, size, pos, colidable, ondeathmethod, player, images, coldown):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.roarsound = pygame.mixer.Sound("sounds/attack/enemys/mixkit-nasty-criature-roar-2781.wav")
        self.colidable = colidable
        self.coldown = coldown
        self.times = {"attack": pygame.time.get_ticks()}
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft = pos)
        self.dir = pygame.math.Vector2()
        self.health = 60
        self.frame = 0
        self.animationspeed = 0.08
        self.speed = 1
        self.izopos = pygame.math.Vector2()
        self.images = images
        self.status = "right"
        self.image = self.images[self.status][0].copy()
        self.onedeathmethod = ondeathmethod
        self.player=player

    def healthbar (self):
        pygame.draw.rect(self.image,(0, 0, 0), (0, 0 , self.rect.width, self.rect.height * 0.1))
        pygame.draw.rect(self.image, (255, 0, 0), (0,0, self.rect.width * (self.health / 60), self.rect.height * 0.1))






    def AI (self):
        distance = pygame.math.Vector2(self.player.rect.left - self.rect.left, self.player.rect.top - self.rect.top).magnitude()
        if  64 < distance < 256:
            self.dir = pygame.math.Vector2(self.player.rect.left - self.rect.left, self.player.rect.top - self.rect.top).normalize()
        elif distance < 64:
            self.dir = pygame.math.Vector2()
            self.player.health -= 1
            if "attack" not in self.status:
                self.status += " attack"
                self.roarsound.play()
                self.roarsound.set_volume(0.1)
        if self.dir.x > 0:
            self.status = "right"
        elif self.dir.x < 0:
            self.status = "left"





    def convertcoordinates(self):
        self.izopos.x = (self.rect.left-self.rect.top) * self.rect.width
        self.izopos.y = (self.rect.left+self.rect.top) * self.rect.height



    def moove(self):
        self.rect.left += self.dir.x * self.speed
        self.callite(True)
        self.rect.top += self.dir.y * self.speed
        self.callite(False)

    def callite(self, dir):
        if dir:
            for sprite in self.colidable.sprites():
                if self.rect.colliderect(sprite.rect):
                    if self.dir.x < 0:
                        self.rect.left = sprite.rect.right
                    elif self.dir.x > 0:
                        self.rect.right = sprite.rect.left
        else:
            for sprite in self.colidable.sprites():
                if self.rect.colliderect(sprite.rect):
                    if self.dir.y < 0:
                        self.rect.top = sprite.rect.bottom
                    elif self.dir.y > 0:
                        self.rect.bottom = sprite.rect.top

    def animate(self):
        self.frame += self.animationspeed
        if self.frame >= len(self.images[self.status]):
            self.frame = 0
        self.image = self.images[self.status][int(self.frame)].copy()






    def update(self):
        if self.coldown(self.times["attack"], 400):
            self.times["attack"] = pygame.time.get_ticks()
            self.AI()
        self.moove()
        self.animate()
        self.healthbar()
