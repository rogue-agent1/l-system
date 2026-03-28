#!/usr/bin/env python3
"""L-System — string rewriting with ASCII turtle graphics."""
import sys, math
PRESETS={"koch":{"axiom":"F","rules":{"F":"F+F-F-F+F"},"angle":90,"iters":3},"sierpinski":{"axiom":"F-G-G","rules":{"F":"F-G+F+G-F","G":"GG"},"angle":120,"iters":4},"dragon":{"axiom":"FX","rules":{"X":"X+YF+","Y":"-FX-Y"},"angle":90,"iters":10},"plant":{"axiom":"X","rules":{"X":"F+[[X]-X]-F[-FX]+X","F":"FF"},"angle":25,"iters":4}}
def expand(axiom, rules, iters):
    s=axiom
    for _ in range(iters): s="".join(rules.get(c,c) for c in s)
    return s
def render(instructions, angle_deg, w=70, h=30):
    x=y=0.0; a=0; points=[(x,y)]
    stack=[]
    for c in instructions:
        if c in "FG": x+=math.cos(math.radians(a)); y+=math.sin(math.radians(a)); points.append((x,y))
        elif c=="+": a+=angle_deg
        elif c=="-": a-=angle_deg
        elif c=="[": stack.append((x,y,a))
        elif c=="]": x,y,a=stack.pop()
    xs=[p[0] for p in points]; ys=[p[1] for p in points]
    mnx,mxx,mny,mxy=min(xs),max(xs),min(ys),max(ys)
    rx,ry=mxx-mnx or 1,mxy-mny or 1
    grid=[[" "]*w for _ in range(h)]
    for px,py in points:
        c=int((px-mnx)/rx*(w-1)); r=h-1-int((py-mny)/ry*(h-1))
        if 0<=r<h and 0<=c<w: grid[r][c]="*"
    for row in grid: print("".join(row))
def cli():
    name=sys.argv[1] if len(sys.argv)>1 else "koch"
    preset=PRESETS.get(name)
    if not preset: print(f"Available: {list(PRESETS.keys())}"); sys.exit(1)
    s=expand(preset["axiom"],preset["rules"],preset["iters"])
    print(f"  {name}: {len(s)} instructions")
    render(s, preset["angle"])
if __name__=="__main__": cli()
