"""
A module level docstring
"""

import matplotlib.colors as mcolors
from pptx.dml.color import RGBColor

colors = {name: RGBColor(*[int(_ * 255) for _ in mcolors.hex2color(rgb)]) for name, rgb in mcolors.CSS4_COLORS.items()}

if __name__ == '__main__':  # pragma: no cover
    print(colors)
