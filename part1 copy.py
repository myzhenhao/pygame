import pgzrun
from pgzhelper import *
WIDTH = 900
HEIGHT = 360

# Load images
background = Actor("background1")
background.x = WIDTH // 2
background.y = HEIGHT // 2
player = Actor("player1")
player.x = WIDTH // 2
player.y = HEIGHT - 70

def draw():
    screen.clear()
    background.draw()
    player.draw()


def update():
    if keyboard.left:
        player.x -= 4
        player.flip_x = True
    if keyboard.right:
        player.x += 4
        player.flip_x = False
    if player.x < 30:
        player.x = 30
    if player.x > 870:
        player.x = 870

pgzrun.go()
