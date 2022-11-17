import bpy
from io import BytesIO
from pathlib import Path 
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import PIL


TMP_PNG_PATH = (Path(__file__).parent / 'grapher.tmp.png').as_posix()


def get_context_for_area(area: bpy.types.Area, region_type='WINDOW') -> Dict:
    for region in area.regions:
        if region.type == region_type:
            ctx = {}

            # In weird cases, e.G mouse over toolbar of filebrowser,
            # bpy.context.copy is None. Check for that.
            if bpy.context.copy:
                ctx = bpy.context.copy()

            ctx['area'] = area
            ctx['region'] = region
            ctx['screen'] = area.id_data
            return ctx

    return {}
0

def example_plot(n=2):
    col = np.linspace(0, n * np.pi, 200)
    row = np.sin(col)

    fig, ax = plt.subplots()
    ax.plot(col, row)

    fig.canvas.draw()
    canvas = fig.canvas

    plt.close()

    png = BytesIO()
    canvas.print_png(png)
    
    img = PIL.Image.open(png)
    img.save(TMP_PNG_PATH)

