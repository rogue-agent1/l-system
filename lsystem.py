#!/usr/bin/env python3
"""lsystem - L-system generator with ASCII turtle rendering."""
import sys, math
def rewrite(axiom, rules, iterations):
    s = axiom
    for _ in range(iterations):
        s = "".join(rules.get(c, c) for c in s)
    return s
def render(instructions, angle_deg=90, step=1):
    x, y, a = 0.0, 0.0, 90.0; stack = []
    points = [(x, y)]; min_x = max_x = min_y = max_y = 0
    for c in instructions:
        if c in "FG":
            x += step * math.cos(math.radians(a))
            y += step * math.sin(math.radians(a))
            points.append((x, y))
            min_x, max_x = min(min_x, x), max(max_x, x)
            min_y, max_y = min(min_y, y), max(max_y, y)
        elif c == "+": a += angle_deg
        elif c == "-": a -= angle_deg
        elif c == "[": stack.append((x, y, a))
        elif c == "]": x, y, a = stack.pop()
    # ASCII render
    w, h = 60, 30
    grid = [[" "]*w for _ in range(h)]
    for px, py in points:
        col = int((px - min_x) / max(max_x - min_x, 1) * (w-1)) if max_x != min_x else w//2
        row = int((py - min_y) / max(max_y - min_y, 1) * (h-1)) if max_y != min_y else h//2
        row = h - 1 - row
        if 0 <= row < h and 0 <= col < w: grid[row][col] = "*"
    for row in grid: print("".join(row))
PRESETS = {
    "koch": ("F", {"F": "F+F-F-F+F"}, 3, 90),
    "sierpinski": ("F-G-G", {"F": "F-G+F+G-F", "G": "GG"}, 4, 120),
    "dragon": ("FX", {"X": "X+YF+", "Y": "-FX-Y"}, 8, 90),
    "plant": ("X", {"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"}, 4, 25),
}
if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "koch"
    if name in PRESETS:
        axiom, rules, iters, angle = PRESETS[name]
        s = rewrite(axiom, rules, iters)
        print(f"{name}: {len(s)} instructions"); render(s, angle)
    else: print(f"Presets: {', '.join(PRESETS)}")
