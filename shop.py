import pgzrun
from pgzhelper import *

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Sword buttons
swords = [
    {"name": "Sword 1", "image": "sword1", "x": 200, "y": 300},
    {"name": "Sword 2", "image": "sword2", "x": 400, "y": 300},
    {"name": "Sword 3", "image": "sword3", "x": 600, "y": 300}
]

# Create Actor objects for each sword
sword_actors = []
for sword in swords:
    actor = Actor(sword["image"], pos=(sword["x"], sword["y"]))
    actor.sword_name = sword["name"]  # Store the name with the actor
    actor.scale = 0.2  # Set initial scale to 0.2
    sword_actors.append(actor)

def draw():
    screen.clear()
    screen.fill((50, 50, 50))  # Dark gray background
    
    # Draw title
    screen.draw.text("Weapon Shop", center=(WIDTH // 2, 50), fontsize=48, color="white")
    
    # Draw all sword buttons
    for actor in sword_actors:
        actor.draw()
        # Draw the sword name below each sword
        screen.draw.text(
            actor.sword_name,
            center=(actor.x, actor.y + 60),
            fontsize=20,
            color="white"
        )

def on_mouse_move(pos):
    """Handle mouse hover - scale to 0.5 when mouse approaches"""
    for actor in sword_actors:
        if actor.collidepoint(pos):
            actor.scale = 0.3  # Scale up when mouse hovers
        else:
            actor.scale = 0.2  # Reset to default when mouse moves away

def on_mouse_down(pos):
    """Handle mouse clicks on sword buttons"""
    for actor in sword_actors:
        if actor.collidepoint(pos):
            print(actor.sword_name)

pgzrun.go()