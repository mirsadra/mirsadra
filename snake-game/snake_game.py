import numpy as np
import svgwrite
import os
from datetime import datetime

def generate_snake_svg():
  
    dwg = svgwrite.Drawing('snake-game.svg', size=("400", "200"), profile='full')

    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill='#0d1117'))
    
    snake_color = "#00ff00"
    dwg.add(dwg.rect(insert=(50, 50), size=(10, 10), fill=snake_color))
    dwg.add(dwg.rect(insert=(60, 50), size=(10, 10), fill=snake_color))
    dwg.add(dwg.rect(insert=(70, 50), size=(10, 10), fill=snake_color))
    
    dwg.add(dwg.circle(center=(120, 80), r=5, fill='#ff0000'))
    
    dwg.add(dwg.text("Score: 3", insert=(10, 190), fill='#ffffff', font_size="14px"))
    
    dwg.add(dwg.text(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                     insert=(250, 190), fill='#888888', font_size="10px"))
    
    dwg.save()
    
    with open('snake-game.svg', 'r') as f:
        content = f.read()
    
    if os.path.exists('snake-game.svg'):
        os.remove('snake-game.svg')
    
    return content

if __name__ == "__main__":
    svg_content = generate_snake_svg()
    print(svg_content)
