import sys
import time
from sprites import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()

        self.player = Player(self.all_sprites)
        self.stage_setup()
        self.ball = Ball(self.all_sprites, self.player, self.block_sprites)

    def stage_setup(self):
        for index_row, row in enumerate(BLOCK_MAP):
            for index_col, col in enumerate(row):
                if col != " ":
                    x = index_col * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE // 2
                    y = index_row * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE // 2
                    Block(col, (x, y), [self.all_sprites, self.block_sprites])

    def run(self):
        last_time = time.time()
        while True:
            dt = time.time() - last_time
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball.active = True

            self.screen.fill("black")

            # join
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.screen)

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
