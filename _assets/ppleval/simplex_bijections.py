"""simplex-bijections.svg and simplex-bijections-dark.svg: one constrained space, three unconstraining maps.

The 3-simplex on the left; on the right, its image in the plane under the simplex
transform of Stan, of Bijectors.jl / NumPyro, and of PyMC. Every curve and dot is
computed from the transform itself, and each transform is pinned by an assert to
its row of the table in pages/BayesEx/PPLEval.md. The figure is drawn once per site
theme, in that theme's paper, ink and series colours; the page shows the one that matches.

    uv run --no-project --with numpy --with matplotlib python _assets/ppleval/simplex_bijections.py
"""
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.colors import to_rgb
from matplotlib.patches import FancyArrowPatch

HERE = Path(__file__).parent

# one palette per site theme, taken from the tokens in _css/franklin.css
THEMES = {
    "simplex-bijections.svg": dict(
        paper="#FFFFFF", ink="#1A1917", muted="#6C6962", faint="#B9B6AE",
        orange="#C06A2E", purple="#6A4C99", green="#457E45", teal="#2A6E7E"),
    "simplex-bijections-dark.svg": dict(
        paper="#16150F", ink="#E9E4D8", muted="#A29C8F", faint="#5E5A4F",
        orange="#D9925A", purple="#9079C0", green="#579C55", teal="#63A8B8"),
}
plt.rcParams.update({
    "font.family": ["Iowan Old Style", "Palatino", "Georgia"], "font.size": 10.8,
    "mathtext.fontset": "cm", "svg.fonttype": "path", "svg.hashsalt": "simplex-bijections",
})


# ---- the transforms: constrained x on the simplex -> unconstrained y in the plane
def clr(x):
    lx = np.log(x)
    return lx - lx.mean(axis=-1, keepdims=True)


def stan(x):
    """Stan >= 2.37: x = softmax(sum_to_zero(y)), so y = sum_to_zero_free(clr(x))."""
    z = clr(x)
    y1 = -z[..., 2] * np.sqrt(6) / 2
    return np.stack([(y1 / np.sqrt(6) - z[..., 1]) * np.sqrt(2), y1], axis=-1)


def stick(x):
    """Bijectors.jl SimplexBijector and NumPyro StickBreakingTransform."""
    logit = lambda p: np.log(p) - np.log1p(-p)
    return np.stack([logit(x[..., 0]) + np.log(2), logit(x[..., 1] / (1 - x[..., 0]))], axis=-1)


def pymc(x):
    """PyMC SimplexTransform: centred logs, last coordinate dropped."""
    return clr(x)[..., :2]


MAPS = [("Stan", "softmax of a\nsum-to-zero vector", stan),
        ("Bijectors.jl, NumPyro", "stick-breaking", stick),
        ("PyMC", "centred log-ratio", pymc)]

P = np.array([0.2, 0.3, 0.5])                       # the test point of the table
for (_, _, f), row in zip(MAPS, [[-0.2867, -0.5826], [-0.6931, -0.5108], [-0.4406, -0.0351]]):
    assert np.allclose(f(P), row, atol=5e-5)
    assert np.allclose(f(np.full(3, 1 / 3)), 0, atol=1e-12)

HOT = 0.2                                           # the coloured level in each direction
COLOURED = [(0, "purple"), (1, "green"), (2, "teal")]       # direction -> palette key
GRID = [(k, c) for k in range(3) for c in (0.4, 0.6, 0.8)]
OTHERS = np.array([
    [0.60, 0.20, 0.20], [0.10, 0.10, 0.80], [0.45, 0.45, 0.10], [0.06, 0.60, 0.34],
    [0.30, 0.06, 0.64], [0.72, 0.22, 0.06], [0.36, 0.30, 0.34], [0.12, 0.38, 0.50],
    [0.50, 0.08, 0.42], [0.22, 0.66, 0.12],
    [0.88, 0.07, 0.05],                             # x1 > 0.8: beyond every drawn line in the stick-breaking plane
])

# ---- geometry of the page
CORNERS = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]])
bary = lambda x: x @ CORNERS
R = 4.4                                             # half-width of a plane; curves are gone by here
SIZE = 2.1                                          # a plane, in inches
UNIT = SIZE / (2 * R)                               # inches per plane unit
W, H = 8.5, 6.15                                    # wider than the text column: labels are set near 11pt
                                                    # so they land around 12px once the page scales it down
minus = lambda s: s.replace("-", "−")


def const_line(k, c, n=500, eps=1e-6):
    """The line x_k = c across the simplex, sampled densely towards both ends."""
    i, j = [a for a in range(3) if a != k]
    t = np.clip((1 - c) / (1 + np.exp(-np.linspace(-9, 9, n))), eps, 1 - c - eps)
    x = np.empty((n, 3)); x[:, k], x[:, i], x[:, j] = c, t, 1 - c - t
    return x


def fade(y):
    """1 near the middle of a plane, falling smoothly to 0 at radius R."""
    s = np.clip((np.linalg.norm(y, axis=-1) / R - 0.45) / 0.55, 0, 1)
    return 1 - s * s * (3 - 2 * s)


def faded_curve(ax, y, colour, lw, zorder, levels=24):
    """Draw y as runs of constant opacity, so the curve dissolves instead of being clipped."""
    alpha = np.round(fade((y[:-1] + y[1:]) / 2) * levels) / levels
    start = 0
    for i in range(1, len(alpha) + 1):
        if i == len(alpha) or alpha[i] != alpha[start]:
            if alpha[start] > 0:
                ax.plot(*y[start:i + 1].T, color=colour, lw=lw, alpha=alpha[start], zorder=zorder,
                        solid_capstyle="butt")
            start = i


