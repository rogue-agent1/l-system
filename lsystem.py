import argparse, math

PRESETS = {
    "koch": {"axiom": "F", "rules": {"F": "F+F-F-F+F"}, "angle": 90, "iters": 4},
    "sierpinski": {"axiom": "F-G-G", "rules": {"F": "F-G+F+G-F", "G": "GG"}, "angle": 120, "iters": 5},
    "dragon": {"axiom": "FX", "rules": {"X": "X+YF+", "Y": "-FX-Y"}, "angle": 90, "iters": 10},
    "plant": {"axiom": "X", "rules": {"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"}, "angle": 25, "iters": 5},
}

def rewrite(axiom, rules, iterations):
    s = axiom
    for _ in range(iterations):
        s = "".join(rules.get(c, c) for c in s)
    return s

def to_ascii(string, angle_deg):
    x, y, a = 0.0, 0.0, 90.0
    stack = []
    points = [(x, y)]
    for c in string:
        if c in "FG":
            x += math.cos(math.radians(a))
            y += math.sin(math.radians(a))
            points.append((x, y))
        elif c == "+": a += angle_deg
        elif c == "-": a -= angle_deg
        elif c == "[": stack.append((x, y, a))
        elif c == "]": x, y, a = stack.pop()
    return len(string), len(points)

def main():
    p = argparse.ArgumentParser(description="L-System")
    p.add_argument("preset", nargs="?", choices=PRESETS.keys())
    p.add_argument("--axiom")
    p.add_argument("--rules", help="A:B,C:D format")
    p.add_argument("-n", "--iterations", type=int, default=4)
    p.add_argument("-a", "--angle", type=float, default=90)
    p.add_argument("--list", action="store_true")
    args = p.parse_args()
    if args.list:
        for k, v in PRESETS.items(): print(f"  {k}: axiom={v['axiom']} angle={v['angle']}")
        return
    if args.preset:
        cfg = PRESETS[args.preset]
        axiom, rules, angle = cfg["axiom"], cfg["rules"], cfg["angle"]
        iters = args.iterations or cfg["iters"]
    else:
        axiom = args.axiom or "F"
        rules = dict(r.split(":") for r in (args.rules or "F:F+F").split(","))
        angle, iters = args.angle, args.iterations
    result = rewrite(axiom, rules, iters)
    strlen, pts = to_ascii(result, angle)
    print(f"String length: {strlen}")
    print(f"Points: {pts}")
    if strlen < 200:
        print(f"Result: {result}")

if __name__ == "__main__":
    main()
