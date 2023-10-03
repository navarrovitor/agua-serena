import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.sprites = []
        self.is_moving = False
        for i in range(8):
            self.sprites.append(
                pygame.image.load(f"assets/sprites/{name}/walking({i}).png")
            )
        self.sprites.append(
            pygame.image.load(f"assets/sprites/{name}/idle.png")
        )
        # self.current_sprite = 8
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.side = 0

    def animate(self):
        self.is_moving = True

    # todo: add logic to sprite side (left or right looking)
    def update(self, speed):
        if self.is_moving == True:
            self.current_sprite += speed

            if self.current_sprite >= 7:
                self.current_sprite = 0
                self.is_moving = False

            self.image = self.sprites[int(self.current_sprite)]

        # todo: add logic to idle sprite
        # else:
        #     self.current_sprite = 8
