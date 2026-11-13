"""Original seamless 'wind lines' pattern for coastalcr.com (used as a CSS mask so one file recolors per section).
Tile repeats in both directions. Usage: python3 make_wind.py out.svg [streaks|flow]"""
import math, random, sys
out = sys.argv[1]; mode = sys.argv[2] if len(sys.argv) > 2 else 'flow'
W, H, N = 1600, 960, 24            # tile size, lines per tile
gap = H / N
rnd = random.Random(7)
paths = []
for i in range(N):
    y0 = i * gap + gap / 2
    # integer wave counts keep the tile seamless left/right
    k1, k2, k3 = rnd.choice([1, 2]), rnd.choice([2, 3]), rnd.choice([4, 5])
    p1, p2, p3 = (rnd.uniform(0, 2 * math.pi) for _ in range(3))
    a1, a2, a3 = rnd.uniform(9, 15), rnd.uniform(4, 7), rnd.uniform(1, 2.5)
    # neighbouring lines share most of their shape so they flow together like air
    shared = math.sin(i / N * 2 * math.pi) * 0.6
    def y(x):
        t = x / W * 2 * math.pi
        return (y0 + a1 * math.sin(k1 * t + p1 + shared) + a2 * math.sin(k2 * t + p2) + a3 * math.sin(k3 * t + p3))
    if mode == 'flow':
        segs = [(0, W)]
    else:  # wind streaks: broken lengths, some long, some short
        segs, x = [], rnd.uniform(-400, 0)
        while x < W:
            ln = rnd.choice([rnd.uniform(160, 380), rnd.uniform(420, 900)])
            segs.append((x, x + ln)); x += ln + rnd.uniform(90, 320)
    for a, b in segs:
        pts = []
        xx = a
        while xx <= b:
            pts.append(f"{xx % W if mode=='flow' else xx:.1f},{y(xx):.1f}"); xx += 8
        if mode == 'flow':
            pts = [f"{x:.1f},{y(x):.1f}" for x in [j * 8 for j in range(int(W / 8) + 1)]]
        paths.append('M' + ' L'.join(pts))
        # streaks crossing the right edge are redrawn on the left so the tile wraps
        if mode != 'flow' and b > W:
            pts2 = []; xx = a
            while xx <= b:
                pts2.append(f"{xx - W:.1f},{y(xx):.1f}"); xx += 8
            paths.append('M' + ' L'.join(pts2))
        if mode != 'flow' and a < 0:
            pts2 = []; xx = a
            while xx <= b:
                pts2.append(f"{xx + W:.1f},{y(xx):.1f}"); xx += 8
            paths.append('M' + ' L'.join(pts2))
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       f'<path d="{" ".join(paths)}" fill="none" stroke="#000" stroke-width="1.3" stroke-linecap="round"/></svg>')
open(out, 'w').write(svg)
print(out, len(svg) // 1024, 'KB')
