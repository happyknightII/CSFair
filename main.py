import math
import random

import pygame
from player import Player
from healthBar import HealthBar
from laserBar import LaserBar
from laser import Laser
from enemyDodge import EnemyDodge
from enemy import Enemy
from comet import Comet


pygame.init()
pygame.display.set_caption('Spacey 2.0')

DIFFICULTY = 5000
# Set up the drawing window
screen = pygame.display.set_mode([1500, 1000])
screenSize = screen.get_size()
# Run until the user asks to quit
running = True
player = Player(screenSize, screenSize[0] * 0.05)
health_bar = HealthBar(coord=(screenSize[0] * 0.1, screenSize[1] - screenSize[0] * 0.1), bar_length=screenSize[0] * 0.3)
laser_bar = LaserBar(coord=(screenSize[0] * 0.9, screenSize[0] * 0.1), bar_length=screenSize[0] * 0.03)
player_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
enemy_laser_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
comet_group = pygame.sprite.Group()
player_group.add(player)

frameIndex = 0
clock = pygame.time.Clock()
last_shot = pygame.time.get_ticks()
level = 1
max_comet = 10
last_enemy = pygame.time.get_ticks()
SPAWN_RATE = 700
last_spawned = pygame.time.get_ticks()

font = pygame.font.Font('freesansbold.ttf', int(screenSize[0] * 0.1))
kills = 0
bruh = True
while running and bruh:
    frameIndex += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            bruh = False

    if len(comet_group) < max_comet:
        comet_group.add(Comet(screenSize, random.random() > 0.5, screenSize[0] * 0.05))

    screen.fill((0, 0, 20))
    player.rotate(pygame.mouse.get_pos())
    player_group.update()
    comet_group.update()
    gameOverIndicator = font.render('Spacey 2.0', True, (30, 30, 30))
    screen.blit(gameOverIndicator, (screenSize[0] * 0.08, screenSize[1] * 0.45))

    comet_group.draw(screen)
    player_group.draw(screen)

    if frameIndex % 50 < 20:
        gameOverIndicator = font.render('Spacey 2.0', True, (50, 50, 50))
        screen.blit(gameOverIndicator, (screenSize[0] * 0.08, screenSize[1] * 0.45))

    pygame.display.flip()
    dt = clock.tick(60)
player_group.add(health_bar)
player_group.add(laser_bar)

while running:
    frameIndex += 1

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((0, 0, 20))

    # Draw a solid blue circle in the center
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.move(-1, 0)
    elif keys[pygame.K_d]:
        player.move(1, 0)
    if keys[pygame.K_w]:
        player.move(-1, 1)
    elif keys[pygame.K_s]:
        player.move(1, 1)
    if pygame.mouse.get_pressed()[0] and player.fire():
        laser_group.add(Laser(screenSize, screenSize[0] * 0.05, player.pos, player.angle, player.speed, True))
        last_shot = pygame.time.get_ticks()

    player.rotate(pygame.mouse.get_pos())

    if len(enemy_group) < level / 2 and pygame.time.get_ticks() - last_spawned > SPAWN_RATE:
        if random.random() > 0.2:
            enemy_group.add(Enemy(screenSize, screenSize[0] * 0.05))
        else:
            enemy_group.add(EnemyDodge(screenSize, screenSize[0] * 0.05))
        last_spawned = pygame.time.get_ticks()
    if len(comet_group) < max_comet:
        comet_group.add(Comet(screenSize, random.random() > 0.5, screenSize[0] * 0.05))

    if pygame.time.get_ticks() - last_enemy > DIFFICULTY:
        level += 1
        SPAWN_RATE /= 1.001
        last_enemy = pygame.time.get_ticks()

    aa = pygame.sprite.groupcollide(laser_group, comet_group, False, False)
    for a in aa:
        if a.dying == 10:
            a.collide()

    ba = pygame.sprite.groupcollide(enemy_laser_group, comet_group, True, False)
    for b in ba:
        if b.dying == 10:
            b.collide()
    collided = pygame.sprite.groupcollide(enemy_group, laser_group, False, True)
    pygame.sprite.groupcollide(laser_group, enemy_laser_group, True, True)
    collided_enemy_laser = pygame.sprite.spritecollideany(player, enemy_laser_group)
    if collided_enemy_laser:
        if collided_enemy_laser.dying == 10:
            player.health -= 5
            collided_enemy_laser.collide()
    collided_enemy = pygame.sprite.spritecollideany(player, enemy_group)
    if collided_enemy:
        if collided_enemy.dying == 10:
            player.health -= 10
            collided_enemy.collide()
            kills += level
    for enemy_object in collided:
        enemy_object.collide()
        kills += level
    for enemy_object in enemy_group:
        if enemy_object.canShoot and pygame.time.get_ticks() - enemy_object.lastFired > 4000:
            enemy_object.lastFired = pygame.time.get_ticks()
            enemy_laser_group.add(Laser(screenSize, screenSize[0] * 0.05, enemy_object.pos, enemy_object.angle + 180, enemy_object.speed, False, speed=10))

    health_bar.current_health = player.health
    laser_bar.current_level = player.ammo
    player_group.update()
    laser_group.update()
    enemy_laser_group.update()
    enemy_group.update(player.pos)
    comet_group.update()
    levelIndicator = font.render(f'Level: {level}', True, (10, 10, 30))
    screen.blit(levelIndicator, (screenSize[0] * 0.1, screenSize[1] * 0.2))
    levelIndicator = font.render(f'Score: {kills}', True, (10, 10, 30))
    screen.blit(levelIndicator, (screenSize[0] * 0.1, screenSize[1] * 0.7))
    laser_group.draw(screen)
    enemy_laser_group.draw(screen)
    comet_group.draw(screen)
    player_group.draw(screen)
    enemy_group.draw(screen)
    if player.health <= 0:
        break

    # Flip the display
    pygame.display.flip()
    dt = clock.tick(60)
health_bar.kill()
laser_bar.kill()

while running:
    frameIndex += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 20))
    player_group.update()
    comet_group.update()
    levelIndicator = font.render(f'Level: {level}', True, (10, 10, 30))
    screen.blit(levelIndicator, (screenSize[0] * 0.1, screenSize[1] * 0.2))
    gameOverIndicator = font.render(f'GAME OVER!', True, (30, 30, 30))
    screen.blit(gameOverIndicator, (screenSize[0] * 0.08, screenSize[1] * 0.45))
    levelIndicator = font.render(f'Score: {kills}', True, (10, 10, 30))
    screen.blit(levelIndicator, (screenSize[0] * 0.1, screenSize[1] * 0.7))

    comet_group.draw(screen)
    player_group.draw(screen)
    if frameIndex % 50 < 20:
        levelIndicator = font.render(f'Level: {level}', True, (30, 30, 30))
        screen.blit(levelIndicator, (screenSize[0] * 0.1, screenSize[1] * 0.2))
        gameOverIndicator = font.render(f'GAME OVER!', True, (50, 50, 50))
        screen.blit(gameOverIndicator, (screenSize[0] * 0.08, screenSize[1] * 0.45))
        levelIndicator = font.render(f'Score: {kills}', True, (30, 30, 30))
        screen.blit(levelIndicator, (screenSize[0] * 0.1, screenSize[1] * 0.7))
    pygame.display.flip()
    dt = clock.tick(60)
# Done! Time to quit.
pygame.quit()
