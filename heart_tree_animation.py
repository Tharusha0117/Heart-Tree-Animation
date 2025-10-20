import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
GROUND_Y = 500  
FPS = 60
MAX_BRANCH_LEVEL = 4  

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Heart Tree Animation")
clock = pygame.time.Clock()

CURSIVE_FONT_FILENAME = "DancingScript-Regular.ttf"

try:
    FONT = pygame.font.Font(CURSIVE_FONT_FILENAME, 28) 
    print(f"Successfully loaded font: {CURSIVE_FONT_FILENAME}")
except (pygame.error, FileNotFoundError):
    print(f"--- FONT FILE NOT FOUND ---")
    print(f"Error: Could not find the font '{CURSIVE_FONT_FILENAME}'.")
    print(f"Please download it from Google Fonts and place it in the script's folder.")
    print("Using default font instead.")
    print(f"---------------------------")
    FONT = pygame.font.Font(None, 30)

TEXT_COLOR = (0, 0, 0) 
ROMANTIC_MESSAGE = (
    "Thanks to you, I smile a little more, laugh a little harder, "
    "and cry a little less. I am so lucky to have you in my life. "
    "I don’t know where I would be without your love."
)
CHAR_APPEAR_DELAY = 3 

def draw_heart(surface, color, x, y, size):
    """
    Draws a heart shape.
    (x, y) is the coordinate of the BOTTOM tip.
    """
    height = size * 0.8
    width = size

    p1 = (x - width / 2, y - height * 0.6)
    p2 = (x + width / 2, y - height * 0.6)
    p3 = (x, y)

    c1_center = (int(x - width / 4), int(y - height * 0.75))
    c2_center = (int(x + width / 4), int(y - height * 0.75))
    radius = int(width / 4)

    pygame.draw.polygon(surface, color, [p1, p2, p3])
    pygame.draw.circle(surface, color, c1_center, radius)
    pygame.draw.circle(surface, color, c2_center, radius)

def reset_animation():
    """Resets all variables to start the animation over."""
    global current_state, heart_y, heart_size, heart_speed, is_absorbing
    global stem_height, stem_max_height, stem_growth_speed
    global branches, growing_branches, branch_index, branch_definitions
    global leaves, leaf_positions, leaf_index, leaf_timer, leaf_fall_timer, leaf_to_fall_index
    global text_char_index, text_display_timer, rendered_text_surface

    current_state = "HEART_FALLING"
    heart_y = -50
    heart_size = 60
    heart_speed = 4
    is_absorbing = False

    stem_height = 0
    stem_max_height = 280
    stem_growth_speed = 1

    branches = [] 
    growing_branches = [] 
    branch_index = 0

    branch_definitions = [
        (0.3, 150, 90, 1),  
        (0.5, 30, 90, 1),   
        (0.7, 130, 100, 1), 
        (0.8, 50, 100, 1),  
        (0.6, 160, 80, 1),  
        (0.75, 170, 70, 1), 
        (0.9, 140, 60, 1),  
        (0.4, 110, 70, 1),  
    ]

    leaves = []
    leaf_positions = [] 
    leaf_index = 0
    leaf_timer = 0
    leaf_fall_timer = 0
    leaf_to_fall_index = 0

    text_char_index = 0
    text_display_timer = 0
    rendered_text_surface = None 

