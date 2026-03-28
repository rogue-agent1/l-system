#!/usr/bin/env python3
"""L-System fractal string generator with turtle-graphics ASCII renderer."""
import sys, math

PRESETS = {
    'sierpinski': {'axiom':'F-G-G', 'rules':{'F':'F-G+F+G-F','G':'GG'}, 'angle':120, 'iters':5},
    'dragon': {'axiom':'FX', 'rules':{'X':'X+YF+','Y':'-FX-Y'}, 'angle':90, 'iters':10},
    'koch': {'axiom':'F', 'rules':{'F':'F+F-F-F+F'}, 'angle':90, 'iters':4},
    'plant': {'axiom':'X', 'rules':{'X':'F+[[X]-X]-F[-FX]+X','F':'FF'}, 'angle':25, 'iters':5},
    'hilbert': {'axiom':'A', 'rules':{'A':'-BF+AFA+FB-','B':'+AF-BFB-FA+'}, 'angle':90, 'iters':5},
}

def generate(axiom, rules, iterations):
    s = axiom
    for _ in range(iterations):
        s = ''.join(rules.get(c, c) for c in s)
    return s

def render(string, angle_deg, size=1):
    x, y, a = 0.0, 0.0, 0.0
    angle = math.radians(angle_deg)
    stack = []
    points = [(x, y)]
    for c in string:
        if c in 'FG':
            x += math.cos(a) * size
            y += math.sin(a) * size
            points.append((x, y))
        elif c == '+': a += angle
        elif c == '-': a -= angle
        elif c == '[': stack.append((x, y, a))
        elif c == ']': x, y, a = stack.pop(); points.append((None, None)); points.append((x, y))
    return points

def ascii_render(points, w=80, h=40):
    real = [(x, y) for x, y in points if x is not None]
    if not real: return
    xs, ys = [p[0] for p in real], [p[1] for p in real]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    rx, ry = maxx-minx or 1, maxy-miny or 1
    grid = [[' ']*w for _ in range(h)]
    for x, y in real:
        col = int((x - minx) / rx * (w-1))
        row = int((y - miny) / ry * (h-1))
        grid[row][col] = '█'
    for row in reversed(grid): print(''.join(row))

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('preset', nargs='?', choices=list(PRESETS.keys()), default='koch')
    p.add_argument('-n', '--iterations', type=int)
    p.add_argument('-W', '--width', type=int, default=80)
    p.add_argument('-H', '--height', type=int, default=40)
    p.add_argument('--string-only', action='store_true')
    args = p.parse_args()
    cfg = PRESETS[args.preset]
    iters = args.iterations or cfg['iters']
    s = generate(cfg['axiom'], cfg['rules'], iters)
    if args.string_only:
        print(s[:500]); print(f"\n({len(s)} chars)")
    else:
        pts = render(s, cfg['angle'])
        ascii_render(pts, args.width, args.height)
        print(f"\n{args.preset} (n={iters}, {len(s)} instructions)")
