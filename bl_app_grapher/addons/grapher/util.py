import bpy
from io import BytesIO
from pathlib import Path 
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import PIL


PLOT_IMAGE_NAME = 'plot'


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


def draw_plot(n=2):

    #
    # plot
    #
    
    column = np.linspace(0, n * np.pi, 200)
    row = np.sin(column)

    figure, axes = plt.subplots()
    axes.plot(column, row)

    figure.canvas.draw()
    plt.close()
    
    #
    # convert to png
    #

    png = BytesIO()
    figure.canvas.print_png(png)
    pixels = np.asarray(PIL.Image.open(png))
    
    #
    # to bpy image
    #

    height, width, depth = pixels.shape
    
    if PLOT_IMAGE_NAME in bpy.data.images:
        image = bpy.data.images[PLOT_IMAGE_NAME]
        image.scale(width, height)
    else:
        image = bpy.data.images.new(PLOT_IMAGE_NAME, width=width, height=height)
    
    inverted_y_axis = np.flip(pixels, axis=0)
    bpy_pixels = np.fromiter(inverted_y_axis.ravel() / 255.0, dtype=np.float64, count=width * height * depth)

    image.pixels.foreach_set(bpy_pixels.tolist())
    image.update()
