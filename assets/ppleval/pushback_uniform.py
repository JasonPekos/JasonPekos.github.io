"""pushback-uniform.svg and pushback-uniform-dark.svg: sample in the plane without the Jacobian term, then map back.

The target is the uniform measure on the 3-simplex. Without the Jacobian term its density on the
plane is a constant, which has no distribution over all of R^2, so the draws are uniform inside
the window shown. Mapped back through Stan's simplex transform they pile up along the edges and
in the corners. Shading is the measure that was wanted; dots are what was drawn. The figure is
drawn once per site theme; the page shows the one that matches.

    uv run --no-project --with numpy --with matplotlib python _assets/ppleval/pushback_uniform.py
"""
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

HERE = Path(__file__).parent

# one palette per site theme, taken from the tokens in _css/franklin.css
THEMES = {
    "pushback-uniform.svg": dict(paper="#FFFFFF", ink="#1A1917", muted="#6C6962", rule="#DDDBD5", flat="#CFCDC8"),
    "pushback-uniform-dark.svg": dict(paper="#16150F", ink="#E9E4D8", muted="#A29C8F", rule="#33302A", flat="#3B382F"),
}
plt.rcParams.update({
    "font.family": ["Iowan Old Style", "Palatino", "Georgia"], "font.size": 9.2,
    "mathtext.fontset": "cm", "svg.fonttype": "path", "svg.hashsalt": "pushback-uniform",
})


def inv_stan(y):
    """Stan's simplex transform, unconstrained -> simplex: softmax of a sum-to-zero vector."""
    z1 = y[..., 1] / np.sqrt(6) - y[..., 0] / np.sqrt(2)
    z2 = -2 * y[..., 1] / np.sqrt(6)
    z = np.stack([-z1 - z2, z1, z2], axis=-1)
    e = np.exp(z - z.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


assert np.allclose(inv_stan(np.array([-0.2867, -0.5826])), [0.2, 0.3, 0.5], atol=1e-4)   # the table's Stan row

L = 4.6                                             # half-width of the window the draws fill
N = 420
u = np.random.default_rng(11).uniform(-L, L, size=(N, 2))
x = inv_stan(u)

CORNERS = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]])
SZ, Y0 = 2.15, 0.4                                  # panel size and baseline, inches
XS = [0.2, 3.25]
W, H = XS[1] + SZ + 0.2, 3.0                        # narrower than the text column, so it shows at natural size


def render(c, out):
    """Draw the figure in palette c and save it to out."""
    fig = plt.figure(figsize=(W, H))
    inch = lambda left, bottom, w, h: fig.add_axes([left / W, bottom / H, w / W, h / H])

    # ---- the plane: a constant, and uniform draws from the window
    ax = inch(XS[0], Y0, SZ, SZ)
    ax.set_xlim(-L, L); ax.set_ylim(-L, L); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_facecolor(c["flat"])
    for s in ax.spines.values():
        s.set_color(c["rule"]); s.set_linewidth(0.8)
    ax.axhline(0, color=c["muted"], lw=0.6, ls=(0, (1, 2.5)), zorder=2)
    ax.axvline(0, color=c["muted"], lw=0.6, ls=(0, (1, 2.5)), zorder=2)
    ax.scatter(*u.T, s=3.4, color=c["ink"], alpha=0.6, lw=0, zorder=4)

    # ---- the simplex: the uniform measure that was wanted, and where the draws landed
    a = inch(XS[1], Y0, SZ, SZ)
    a.set_aspect("equal"); a.axis("off"); a.set_xlim(-0.07, 1.07); a.set_ylim(-0.14, 1.0)
    a.fill(*CORNERS.T, color=c["flat"], lw=0, zorder=1)
    a.plot(*np.vstack([CORNERS, CORNERS[:1]]).T, color=c["ink"], lw=1.2, zorder=5, solid_joinstyle="round")
    a.scatter(*(x @ CORNERS).T, s=3.4, color=c["ink"], alpha=0.6, lw=0, zorder=6, clip_on=False)
    for name, (cx, cy), (dx, dy) in zip(["$x_1$", "$x_2$", "$x_3$"], CORNERS, [(-0.06, -0.05), (0.06, -0.05), (0, 0.065)]):
        a.text(cx + dx, cy + dy, name, ha="center", va="center", color=c["muted"])

    for cx, formula in zip([XS[0] + SZ / 2, XS[1] + SZ / 2], [r"$p\left(f^{-1}(u)\right)$", r"$\Psi = f^{-1}(u)$"]):
        fig.text(cx / W, (Y0 - 0.12) / H, formula, ha="center", va="top", fontsize=9.8, color=c["ink"])
    fig.text(0.5, (Y0 + SZ + 0.2) / H, "Uniform measure over simplex", ha="center", va="bottom", fontsize=11, color=c["ink"])

    x0, x1, yy = XS[0] + SZ + 0.12, XS[1] - 0.02, Y0 + SZ / 2
    fig.add_artist(FancyArrowPatch((x0, yy), (x1, yy), transform=fig.dpi_scale_trans,
                                   arrowstyle="->,head_length=6,head_width=3.2", color=c["ink"], lw=1.0))
    fig.text((x0 + x1) / 2 / W, (yy + 0.13) / H, r"$f^{-1}$", ha="center", va="bottom", fontsize=9.8, color=c["ink"])
    fig.savefig(out, facecolor=c["paper"], bbox_inches="tight", pad_inches=0.08, metadata={"Date": None})
    plt.close(fig)
    print(f"wrote {out.name}: {out.stat().st_size / 1024:.0f} kB")


for filename, palette in THEMES.items():
    render(palette, HERE / filename)
