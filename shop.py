import pgzrun
from pgzhelper import *

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Player money
player_money = 1000

# Inventory - tracks purchased items (sword_name -> quantity)
inventory = {}

# Sword buttons with prices
swords = [
    {"name": "Sword 1", "image": "sword1", "x": 200, "y": 300, "price": 200},
    {"name": "Sword 2", "image": "sword2", "x": 400, "y": 300, "price": 350},
    {"name": "Sword 3", "image": "sword3", "x": 600, "y": 300, "price": 500}
]

# Create Actor objects for each sword
sword_actors = []
for sword in swords:
    actor = Actor(sword["image"], pos=(sword["x"], sword["y"]))
    actor.sword_name = sword["name"]  # Store the name with the actor
    actor.price = sword["price"]  # Store the price with the actor
    actor.scale = 0.2  # Set initial scale to 0.2
    sword_actors.append(actor)

def draw():
    screen.clear()
    screen.fill((50, 50, 50))  # Dark gray background
    
    # Draw title
    screen.draw.text("Weapon Shop", center=(WIDTH // 2, 50), fontsize=48, color="white")
    
    # Draw player money
    screen.draw.text(
        f"Money: ${player_money}",
        topleft=(20, 20),
        fontsize=24,
        color="gold"
    )
    
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
        # Draw the price below the name
        price_color = "green" if player_money >= actor.price else "red"
        screen.draw.text(
            f"${actor.price}",
            center=(actor.x, actor.y + 85),
            fontsize=18,
            color=price_color
        )
    
    # Draw inventory at the bottom
    draw_inventory()

def draw_inventory():
    # Draw inventory title
    screen.draw.text(
        "Inventory:",
        topleft=(20, HEIGHT - 120),
        fontsize=24,
        color="white"
    )
    
    # Draw inventory items
    x_offset = 20
    y_pos = HEIGHT - 60
    item_spacing = 100
    
    for sword_name, quantity in inventory.items():
        # Find the sword data to get the image
        sword_data = None
        for sword in swords:
            if sword["name"] == sword_name:
                sword_data = sword
                break
        
        if sword_data:
            # Create a small inventory item actor
            inv_actor = Actor(sword_data["image"], pos=(x_offset + 30, y_pos))
            inv_actor.scale = 0.15
            inv_actor.draw()
            
            # Draw quantity below the image
            screen.draw.text(
                f"x{quantity}",
                center=(x_offset + 30, y_pos + 25),
                fontsize=16,
                color="white"
            )
            
            x_offset += item_spacing

def on_mouse_move(pos):
    """Handle mouse hover - scale to 0.5 when mouse approaches"""
    for actor in sword_actors:
        if actor.collidepoint(pos):
            actor.scale = 0.3  # Scale up when mouse hovers
        else:
            actor.scale = 0.2  # Reset to default when mouse moves away

def on_mouse_down(pos):
    """Handle mouse clicks on sword buttons"""
    global player_money
    for actor in sword_actors:
        if actor.collidepoint(pos):
            # Check if player has enough money
            if player_money >= actor.price:
                player_money -= actor.price
                # Add to inventory
                if actor.sword_name in inventory:
                    inventory[actor.sword_name] += 1
                else:
                    inventory[actor.sword_name] = 1
                print(f"Purchased {actor.sword_name} for ${actor.price}! Remaining money: ${player_money}")
            else:
                print(f"Cannot buy {actor.sword_name}. Need ${actor.price}, but only have ${player_money}")

pgzrun.go()