reset_animation()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(SKY_BLUE)
    pygame.draw.rect(screen, GRASS_GREEN, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))


    if current_state == "HEART_FALLING":
        if not is_absorbing:
            heart_y += heart_speed
            if heart_y >= GROUND_Y - (heart_size * 0.2):
                heart_y = GROUND_Y - (heart_size * 0.2)
                is_absorbing = True
        else:
            heart_size -= 0.5
            if heart_size <= 0:
                current_state = "STEM_GROWING"
        
        if heart_size > 0:
            draw_heart(screen, RED, WIDTH // 2, heart_y, heart_size)

    elif current_state == "STEM_GROWING":
        if stem_height < stem_max_height:
            stem_height += stem_growth_speed
        else:
            current_state = "BRANCHES_GROWING"
        
        pygame.draw.rect(screen, BROWN, (WIDTH // 2 - 5, GROUND_Y - stem_height, 10, stem_height))

    elif current_state == "BRANCHES_GROWING":

        pygame.draw.rect(screen, BROWN, (WIDTH // 2 - 5, GROUND_Y - stem_height, 10, stem_height))

        if branch_index < len(branch_definitions):
            h_frac, angle_deg, max_len, level = branch_definitions[branch_index]
            start_x = WIDTH // 2
            start_y = GROUND_Y - (stem_max_height * h_frac)
            angle_rad = math.radians(angle_deg)
            
            growing_branches.append({
                'start': (start_x, start_y),
                'angle': angle_rad,
                'max_len': max_len,
                'current_len': 0,
                'speed': 2,
                'level': level
            })
            branch_index += 1

        for i in range(len(growing_branches) - 1, -1, -1):
            branch = growing_branches[i]
            branch['current_len'] += branch['speed']
            
            end_x = branch['start'][0] + branch['current_len'] * math.cos(branch['angle'])
            end_y = branch['start'][1] - branch['current_len'] * math.sin(branch['angle'])
            
            pygame.draw.line(screen, BROWN, branch['start'], (end_x, end_y), max(1, 8 - (branch['level'] * 2)))

            if branch['current_len'] >= branch['max_len']:
                
                branches.append({'start': branch['start'], 'end': (end_x, end_y), 'level': branch['level']})
                
                current_level = branch['level']

                start_x, start_y = branch['start']
                num_leaves_this_segment = random.randint(3, 7) 
                for k in range(num_leaves_this_segment):
                    fraction = (k / (num_leaves_this_segment - 1)) if num_leaves_this_segment > 1 else 0.5
                    leaf_x = start_x + (end_x - start_x) * fraction + random.randint(-5, 5) 
                    leaf_y = start_y + (end_y - start_y) * fraction + random.randint(-5, 5)
                    leaf_positions.append((leaf_x, leaf_y))

                if current_level < MAX_BRANCH_LEVEL:
                    new_len = branch['max_len'] * random.uniform(0.6, 0.8)  
                    new_level = current_level + 1
       
                    growing_branches.append({
                        'start': (end_x, end_y),
                        'angle': branch['angle'] + math.radians(random.randint(15, 45)), 
                        'max_len': new_len,
                        'current_len': 0, 'speed': 2, 'level': new_level
                    })
                    
  
                    growing_branches.append({
                        'start': (end_x, end_y),
                        'angle': branch['angle'] - math.radians(random.randint(15, 45)), 
                        'max_len': new_len,
                        'current_len': 0, 'speed': 2, 'level': new_level
                    })

                growing_branches.pop(i)

        for branch in branches:
            pygame.draw.line(screen, BROWN, branch['start'], branch['end'], max(1, 8 - (branch['level'] * 2)))

        if not growing_branches and branch_index == len(branch_definitions):
            current_state = "LEAVES_APPEARING"

    elif current_state == "LEAVES_APPEARING":

        pygame.draw.rect(screen, BROWN, (WIDTH // 2 - 5, GROUND_Y - stem_height, 10, stem_height))
        for branch in branches:
            pygame.draw.line(screen, BROWN, branch['start'], branch['end'], max(1, 8 - (branch['level'] * 2)))
            

        for leaf in leaves:
            draw_heart(screen, leaf['color'], leaf['x'], leaf['y'], leaf['size'])
            

        leaf_timer += 1
        if leaf_timer >= 1 and leaf_index < len(leaf_positions): 
            leaf_timer = 0
            pos = leaf_positions[leaf_index]
            color = random.choice([(255, 105, 180), (255, 192, 203), (255, 0, 255), (255, 20, 147), (221, 160, 221)])
            
            leaves.append({
                'x': pos[0], 'y': pos[1], 
                'size': random.randint(15, 25), 
                'color': color, 
                'state': 'on_tree', 'vy': 0, 'vx': 0
            })
            leaf_index += 1

        if leaf_index == len(leaf_positions):
            current_state = "LEAVES_FALLING"

    elif current_state == "LEAVES_FALLING":

        pygame.draw.rect(screen, BROWN, (WIDTH // 2 - 5, GROUND_Y - stem_height, 10, stem_height))
        for branch in branches:
            pygame.draw.line(screen, BROWN, branch['start'], branch['end'], max(1, 8 - (branch['level'] * 2)))

        leaf_fall_timer += 1
        if leaf_fall_timer >= 5 and leaf_to_fall_index < len(leaves):
            leaf_fall_timer = 0
            leaves[leaf_to_fall_index]['state'] = 'falling'
            leaves[leaf_to_fall_index]['vy'] = random.uniform(1, 3)
            leaves[leaf_to_fall_index]['vx'] = random.uniform(-1, 1)
            leaf_to_fall_index += 1

        all_on_ground = True
        for leaf in leaves:
            if leaf['state'] == 'on_tree':
                all_on_ground = False
                draw_heart(screen, leaf['color'], leaf['x'], leaf['y'], leaf['size'])
            
            elif leaf['state'] == 'falling':
                all_on_ground = False
                leaf['y'] += leaf['vy'] 
                leaf['x'] += leaf['vx']
                draw_heart(screen, leaf['color'], leaf['x'], leaf['y'], leaf['size'])
                
                if leaf['y'] >= GROUND_Y:
                    leaf['y'] = GROUND_Y
                    leaf['state'] = 'on_ground'
            
            elif leaf['state'] == 'on_ground':
                draw_heart(screen, leaf['color'], leaf['x'], leaf['y'], leaf['size'])

        text_display_timer += 1
        if text_display_timer >= CHAR_APPEAR_DELAY and text_char_index < len(ROMANTIC_MESSAGE):
            text_char_index += 1
            text_display_timer = 0

        current_text = ROMANTIC_MESSAGE[:text_char_index]
        if current_text:

            words = current_text.split(' ')
            line = ""
            lines = []
            for word in words:
                if FONT.size(line + word)[0] < WIDTH - 40: 
                    line += word + " "
                else:
                    lines.append(line)
                    line = word + " "
            lines.append(line) 

            text_y_offset = 50 
            for i, text_line in enumerate(lines):
                text_surface = FONT.render(text_line, True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, text_y_offset + i * FONT.get_linesize()))
                screen.blit(text_surface, text_rect)

        
        if all_on_ground and leaf_to_fall_index == len(leaves):
            current_state = "DONE"
            

    elif current_state == "DONE":

        pygame.draw.rect(screen, BROWN, (WIDTH // 2 - 5, GROUND_Y - stem_height, 10, stem_height))
        for branch in branches:
            pygame.draw.line(screen, BROWN, branch['start'], branch['end'], max(1, 8 - (branch['level'] * 2)))
        for leaf in leaves:
            draw_heart(screen, leaf['color'], leaf['x'], leaf['y'], leaf['size'])
        

        words = ROMANTIC_MESSAGE.split(' ')
        line = ""
        lines = []
        for word in words:
            if FONT.size(line + word)[0] < WIDTH - 40:
                line += word + " "
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)

        text_y_offset = 50
        for i, text_line in enumerate(lines):
            text_surface = FONT.render(text_line, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, text_y_offset + i * FONT.get_linesize()))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        pygame.time.wait(3000) 
        reset_animation()


    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
