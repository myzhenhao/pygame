import pgzrun
from pgzhelper import *

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Player money
player_money = 1000

# Inventory - tracks purchased items (sword_name -> quantity)
inventory = {}

# Shop state
shop_open = False

# Inventory state
inventory_open = False

# Create player character
player = Actor("player1", pos=(WIDTH // 2, HEIGHT // 2))
player.speed = 5

# Create shop button actor
shop_button = Actor("shop", pos=(WIDTH - 60, 40))
shop_button.scale = 0.2

# Create inventory button actor (below shop button)
inventory_button = Actor("inventory", pos=(WIDTH - 60, 100))
inventory_button.scale = 0.2
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
    
    # Draw player character (always visible)
    player.draw()
    
    # Draw buttons at top right corner
    draw_buttons()
    
    # Only draw shop content if shop is open
    if shop_open:
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
    
    # Draw inventory window if inventory is open
    if inventory_open:
        draw_inventory_window()

def draw_buttons():
    """Draw the shop and inventory buttons at top right corner"""
    shop_button.draw()
    inventory_button.draw()

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

def draw_inventory_window():
    """Draw the inventory window - similar style to shop"""
    # Draw title (similar to shop title)
    screen.draw.text("Inventory", center=(WIDTH // 2, 50), fontsize=48, color="white")
    
    # Draw player money (same as shop)
    screen.draw.text(
        f"Money: ${player_money}",
        topleft=(20, 20),
        fontsize=24,
        color="gold"
    )
    
    # Draw inventory items (similar to shop items)
    if not inventory:
        screen.draw.text(
            "No items yet",
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=32,
            color="gray"
        )
    else:
        # Calculate starting position to center items
        item_count = len(inventory.items())
        total_width = item_count * 200  # Approximate width per item
        start_x = (WIDTH - total_width) // 2 + 100
        
        x_offset = start_x
        y_pos = HEIGHT // 2
        
        for sword_name, quantity in inventory.items():
            # Find the sword data to get the image
            sword_data = None
            for sword in swords:
                if sword["name"] == sword_name:
                    sword_data = sword
                    break
            
            if sword_data:
                # Create inventory item actor (similar scale to shop items)
                inv_actor = Actor(sword_data["image"], pos=(x_offset, y_pos))
                inv_actor.scale = 0.2
                inv_actor.draw()
                
                # Draw item name below the image (similar to shop)
                screen.draw.text(
                    sword_name,
                    center=(x_offset, y_pos + 60),
                    fontsize=20,
                    color="white"
                )
                
                # Draw quantity below the name (similar to price in shop)
                screen.draw.text(
                    f"x{quantity}",
                    center=(x_offset, y_pos + 85),
                    fontsize=18,
                    color="lightgreen"
                )
                
                x_offset += 200

def update():
    """Update game state - handle player movement"""
    # Player movement with WASD keys
    if keyboard.a or keyboard.left:
        player.x -= player.speed
        player.flip_x = True
    if keyboard.d or keyboard.right:
        player.x += player.speed
        player.flip_x = False
    if keyboard.w or keyboard.up:
        player.y -= player.speed
    if keyboard.s or keyboard.down:
        player.y += player.speed
    
    # Keep player within screen bounds
    player.x = max(0, min(WIDTH, player.x))
    player.y = max(0, min(HEIGHT, player.y))

def on_mouse_move(pos):
    """Handle mouse hover - scale to 0.5 when mouse approaches"""
    # Only handle hover if shop is open
    if shop_open:
        for actor in sword_actors:
            if actor.collidepoint(pos):
                actor.scale = 0.3  # Scale up when mouse hovers
            else:
                actor.scale = 0.2  # Reset to default when mouse moves away

def on_mouse_down(pos):
    """Handle mouse clicks on sword buttons and toggle buttons"""
    global shop_open, inventory_open, player_money
    
    # Check if inventory button is clicked
    if inventory_button.collidepoint(pos):
        inventory_open = not inventory_open
        return
    
    # Check if shop button is clicked
    if shop_button.collidepoint(pos):
        shop_open = not shop_open
        return
    
    # Only handle sword clicks if shop is open
    if shop_open:
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