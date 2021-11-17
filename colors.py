#!/usr/bin/env python3
#
#  MIT License
#
#  Copyright (c) 2021 Unnamed Team
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
from cairosvg import svg2png

#
# Small script to generate an image of our branding colors in a single PNG
# file
#
colors = dict()

# Read colors from src/colors.txt
with open('src/colors.txt') as f:
    for line in f.readlines():
        line = line.strip()
        if len(line) == 0 or line.startswith('#'):
            continue
        args = line.split(':')
        name = args[0].strip()
        color = args[1].strip()
        fore = args[2].strip()
        colors[name] = (color, fore)

count = len(colors)

columns = int(count / 2)
rows = count - columns

item_width = 16
item_height = 16
font_size = 2

canvas_width = item_width * columns
canvas_height = item_height * rows

x = 0
y = 0
in_row = 0

svg = f'<svg viewBox="0 0 {canvas_width} {canvas_height}" version="1.1" xmlns="http://www.w3.org/2000/svg">'
labels = f'<g font-size="{font_size}" font-family="Rubik">'
for name, (color, fore) in colors.items():

    # Draw background rectangle
    svg += f'<rect fill="{color}" x="{x}" y="{y}" width="{item_width}" height="{item_height}" />'

    # Draw label
    label_x = x + 1
    labels += f'<text fill="{fore}" x="{label_x}" y="{y + font_size + 1}">{name}</text>'
    labels += f'<text font-size="1.5" fill="{fore}" x="{label_x}" y="{y + item_height - 1}">{color}</text>'

    x += item_width

    # update variables because we added a new
    # item to the canvas
    in_row += 1
    if in_row >= columns:
        in_row = 0
        x = 0
        y += item_height

labels += '</g>'
svg += labels
svg += '</svg>'

# Write SVG as PNG
svg2png(bytestring=svg, write_to=f'png/colors.png', parent_width=512, parent_height=512)
