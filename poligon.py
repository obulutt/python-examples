""""
yön tuşları ile sağa sola hareket edip space tuşu ile atış yapabilirsiniz
hedefi 3 saniye içerisinde vuramazsanız hedef kaybolur
"""

import pygame
import sys
import random

# Pygame'i başlat
pygame.init()

# Ekran boyutları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Silahlı Hedef Vurma Oyunu')

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# FPS
clock = pygame.time.Clock()
FPS = 60


class Target:
    def __init__(self):
        self.size = 50
        self.x = random.randint(self.size, SCREEN_WIDTH - self.size)
        self.y = random.randint(self.size, SCREEN_HEIGHT - self.size)
        self.color = RED
        self.spawn_time = pygame.time.get_ticks()

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def is_hit(self, pos):
        return (self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2 < self.size ** 2


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10

    def update(self):
        self.y -= self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, 5, 10))

    def is_off_screen(self):
        return self.y < 0


class Gun:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 50
        self.speed = 10

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x < SCREEN_WIDTH - 50:
            self.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, 50, 20))


def main():
    running = True
    targets = [Target()]
    bullets = []
    gun = Gun()
    score = 0
    font = pygame.font.SysFont(None, 36)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(gun.x + 22, gun.y))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            gun.move_left()
        if keys[pygame.K_RIGHT]:
            gun.move_right()

        screen.fill(BLACK)

        for target in targets:
            target.draw()

        for bullet in bullets:
            bullet.update()
            bullet.draw()
            if bullet.is_off_screen():
                bullets.remove(bullet)

        for bullet in bullets:
            for target in targets:
                if target.is_hit((bullet.x, bullet.y)):
                    targets.remove(target)
                    bullets.remove(bullet)
                    targets.append(Target())
                    score += 1

        gun.draw()

        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        for target in targets:
            if pygame.time.get_ticks() - target.spawn_time > 3000:
                targets.remove(target)
                targets.append(Target())

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
