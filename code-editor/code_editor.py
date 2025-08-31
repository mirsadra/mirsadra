import random
import os
import json
from datetime import datetime

def load_editor_state():
    """Load the current editor state"""
    state_file = 'editor_state.json'
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)
                return state
        except:
            pass
    
    return {
        'current_snippet': 0,
        'current_line': 0,
        'current_char': 0,
        'typing_complete': False,
        'step': 0
    }

def save_editor_state(state):
    """Save the current editor state"""
    with open('editor_state.json', 'w') as f:
        json.dump(state, f)

def get_code_snippets():
    """Return different code snippets to cycle through"""
    return [
        {
            'language': 'Swift',
            'filename': 'ViewController.swift',
            'theme': '#fa7343',
            'code': [
                'import UIKit',
                'import SwiftUI',
                '',
                'class ViewController: UIViewController {',
                '    override func viewDidLoad() {',
                '        super.viewDidLoad()',
                '        setupUI()',
                '    }',
                '    ',
                '    private func setupUI() {',
                '        view.backgroundColor = .systemBackground',
                '        // Add your UI elements here',
                '    }',
                '}'
            ]
        },
        {
            'language': 'TypeScript',
            'filename': 'components/Hero.tsx',
            'theme': '#3178c6',
            'code': [
                'import React from "react";',
                'import { NextPage } from "next";',
                '',
                'interface HeroProps {',
                '  title: string;',
                '  subtitle?: string;',
                '}',
                '',
                'const Hero: React.FC<HeroProps> = ({ title, subtitle }) => {',
                '  return (',
                '    <div className="hero-container">',
                '      <h1>{title}</h1>',
                '      {subtitle && <p>{subtitle}</p>}',
                '    </div>',
                '  );',
                '};',
                '',
                'export default Hero;'
            ]
        },
        {
            'language': 'Python',
            'filename': 'ai_model.py',
            'theme': '#3776ab',
            'code': [
                'import torch',
                'import torch.nn as nn',
                'from transformers import AutoModel',
                '',
                'class CustomLLM(nn.Module):',
                '    def __init__(self, config):',
                '        super().__init__()',
                '        self.transformer = AutoModel.from_pretrained(',
                '            config.model_name',
                '        )',
                '        self.head = nn.Linear(',
                '            config.hidden_size, config.vocab_size',
                '        )',
                '    ',
                '    def forward(self, input_ids):',
                '        outputs = self.transformer(input_ids)',
                '        return self.head(outputs.last_hidden_state)'
            ]
        }
    ]

def escape_html(text):
    """Escape HTML characters"""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#x27;')

def get_syntax_color(token, language):
    """Get color for syntax highlighting"""
    if language == 'Swift':
        if token in ['import', 'class', 'func', 'var', 'let', 'override', 'private', 'super']:
            return '#ff7ab2'  # Keywords
        elif token in ['UIViewController', 'UIKit', 'SwiftUI', 'UIView']:
            return '#6699cc'  # Types
        elif token.startswith('"') and token.endswith('"'):
            return '#ffa500'  # Strings
    elif language == 'TypeScript':
        if token in ['import', 'export', 'interface', 'const', 'return', 'from', 'default']:
            return '#569cd6'  # Keywords
        elif token in ['React', 'NextPage', 'string', 'FC']:
            return '#4ec9b0'  # Types
        elif token.startswith('"') and token.endswith('"'):
            return '#ce9178'  # Strings
    elif language == 'Python':
        if token in ['import', 'from', 'class', 'def', 'return', 'super']:
            return '#569cd6'  # Keywords
        elif token in ['torch', 'nn', 'AutoModel', 'Module']:
            return '#4ec9b0'  # Types
        elif token.startswith("'") and token.endswith("'"):
            return '#ce9178'  # Strings
    
    return '#d4d4d4'  # Default text color

def highlight_line(line, language):
    """Apply syntax highlighting to a line of code"""
    if not line.strip():
        return ''
    
    # Simple tokenization - split by spaces and common delimiters
    tokens = []
    current_token = ''
    in_string = False
    string_char = None
    
    for char in line:
        if char in ['"', "'"] and not in_string:
            if current_token:
                tokens.append(current_token)
                current_token = ''
            in_string = True
            string_char = char
            current_token = char
        elif char == string_char and in_string:
            current_token += char
            tokens.append(current_token)
            current_token = ''
            in_string = False
            string_char = None
        elif in_string:
            current_token += char
        elif char in [' ', '(', ')', '{', '}', '[', ']', ';', ':', ',', '.', '<', '>']:
            if current_token:
                tokens.append(current_token)
                current_token = ''
            if char != ' ':
                tokens.append(char)
            if char == ' ':
                tokens.append(' ')
        else:
            current_token += char
    
    if current_token:
        tokens.append(current_token)
    
    # Apply syntax highlighting
    highlighted = ''
    for token in tokens:
        color = get_syntax_color(token, language)
        if token == ' ':
            highlighted += ' '
        else:
            highlighted += f'<tspan fill="{color}">{escape_html(token)}</tspan>'
    
    return highlighted

