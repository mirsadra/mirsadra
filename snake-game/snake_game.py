import random
import os
import json
from datetime import datetime

def load_game_state():
    """Load the current game state from a file"""
    state_file = 'game_state.json'
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r') as f:
                return json.load(f)
        except:
            pass
    
    # Default initial state
    width, height = 30, 15
    return {
        'snake': [[width // 2, height // 2]],
        'direction': [1, 0],
        'food': [random.randint(1, width-2), random.randint(1, height-2)],
        'score': 0,
        'game_over': False,
        'width': width,
        'height': height
    }

def save_game_state(state):
    """Save the current game state to a file"""
    with open('game_state.json', 'w') as f:
        json.dump(state, f)

def move_snake(state):
    """Move the snake and handle game logic"""
    if state['game_over']:
        return state
    
    snake = state['snake'][:]
    direction = state['direction']
    food = state['food']
    width = state['width']
    height = state['height']
    
    # Calculate new head position
    head = snake[0]
    new_head = [head[0] + direction[0], head[1] + direction[1]]
    
    # Check wall collision
    if (new_head[0] < 0 or new_head[0] >= width or 
        new_head[1] < 0 or new_head[1] >= height):
        state['game_over'] = True
        return state
    
    # Check self collision
    if new_head in snake:
        state['game_over'] = True
        return state
    
    # Add new head
    snake.insert(0, new_head)
    
    # Check if food is eaten
    if new_head == food:
        state['score'] += 1
        # Generate new food position
        while True:
            new_food = [random.randint(0, width-1), random.randint(0, height-1)]
            if new_food not in snake:
                state['food'] = new_food
                break
    else:
        # Remove tail if no food eaten
        snake.pop()
    
    # Randomly change direction occasionally to make it more interesting
    if random.random() < 0.1:  # 10% chance to change direction
        possible_directions = []
        current_dir = direction
        
        # Add all perpendicular directions
        if current_dir[0] == 0:  # Moving vertically
            possible_directions = [[1, 0], [-1, 0]]
        else:  # Moving horizontally
            possible_directions = [[0, 1], [0, -1]]
        
        # Sometimes continue straight
        possible_directions.append(current_dir)
        
        # Choose a random direction, but avoid immediate collision
        for _ in range(10):  # Try up to 10 times
            new_direction = random.choice(possible_directions)
            test_head = [new_head[0] + new_direction[0], new_head[1] + new_direction[1]]
            
            # Check if this direction would cause immediate collision
            if (0 <= test_head[0] < width and 0 <= test_head[1] < height and 
                test_head not in snake):
                state['direction'] = new_direction
                break
    
    state['snake'] = snake
    return state

def reset_game_if_over(state):
    """Reset the game if it's over"""
    if state['game_over']:
        width, height = state['width'], state['height']
        state.update({
            'snake': [[width // 2, height // 2]],
            'direction': [random.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])],
            'food': [random.randint(0, width-1), random.randint(0, height-1)],
            'score': 0,
            'game_over': False
        })
        # Make sure food doesn't spawn on snake
        while state['food'] in state['snake']:
            state['food'] = [random.randint(0, width-1), random.randint(0, height-1)]
    
    return state

def generate_snake_svg():
    # Load current state
    state = load_game_state()
    
    # Move the snake
    state = move_snake(state)
    
    # Reset if game over
    state = reset_game_if_over(state)
    
    # Save updated state
    save_game_state(state)
    
    # Generate SVG
    width = state['width']
    height = state['height']
    cell_size = 10
    snake = state['snake']
    food = state['food']
    score = state['score']
    
    svg_content = f'''<svg width="{width * cell_size}" height="{height * cell_size}" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="#0d1117"/>
    
    <!-- Grid lines for better visibility -->
    <defs>
        <pattern id="grid" width="{cell_size}" height="{cell_size}" patternUnits="userSpaceOnUse">
            <path d="M {cell_size} 0 L 0 0 0 {cell_size}" fill="none" stroke="#1a1a1a" stroke-width="0.5"/>
        </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#grid)"/>
    
    <!-- Food -->
    <circle cx="{food[0] * cell_size + cell_size//2}" cy="{food[1] * cell_size + cell_size//2}" 
            r="{cell_size//2 - 1}" fill="#ff4444" stroke="#ff6666" stroke-width="1"/>
    
    <!-- Snake -->'''
    
    for i, segment in enumerate(snake):
        if i == 0:  # Head
            color = "#00ff00"
            svg_content += f'''
    <rect x="{segment[0] * cell_size + 1}" y="{segment[1] * cell_size + 1}" 
          width="{cell_size - 2}" height="{cell_size - 2}" fill="{color}" rx="2"/>
    <circle cx="{segment[0] * cell_size + cell_size//2}" cy="{segment[1] * cell_size + cell_size//2}" 
            r="1" fill="#ffffff"/>'''
        else:  # Body
            color = "#00cc00" if i % 2 == 1 else "#00aa00"
            svg_content += f'''
    <rect x="{segment[0] * cell_size + 1}" y="{segment[1] * cell_size + 1}" 
          width="{cell_size - 2}" height="{cell_size - 2}" fill="{color}" rx="1"/>'''
    
    svg_content += f'''
    
    <!-- UI -->
    <rect x="0" y="{height * cell_size - 20}" width="{width * cell_size}" height="20" fill="#000000" opacity="0.8"/>
    <text x="5" y="{height * cell_size - 7}" fill="#00ff00" font-family="monospace" font-size="12">
        Score: {score} | Length: {len(snake)} | {'GAME OVER' if state.get('game_over') else 'Playing...'}
    </text>
    <text x="{width * cell_size - 120}" y="{height * cell_size - 7}" fill="#888" font-family="monospace" font-size="10">
        {datetime.now().strftime('%H:%M:%S')}
    </text>
</svg>'''
    
    return svg_content

if __name__ == "__main__":
    svg_content = generate_snake_svg()
    print(svg_content)
