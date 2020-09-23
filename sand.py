"""
Beware, it can be slow:
$ python sand.py 24
[...]
7866375 iterations in 14 days, 15:47:07
"""
from datetime import datetime
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.animation import FFMpegWriter


def apply_gravity(grid):
    i = 0
    begin = datetime.now().replace(microsecond=0)
    while np.max(grid) > 3:
        max = np.max(grid)
        if i % 100000 == 0:
            yield None

        if i % 10000 == 0:
            elapsed = datetime.now().replace(microsecond=0) - begin
            print(
                f"{datetime.now().replace(microsecond=0).isoformat()} {elapsed} iteration={i}, max={max}, sum={np.sum(grid)}"
            )
        i += 1

        tops = grid == max
        grid[tops] = max % 4
        grid[1:, :][tops[:-1, :]] += max // 4
        grid[:-1, :][tops[1:, :]] += max // 4
        grid[:, 1:][tops[:, :-1]] += max // 4
        grid[:, :-1][tops[:, 1:]] += max // 4

        grid[0, :] = 0
        grid[-1, :] = 0
        grid[:, 0] = 0
        grid[:, -1] = 0

        tops = grid > 3
        grid[tops] -= 4
        grid[1:, :][tops[:-1, :]] += 1
        grid[:-1, :][tops[1:, :]] += 1
        grid[:, 1:][tops[:, :-1]] += 1
        grid[:, :-1][tops[:, 1:]] += 1

        grid[0, :] = 0
        grid[-1, :] = 0
        grid[:, 0] = 0
        grid[:, -1] = 0
    print(f"{i} iterations in {datetime.now().replace(microsecond=0) - begin}")


def main():
    power = int(sys.argv[1])
    height = 2 ** power
    width = int(height ** 0.5)
    sandpile = np.zeros((width, width), dtype=np.uint32)
    sandpile[width // 2, width // 2] = height
    my_cmap = colors.ListedColormap(["white", "green", "purple", "gold"])
    bounds = [-1, 0.5, 1.5, 2.5, 3.5]
    norm = colors.BoundaryNorm(bounds, my_cmap.N)
    writer = FFMpegWriter(
        fps=15, metadata={"title": "Abelian Sand", "artist": "Matplotlib"}
    )
    fig, ax = plt.subplots()
    plt.axis("off")
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
    im = ax.imshow(sandpile, cmap=my_cmap, norm=norm)
    min_height = np.max(sandpile)
    with writer.saving(fig, f"sand-{power}.mp4", dpi=100):
        for i, _ in enumerate(apply_gravity(sandpile)):
            im.set_data(sandpile)
            min_height = min(min_height, np.max(sandpile))
            im.set_clim(0, 4)  # min_height)
            writer.grab_frame()
            np.save(f"video/frame-{power}-{i:09d}", sandpile)
    np.save(f"sand-{power}", sandpile)
    plt.imsave(f"sand-{power}.png", sandpile, cmap=my_cmap)


if __name__ == "__main__":
    main()