def generate_code_editor_svg():
    # Load current state
    state = load_editor_state()
    snippets = get_code_snippets()
    
    # Increment step
    state['step'] += 1
    
    # Get current snippet
    current_snippet = snippets[state['current_snippet']]
    
    # Typing animation logic
    if not state['typing_complete']:
        # Advance typing
        if state['current_char'] < len(current_snippet['code'][state['current_line']]):
            state['current_char'] += random.randint(1, 3)  # Type 1-3 characters
        else:
            # Move to next line
            state['current_line'] += 1
            state['current_char'] = 0
            
        # Check if we've typed the whole snippet
        if state['current_line'] >= len(current_snippet['code']):
            state['typing_complete'] = True
    
    # If typing is complete, wait a bit then move to next snippet
    if state['typing_complete']:
        if state['step'] % 8 == 0:  # Wait 8 steps before next snippet
            state['current_snippet'] = (state['current_snippet'] + 1) % len(snippets)
            state['current_line'] = 0
            state['current_char'] = 0
            state['typing_complete'] = False
    
    # Save state
    save_editor_state(state)
    
    # Generate SVG
    width, height = 600, 400
    line_height = 16
    
    # Calculate visible lines
    lines_to_show = min(state['current_line'] + 1, len(current_snippet['code']))
    
    svg_content = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            .editor-bg {{ fill: #1e1e1e; }}
            .title-bar {{ fill: #2d2d30; }}
            .line-numbers {{ fill: #858585; font-family: 'Courier New', monospace; font-size: 12px; }}
            .code-text {{ fill: #d4d4d4; font-family: 'Courier New', monospace; font-size: 12px; }}
            .cursor {{ fill: #ffffff; }}
            .tab {{ fill: #2d2d30; stroke: #3e3e42; stroke-width: 1; }}
            .tab-active {{ fill: #1e1e1e; stroke: #007acc; stroke-width: 1; }}
        </style>
    </defs>
    
    <!-- Editor background -->
    <rect width="100%" height="100%" class="editor-bg"/>
    
    <!-- Title bar -->
    <rect x="0" y="0" width="100%" height="30" class="title-bar"/>
    <circle cx="15" cy="15" r="6" fill="#ff5f56"/>
    <circle cx="35" cy="15" r="6" fill="#ffbd2e"/>
    <circle cx="55" cy="15" r="6" fill="#27ca3f"/>
    
    <!-- Tabs -->
    <rect x="80" y="5" width="120" height="20" class="tab-active"/>
    <text x="85" y="18" fill="#ffffff" font-family="system-ui" font-size="11">{current_snippet['filename']}</text>
    <rect x="200" y="5" width="80" height="20" class="tab"/>
    <text x="205" y="18" fill="#cccccc" font-family="system-ui" font-size="11">README.md</text>
    
    <!-- Language indicator -->
    <rect x="{width-80}" y="5" width="75" height="20" fill="{current_snippet['theme']}" opacity="0.8"/>
    <text x="{width-75}" y="18" fill="#ffffff" font-family="system-ui" font-size="10" font-weight="bold">{current_snippet['language']}</text>
    
    <!-- Line numbers background -->
    <rect x="0" y="30" width="40" height="{height-30}" fill="#262626"/>
    
    <!-- Code content -->'''
    
    # Render visible lines
    for i in range(lines_to_show):
        line_y = 45 + i * line_height
        line_content = current_snippet['code'][i]
        
        # Line number
        svg_content += f'\n    <text x="35" y="{line_y}" class="line-numbers" text-anchor="end">{i + 1}</text>'
        
        # Code line
        if i < state['current_line']:
            # Fully typed line
            highlighted_line = highlight_line(line_content, current_snippet['language'])
            svg_content += f'\n    <text x="50" y="{line_y}" class="code-text">{highlighted_line}</text>'
        elif i == state['current_line']:
            # Currently typing line
            visible_text = line_content[:state['current_char']]
            if visible_text:
                highlighted_line = highlight_line(visible_text, current_snippet['language'])
                svg_content += f'\n    <text x="50" y="{line_y}" class="code-text">{highlighted_line}</text>'
            
            # Cursor
            cursor_x = 50 + len(visible_text) * 7  # Approximate character width
            if state['step'] % 2 == 0:  # Blinking cursor
                svg_content += f'\n    <rect x="{cursor_x}" y="{line_y - 12}" width="2" height="14" class="cursor"/>'
    
    # Status bar
    svg_content += f'''
    
    <!-- Status bar -->
    <rect x="0" y="{height-25}" width="100%" height="25" fill="#007acc"/>
    <text x="10" y="{height-8}" fill="#ffffff" font-family="system-ui" font-size="11">
        {current_snippet['language']} | Line {state['current_line'] + 1} | Col {state['current_char'] + 1}
    </text>
    <text x="{width-150}" y="{height-8}" fill="#ffffff" font-family="system-ui" font-size="10" opacity="0.8">
        Last updated: {datetime.now().strftime('%H:%M:%S')}
    </text>
    
    <!-- Progress indicator -->
    <rect x="{width-20}" y="{height-20}" width="15" height="15" fill="#ffffff" opacity="0.2"/>
    <rect x="{width-18}" y="{height-18}" width="11" height="11" fill="#ffffff" opacity="0.5"/>
    <circle cx="{width-12.5}" cy="{height-12.5}" r="3" fill="#ffffff">
        <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite"/>
    </circle>
</svg>'''
    
    return svg_content

if __name__ == "__main__":
    svg_content = generate_code_editor_svg()
    print(svg_content)
