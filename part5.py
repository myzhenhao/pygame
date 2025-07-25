import pgzrun
from pgzhelper import *
import random

WIDTH = 900
HEIGHT = 360

# Load images
background1 = Actor("background1")
background1.x = WIDTH // 2
background1.y = HEIGHT // 2
background2 = Actor("background2")
background2.x = WIDTH // 2
background2.y = HEIGHT // 2
player = Actor("player1")
player.x = WIDTH // 2
player.y = HEIGHT - 70
player.vy = 0
player.on_ground = True

mobs = []
spawn_timer = 0
SPAWN_INTERVAL = 2.0  # seconds

player_lives = 3

fireballs = []
score = 0

# Level state
level = 1

# Initial platforms for level 1
platforms = [
    Actor("platform1", (200, 250)),
    Actor("platform1", (350, 180)),
    Actor("platform1", (700, 300)),
]

# Level 2 platforms
platforms_level2 = [
    Actor("platform2", (120, 260)),
    Actor("platform2", (300, 200)),
    Actor("platform2", (480, 150)),
    Actor("platform2", (650, 220)),
    Actor("platform2", (800, 300)),
]

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
    screen.clear()
    if level == 1:
        background1.draw()
    else:
        background2.draw()
    for platform in platforms:
        platform.draw()
    player.draw()
    for mob in mobs:
        mob.draw()
    for fireball in fireballs:
        fireball.draw()
    screen.draw.text(f"Lives: {player_lives}", (10, 10), color=(255,255,255), fontsize=40)
    screen.draw.text(f"Score: {score}", (10, 50), color="yellow", fontsize=40)

def update():
    global spawn_timer, player_lives, score, level, platforms

    # Player movement
    if keyboard.left:
        player.x -= 4
        player.flip_x = True
    if keyboard.right:
        player.x += 4
        player.flip_x = False

    # Gravity and jump
    player.y += player.vy
    if not player.on_ground:
        player.vy += 0.5  # gravity

    # Platform collision
    player.on_ground = False
    for platform in platforms:
        # Check if player is falling and feet are above the platform, and will land on it
        if (
            player.vy >= 0 and
            player.y  <= platform.y and
            player.y + player.height/2 + player.vy >= platform.y - platform.height/2 and
            abs(player.x - platform.x) < (platform.width/2 + player.width/2 - 10)
        ):
            player.y = platform.y - platform.height/2 - player.height/2
            print(f"{player.y} and {platform.y}")
            player.vy = 0
            player.on_ground = True
            break

    # Check if player is on the ground (only set to True if not already on a platform)
    if not player.on_ground and player.y >= HEIGHT - 70:
        player.y = HEIGHT - 70
        player.vy = 0
        player.on_ground = True

    # Mob spawn timer
    spawn_timer += 1 / 60
    if spawn_timer >= SPAWN_INTERVAL:
        spawn_mob()
        spawn_timer = 0

    # Move mobs and check collision
    for mob in mobs:
        if mob.x < player.x:
            mob.x += 2
        elif mob.x > player.x:
            mob.x -= 2
        if mob.colliderect(player):
            mobs.remove(mob)
            player_lives -= 1

    # Move fireballs and check collision with mobs
    for fireball in fireballs:
        if fireball.flip_x:
            fireball.x -= 8
        else:
            fireball.x += 8
        # Remove fireball if it goes off screen
        if fireball.x < 0 or fireball.x > WIDTH:
            fireballs.remove(fireball)
            continue

        for mob in mobs:
            if fireball.colliderect(mob):
                mobs.remove(mob)
                if fireball in fireballs:
                    fireballs.remove(fireball)
                score += 1
                break

    # Level up logic
    if level == 1 and score > 5:
        level = 2
        platforms = platforms_level2
        player.x = WIDTH // 2
        player.y = HEIGHT - 70
        player.vy = 0
        player.on_ground = True

def on_key_down(key):
    if key == keys.SPACE and player.on_ground:
        player.vy = -10
        player.on_ground = False
    if key == keys.A:
        # Shoot fireball
        fireball = Actor("fireball")
        fireball.y = player.y
        fireball.x = player.x
        # Set direction based on player facing
        fireball.vx = 8 
        if player.flip_x:
            fireball.flip_x = True
        else:
            fireball.flip_x = False
        fireballs.append(fireball)

pgzrun.go()
