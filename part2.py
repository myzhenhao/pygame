import pgzrun
from pgzhelper import *
import random

WIDTH = 900
HEIGHT = 360

# Load images
background = Actor("background1")
background.x = WIDTH // 2
background.y = HEIGHT // 2
player = Actor("player1")
player.x = WIDTH // 2
player.y = HEIGHT - 70

mobs = []
spawn_timer = 0
SPAWN_INTERVAL = 2.0  # seconds

def spawn_mob():
    side = random.choice(['left', 'right'])
    if side == 'left':
        mob = Actor("mob1")
        mob.x = 0
        mob.y = HEIGHT - 70
        mob.flip_x = True
        mobs.append(mob)
    else:
        mob = Actor("mob1")
        mob.x = WIDTH
        mob.y = HEIGHT - 70
        mob.flip_x = False
        mobs.append(mob)

def draw():
    background.draw()
    player.draw()
    for mob in mobs:
        mob.draw()

def update():
    global spawn_timer
    if keyboard.left:
        player.x -= 4
        player.flip_x = True
    if keyboard.right:
        player.x += 4
        player.flip_x = False

    # Mob spawn timer
    spawn_timer += 1 / 60  # assuming 60 FPS
    if spawn_timer >= SPAWN_INTERVAL:
        spawn_mob()
        spawn_timer = 0

    # Move mobs toward player and check collision
    for mob in mobs:  # iterate over a copy for safe removal
        if mob.x < player.x:
            mob.x += 2
        elif mob.x > player.x:
            mob.x -= 2
        if mob.colliderect(player):
            mobs.remove(mob)

pgzrun.go()
