import pygame
from settings import*

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, size, pos, colidable, enemys, coldown):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.colidable = colidable
        self.enemys = enemys
        self.attacksound = pygame.mixer.Sound("sounds/attack/player/mixkit-metal-hit-woosh-1485.wav")
        self.attacksound.set_volume(0.5)
        self.health = 100
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft = pos)
        self.dir = pygame.math.Vector2()
        self.cameraoffset = pygame.math.Vector2()
        self.coldown = coldown
        self.times = {"attack": pygame.time.get_ticks()}
        self.status = "right"
        self.images = {"right": pygame.transform.scale(pygame.image.load(
            "images/player/right/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.u1.png"), size),
                     "left": pygame.transform.scale(pygame.image.load(
                         "images/player/left/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.u1 (1).png"), size)}
        self.speed = 1
        self.image = self.images[self.status]
        self.izopos = pygame.math.Vector2()

    def attack(self):
        key = pygame.math.Vector2(pygame.mouse.get_pos()) + self.cameraoffset
        for enemy in self.enemys.sprites():
            if enemy.rect.collidepoint(key):
                distance = pygame.math.Vector2(enemy.rect.left - self.rect.left, enemy.rect.top - self.rect.top).magnitude()
                if distance < self.rect.width*1.5:
                    enemy.health -=10
                    self.attacksound.play()

                    if enemy.health <= 0:
                        enemy.onedeathmethod()
                        enemy.kill()






    def input (self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:self.dir.y = -1
        elif keys[pygame.K_s]:self.dir.y = 1
        else:self.dir.y = 0
        if keys[pygame.K_a]:
            self.dir.x = -1
            self.status = "left"
            self.image = self.images[self.status]
        elif keys[pygame.K_d]:
            self.dir.x = 1
            self.status = "right"
            self.image = self.images[self.status]
        else:self.dir.x = 0
        keys = pygame.mouse.get_pressed()
        if keys[0] and self.coldown(self.times["attack"], 500):
            self.attack()
            self.times["attack"] = pygame.time.get_ticks()



    def healthbar(self):
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, self.rect.width, self.rect.height * 0.1))
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, self.rect.width * (self.health / 60), self.rect.height * 0.1))



    def moove(self):
        self.rect.left += self.dir.x * self.speed
        self.callite(True)
        self.rect.top+=self.dir.y * self.speed
        self.callite(False)

    def callite(self, dir):
        if dir:
            for sprite in self.colidable.sprites():
                if self.rect.colliderect(sprite.rect):
                    if self.dir.x < 0:
                        self.rect.left = sprite.rect.right
                    elif self.dir.x > 0:
                        self.rect.right = sprite.rect.left
                    if sprite.collidemethod:
                        sprite.collidemethod()

        else:
            for sprite in self.colidable.sprites():
                if self.rect.colliderect(sprite.rect):
                    if self.dir.y < 0:
                        self.rect.top = sprite.rect.bottom
                    elif self.dir.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if sprite.collidemethod:
                        sprite.collidemethod()



    def update(self):
        self.input()
        self.moove()
        self.healthbar()