def render(pal, dest):
    """Draw the figure in palette pal and save it to dest."""
    halo = [pe.withStroke(linewidth=3, foreground=pal["paper"])]
    fig = plt.figure(figsize=(W, H))
    inch = lambda left, bottom, w, h: fig.add_axes([left / W, bottom / H, w / W, h / H])

    # ---- the simplex
    a = inch(0.25, H / 2 - 1.4, 2.5, 2.5)
    a.set_aspect("equal"); a.axis("off"); a.set_xlim(-0.08, 1.08); a.set_ylim(-0.15, 1.01)
    a.plot(*np.vstack([CORNERS, CORNERS[:1]]).T, color=pal["ink"], lw=1.3, zorder=5, solid_joinstyle="round")
    for name, (cx, cy), (dx, dy) in zip(["$x_1$", "$x_2$", "$x_3$"], CORNERS, [(-0.05, -0.04), (0.05, -0.04), (0, 0.055)]):
        a.text(cx + dx, cy + dy, name, ha="center", va="center", color=pal["muted"], fontsize=11.8)
    for k, c in GRID:
        a.plot(*bary(const_line(k, c)).T, color=pal["faint"], lw=0.6, ls=(0, (1, 2.2)), zorder=2)
    a.scatter(*bary(OTHERS).T, s=7, color=pal["muted"], alpha=0.5, lw=0, zorder=6)
    for k, key in COLOURED:
        a.plot(*bary(const_line(k, HOT)).T, color=pal[key], lw=1.4, ls=(0, (1, 1.8)), zorder=4, dash_capstyle="round")
    a.scatter(*bary(P), s=42, color=pal["orange"], zorder=9)
    a.annotate("(0.2, 0.3, 0.5)", bary(P), xytext=(-0.02, 0.62), fontsize=10.8, color=pal["orange"], ha="center",
               arrowprops=dict(arrowstyle="-", color=pal["orange"], lw=0.6, shrinkB=4))
    a.text(0.5, 1.085, "simplex", ha="center", fontsize=12.8, color=pal["ink"])
    a.text(0.5, 1.02, "constrained space", ha="center", fontsize=10.2, color=pal["muted"])
    for (k, key), xpos in zip(COLOURED, [0.2, 0.5, 0.8]):
        a.text(xpos, -0.12, f"$x_{k + 1} = {HOT}$", ha="center", va="top", fontsize=10.8, color=pal[key])

    # ---- three planes fanned around the simplex, each reached by its own map arrow
    PLANES = [(4.8, H - 0.6 - SIZE / 2, -0.22), (7.3, 2.95, 0.0), (4.8, 0.1 + SIZE / 2, 0.22)]       # centre x, y, arrow bend
    TAILS = [(2.7, H / 2 + 0.8), (2.95, 2.95), (2.7, H / 2 - 0.85)]
    for (name, how, f), (cx, cy, bend), tail in zip(MAPS, PLANES, TAILS):
        ax = inch(cx - SIZE / 2, cy - SIZE / 2, SIZE, SIZE)
        ax.set_xlim(-R, R); ax.set_ylim(-R, R); ax.set_aspect("equal"); ax.axis("off")

        for k, c in GRID:
            faded_curve(ax, f(const_line(k, c)), pal["faint"], 0.6, 2)
        for k, key in COLOURED:
            faded_curve(ax, f(const_line(k, HOT)), pal[key], 1.4, 4)
        others = f(OTHERS)
        ax.scatter(*others.T, s=7, color=[(*to_rgb(pal["muted"]), 0.5 * al) for al in fade(others)], lw=0, zorder=6)

        y = f(P)
        ax.scatter(*y, s=42, color=pal["orange"], zorder=9)
        top = cy + SIZE / 2                                                       # header: library, then where P landed
        fig.text(cx / W, (top + 0.3) / H, name, ha="center", va="baseline", fontsize=12.8, color=pal["ink"])
        fig.text(cx / W, (top + 0.08) / H, minus(f"({y[0]:.4f}, {y[1]:.4f})"), ha="center", va="baseline", fontsize=10.8,
                 color=pal["orange"])
        ax.text(0.93, 0.91, r"$\mathbb{R}^2$", transform=ax.transAxes, ha="center", va="center", fontsize=11.8, color=pal["muted"])

        centre, tail = np.array([cx, cy]), np.array(tail)
        head = centre + (tail - centre) / np.linalg.norm(tail - centre) * SIZE * 0.52
        fig.add_artist(FancyArrowPatch(tail, head, transform=fig.dpi_scale_trans, connectionstyle=f"arc3,rad={bend}",
                                       arrowstyle="->,head_length=6,head_width=3.2", color=pal["ink"], lw=1.0))
        ctrl = (tail + head) / 2 + bend * np.array([head[1] - tail[1], -(head[0] - tail[0])])
        crest = 0.25 * tail + 0.5 * ctrl + 0.25 * head
        out = ctrl - (tail + head) / 2
        out = out / np.linalg.norm(out) if np.linalg.norm(out) > 1e-9 else np.array([0.0, 1.0])
        lab = crest + out * (0.14 + 0.15 * (how.count("\n") + 1))
        fig.text(lab[0] / W, lab[1] / H, how, ha="center", va="center", fontsize=10.8, style="italic", linespacing=1.05,
                 color=pal["ink"], path_effects=halo)
    fig.savefig(dest, facecolor=pal["paper"], bbox_inches="tight", pad_inches=0.08, metadata={"Date": None})
    plt.close(fig)
    print(f"wrote {dest.name}: {dest.stat().st_size / 1024:.0f} kB")


for filename, palette in THEMES.items():
    render(palette, HERE / filename)
