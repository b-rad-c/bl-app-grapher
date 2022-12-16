import bpy
from typing import Set
from .util import get_context_for_area
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import PIL

PLOT_IMAGE_NAME = 'plot'


def draw_plot(periods=1, function='sin'):

    #
    # plot
    #
    
    column = np.linspace(0, np.pi * 2 * periods, 200)
    row = getattr(np, function)(column)

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


class generate_plot(bpy.types.Operator):
    bl_idname = 'grapher.generate_plot'
    bl_label = 'Generate plot'
    bl_description = 'Generates a plot and updates the image canvas'

    @classmethod
    def poll(cls, _) -> bool:
        return True

    def execute(self, context: bpy.types.Context) -> Set[str]:
        print('grapher.generate_plot()')
        draw_plot(context.scene.grapher_periods, context.scene.grapher_function)

        for area in context.screen.areas:
            for space in area.spaces:
                if space.type == 'IMAGE_EDITOR': 
                    bpy.ops.image.view_all(get_context_for_area(area), fit_view=True)
                    break

        return {"FINISHED"}


#
# registration
#


classes = [generate_plot]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)