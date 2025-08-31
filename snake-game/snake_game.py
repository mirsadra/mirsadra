import random
import os
from datetime import datetime

def generate_snake_svg():
    width, height = 30, 15
    cell_size = 10
    
    snake = [[width // 2, height // 2]]
    direction = [1, 0]
    food = [random.randint(1, width-2), random.randint(1, height-2)]
    score = 0
    
    svg_content = f'''<svg width="{width * cell_size}" height="{height * cell_size}" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="#0d1117"/>
    <text x="5" y="{height * cell_size - 5}" fill="white" font-size="10">Score: {score}</text>
    <text x="{width * cell_size - 100}" y="{height * cell_size - 5}" fill="#888" font-size="8">Updated: {datetime.now().strftime('%H:%M')}</text>
'''
    
    svg_content += f'<circle cx="{food[0] * cell_size + cell_size//2}" cy="{food[1] * cell_size + cell_size//2}" r="{cell_size//2 - 1}" fill="#ff0000"/>\n'
    
    for i, segment in enumerate(snake):
        color = "#00ff00" if i == 0 else "#00cc00"  # Head is brighter green
        svg_content += f'<rect x="{segment[0] * cell_size}" y="{segment[1] * cell_size}" width="{cell_size}" height="{cell_size}" fill="{color}"/>\n'
    
    svg_content += '</svg>'
    
    return svg_content

if __name__ == "__main__":
    svg_content = generate_snake_svg()
    print(svg_content)
