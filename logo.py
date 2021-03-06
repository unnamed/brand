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
# Small script to generate our logo in Scalable Vector Graphics format
# (SVG) allowing to create variations with different fill, padding,
# background color and stroke width, this allows designers to use a
# single file for every single variation, which can be generated using
# a command. Created by yusshu (Andre Roldan)
#

def parse_args():
    """
    Registers and parses arguments from the command line
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--variant', '-v', help='Set logo variant name', type=str, default='default')
    parser.add_argument('--stroke', '-s', help='Set the stroke width', type=int, default=6)
    parser.add_argument('--fill', '-f', help='Set the logo fill color', type=str, default='#ff8df8')
    parser.add_argument('--padding', '-p', help='Set the logo padding', type=int, default=0)
    parser.add_argument('--background', '-b', help='Set the logo background color', type=str)
    parser.add_argument('--background_radius', '-r', help='Set the background radius', type=int, default=0)
    return parser.parse_args()

# Parse arguments
args = parse_args()

variant = args.variant
# '64' is the base size for the logo,
# we add the padding to it
off = args.padding or 0
size = 64 + off + off


# TODO: use better names and make it more legible
# Sizes
s = args.stroke
ss = s / 2

# '??' and '??' connection
# arc sizes (width, radius)
arc_width = 32 + ss
arc_r = arc_width / 2
sub_arc_width = 32 - (s * 1.5)
sub_arc_r = sub_arc_width / 2

# '??' tail (arc and circle)
tail_bottom_y = 62
cx = 51.5
cy = tail_bottom_y - ss
tail_y = 49.5
tail_r = tail_bottom_y - tail_y
sub_tail_r = tail_r - s

# Create background
background_color = args.background
background = '' if background_color is None else f'<rect width="{size}" height="{size}" x="0" y="0" fill="{background_color}" ry="{args.background_radius}" />'

# Create SVG
svg = \
    f'<svg viewBox="0 0 {size} {size}" version="1.1" xmlns="http://www.w3.org/2000/svg">\n' \
    f'{background}' \
    f'  <g fill="{args.fill}">\n' \
    f'    <rect width="{s}" height="58" x="{off}" y="{off + 2}" ry="{ss}"/>\n' \
    f'    <rect width="{s}" height="42" x="{off + 32 - ss}" y="{off + 2}" ry="{ss}"/>\n' \
    f'    <rect width="{s}" height="{30 + s}" x="{off + 64 - s}" y="{off + 19.5 - ss}" ry="{ss}" />\n' \
    f'    <path d="M {off + 64} {off + 19.5} a {arc_r} {arc_r} 0 0 0 {-arc_width} 0 h {s} a {sub_arc_r} {sub_arc_r} 0 0 1 {sub_arc_width} 0 z"/>\n' \
    f'    <path d="M {off} {off + 27.5} a {arc_r} {arc_r} 0 0 0 {arc_width} 0 h {-s} a {sub_arc_r} {sub_arc_r} 0 0 1 {-sub_arc_width} 0 z"/>\n' \
    f'    <path d="M {off + 64 - s} {off + tail_y} a {sub_tail_r} {sub_tail_r} 0 0 1 {-sub_tail_r} {sub_tail_r} v {s} a {tail_r} {tail_r} 0 0 0 {tail_r} {-tail_r} z"/>\n' \
    f'    <circle cx="{off + cx}" cy="{off + cy}" r="{ss}" />\n' \
    f'  </g>\n' \
    f'</svg>'

# Write SVG file
with open(f'svg/logo.svg', 'w') as f:
    f.write(svg)

# Write PNG files
with open('src/dimensions_square_logo.txt') as f:
    for line in f.readlines():
        if line.startswith('#'):
            continue
        size = int(line.strip())
        svg2png(
            bytestring=svg,
            write_to=f'png/logo-{variant}-{size}x{size}.png',
            parent_width=size,
            parent_height=size
        )