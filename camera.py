import pygame
class Camera(pygame.sprite.Group):
    def __init__(self):
       super().__init__()
       self.screen = pygame.display.get_surface()
       self.halfwidth = self.screen.get_width() // 2
       self.halfheight = self.screen.get_height() // 2
       self.offset = pygame.math.Vector2()
    def draw(self, player):
        self.offset.x = player.rect.left - self.halfwidth
        self.offset.y = player.rect.top - self.halfheight
        player.cameraoffset = self.offset
        for sprite in self.sprites():
            offset=(
                sprite.rect.left - self.offset.x,
                sprite.rect.top - self.offset.y
            )
            self.screen.blit(sprite.image, offset)





