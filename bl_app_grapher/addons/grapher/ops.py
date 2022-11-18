import bpy
from typing import Set
from .util import TMP_PNG_PATH, example_plot, example_plot2, get_context_for_area
import numpy as np
from io import BytesIO


class refresh_plot(bpy.types.Operator):
    bl_idname = 'grapher.refresh_plot'
    bl_label = 'Refresh plot'
    bl_description = 'Refreshes the plot image'

    @classmethod
    def poll(cls, _) -> bool:
        return True

    def execute(self, context: bpy.types.Context) -> Set[str]:
        example_plot(context.scene.grapher_n)
        image = bpy.data.images.load(TMP_PNG_PATH)

        for area in context.screen.areas:
            for space in area.spaces:
                if space.type == 'IMAGE_EDITOR':
                    area.spaces.active.image = image    
                    bpy.ops.image.view_all(get_context_for_area(area), fit_view=True)
                    break

        return {"FINISHED"}


class generate_plot(bpy.types.Operator):
    bl_idname = 'grapher.generate_plot'
    bl_label = 'Generate plot'
    bl_description = 'Generates the plot!'

    @classmethod
    def poll(cls, _) -> bool:
        return True

    def execute(self, context: bpy.types.Context) -> Set[str]:
        canvas = example_plot2(context.scene.grapher_n)
        width, height = canvas.get_width_height()
        rgb = canvas.tostring_rgb()
        pixel_data = np.frombuffer(rgb, dtype=np.uint32)

        value = lambda n: int(n) * (1/4294967296)

        #breakpoint()
        

        # depth = 4
        pixels = [] # np.zeros(width * height * 4)
        for pixel in np.split(pixel_data, width * height):
            pixels.append(value(pixel[0]))
            pixels.append(value(pixel[1]))
            pixels.append(value(pixel[2]))
            pixels.append(1.0)


        image = bpy.data.images.new('grapher-canvas', width, height)
        image.scale(width, height)
        
        #breakpoint()

        #raveled = pixels.ravel()
        image.pixels.foreach_set(pixels)
        image.update()

        for area in context.screen.areas:
            for space in area.spaces:
                if space.type == 'IMAGE_EDITOR':
                    area.spaces.active.image = image    
                    bpy.ops.image.view_all(get_context_for_area(area), fit_view=True)
                    break

        return {"FINISHED"}



#
# registration
#


classes = [refresh_plot, generate_plot]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)