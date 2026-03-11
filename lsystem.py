#!/usr/bin/env python3
"""L-system fractal generator."""
import sys, math
PRESETS={
  'koch':{'axiom':'F','rules':{'F':'F+F-F-F+F'},'angle':90,'iters':3},
  'sierpinski':{'axiom':'F-G-G','rules':{'F':'F-G+F+G-F','G':'GG'},'angle':120,'iters':4},
  'dragon':{'axiom':'FX','rules':{'X':'X+YF+','Y':'-FX-Y'},'angle':90,'iters':10},
  'plant':{'axiom':'X','rules':{'X':'F+[[X]-X]-F[-FX]+X','F':'FF'},'angle':25,'iters':5},
}
name=sys.argv[1] if len(sys.argv)>1 else 'koch'
p=PRESETS.get(name,PRESETS['koch'])
s=p['axiom']
for _ in range(p['iters']):
    s=''.join(p['rules'].get(c,c) for c in s)
x=y=0; a=0; pts=[(0,0)]; stk=[]
for c in s:
    if c in 'FG': x+=math.cos(math.radians(a)); y+=math.sin(math.radians(a)); pts.append((x,y))
    elif c=='+': a+=p['angle']
    elif c=='-': a-=p['angle']
    elif c=='[': stk.append((x,y,a))
    elif c==']': x,y,a=stk.pop()
mnx=min(p[0] for p in pts); mny=min(p[1] for p in pts)
mxx=max(p[0] for p in pts); mxy=max(p[1] for p in pts)
W,H=60,30
grid=[[' ']*W for _ in range(H)]
for px,py in pts:
    c=int((px-mnx)/(mxx-mnx+.001)*(W-1)); r=int((py-mny)/(mxy-mny+.001)*(H-1))
    if 0<=r<H and 0<=c<W: grid[r][c]='*'
for row in grid: print(''.join(row))
print(f"\nL-system: {name}, {p['iters']} iterations, {len(s)} symbols")
