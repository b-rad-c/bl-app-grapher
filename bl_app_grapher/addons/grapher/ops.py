import bpy
from typing import Set
from .util import get_context_for_area, draw_plot


class generate_plot(bpy.types.Operator):
    bl_idname = 'grapher.generate_plot'
    bl_label = 'Generate plot'
    bl_description = 'Generates a plot and updates the image canvas'

    @classmethod
    def poll(cls, _) -> bool:
        return True

    def execute(self, context: bpy.types.Context) -> Set[str]:
        print('grapher.generate_plot()')
        draw_plot(context.scene.grapher_n)

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