"""Game view"""

import pygame
from src.views.view import View
from src.managers.gamesprite import GameSpriteManager
from src.config import WIDTH, INITIAL_SPEED

import src.views.gameover as gameover

class Game(View):
    """Main game view class"""
    def __init__(self, state: dict) -> None:
        super().__init__(state)
        pygame.display.set_caption("Traffic Evader")

        self.sprites = GameSpriteManager(self.state)
        
        self.score_text = self.fonts.font_score.render("0", True, "black")

        self.frame_count = 0
        self.speed = INITIAL_SPEED
        self.score = 0

        self.exploding = False

    def process_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.sprites.player.move_left()
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.sprites.player.move_right()

    def update(self) -> None:
        # Special state: While explosion is happening,
        # (before moving to game over screen), no other updates are executed
        if self.exploding:
            self.sprites.explosion.update()
            if self.sprites.explosion.animation_finished:
                self.active = False
            return

        self.sprites.update(self.speed)
        self.sprites.spawn_road_objects(self.speed)
        self.sprites.despawn_obsolete()

        collided = pygame.sprite.spritecollideany(self.sprites.player, self.sprites.obstacles, pygame.sprite.collide_mask)

        if collided:
            self.exploding = True
            self.sounds.explosion.play()
            self.sprites.spawn_explosion(collided)
            self.transition_to = gameover.GameOver(self.state)

        # Third argument specifies to remove any coins collected from the coin sprite group
        coins_collected = pygame.sprite.spritecollide(self.sprites.player, self.sprites.coins, True, pygame.sprite.collide_mask)

        self.score += len(coins_collected)
        if len(coins_collected) > 0 and self.score % 10 == 0:
            self.sounds.coin.play()

        self.score_text = self.fonts.font_score.render(str(self.score), True, "black")

        self.frame_count += 1
        # Each "speed level" duration is constantly increasing
        # (speed is 2 for 1200 frames, speed is 5 for 6000 frames, etc)
        if self.frame_count >= self.speed * 600:
            self.frame_count = 0
            self.speed += 1

    def render(self) -> None:
        """Render: Fill background, blit sprites, etc"""
        self.screen.fill((255, 255, 255))

        self.sprites.draw(self.screen)
        self.screen.blit(self.score_text, (WIDTH - 100, 25))

        if self.exploding:
            self.sprites.explosion.draw(self.screen)

        pygame.display.flip()
