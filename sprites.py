import pygame
from setting import *
from random import choice


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.width = 200
        self.height = 30
        # image
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill("yellow")

        # pos
        self.rect = self.image.get_rect(midbottom=(WIN_WIDTH // 2, WIN_HEIGHT - 50))
        self.old_rect = self.rect.copy()

        # moving
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.dir = pygame.math.Vector2()
        self.speed = 500

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.dir.x = 1
        elif keys[pygame.K_a]:
            self.dir.x = -1
        else:
            self.dir.x = 0

    def win_collision(self):
        if self.rect.right > WIN_WIDTH:
            self.rect.right = WIN_WIDTH
            self.pos.x = self.rect.x
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.x

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.win_collision()
        self.pos.x += self.dir.x * self.speed * dt
        self.rect.x = round(self.pos.x)


class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, player, blocks):
        super().__init__(groups)

        # collision sprites
        self.player = player
        self.blocks = blocks

        # image
        self.image = pygame.Surface((30, 30))
        self.image.fill("red")

        # pos
        self.rect = self.image.get_rect(midbottom=player.rect.midtop)
        self.old_rect = self.rect.copy()

        # moving
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.dir = pygame.math.Vector2((choice((1, -1)), -1))
        self.speed = 1200

        self.active = False

    def win_collision(self, dir):
        if dir == "h":
            if self.rect.left < 0:
                self.rect.left = 0
                self.pos.x = self.rect.x
                self.dir.x *= -1

            if self.rect.right > WIN_WIDTH:
                self.rect.right = WIN_WIDTH
                self.pos.x = self.rect.x
                self.dir.x *= -1

        if dir == "v":
            if self.rect.top < 0:
                self.rect.top = 0
                self.pos.y = self.rect.y
                self.dir.y *= -1

            if self.rect.bottom > WIN_HEIGHT:
                self.rect.bottom = WIN_HEIGHT
                self.pos.y = self.rect.y
                self.dir.y *= -1

            # if self.rect.bottom > WIN_HEIGHT:
            #     self.active = False
            #     self.dir.y = -1

    def collision(self, dir):
        all_sprites = pygame.sprite.spritecollide(self, self.blocks, False)
        if self.rect.colliderect(self.player.rect):
            all_sprites.append(self.player)

        if all_sprites:
            if dir == "h":
                for s in all_sprites:
                    if self.rect.right >= s.rect.left and self.old_rect.right <= s.old_rect.left:
                        self.rect.right = s.rect.left - 1
                        self.pos.x = self.rect.x
                        self.dir.x *= -1

                    if self.rect.left <= s.rect.right and self.old_rect.left >= s.old_rect.right:
                        self.rect.left = s.rect.right + 1
                        self.pos.x = self.rect.x
                        self.dir.x *= -1

                    if getattr(s, "health", None):
                        s.get_damage(1)

            if dir == "v":
                for s in all_sprites:
                    if self.rect.bottom >= s.rect.top and self.old_rect.bottom <= s.old_rect.top:
                        self.rect.bottom = s.rect.top - 1
                        self.pos.y = self.rect.y
                        self.dir.y *= -1

                    if self.rect.top <= s.rect.bottom and self.old_rect.top >= s.old_rect.bottom:
                        self.rect.top = s.rect.bottom + 1
                        self.pos.y = self.rect.y
                        self.dir.y *= -1

                    if getattr(s, "health", None):
                        s.get_damage(1)

    def update(self, dt):
        self.old_rect = self.rect.copy()

        if self.active:
            if self.dir.magnitude() != 0:
                self.dir = self.dir.normalize()

                self.pos.x += self.dir.x * self.speed * dt
                self.rect.x = round(self.pos.x)
                self.collision("h")
                self.win_collision("h")

                self.pos.y += self.dir.y * self.speed * dt
                self.rect.y = round(self.pos.y)
                self.collision("v")
                self.win_collision("v")

        else:
            self.rect.midbottom = self.player.rect.midtop
            self.pos = pygame.math.Vector2(self.rect.topleft)


class Block(pygame.sprite.Sprite):
    def __init__(self, block_type, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.fill("white")
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()

        self.health = int(block_type)

    def get_damage(self, amount):
        self.health -= amount

        if self.health > 0:
            pass
        else:
            self.kill()
