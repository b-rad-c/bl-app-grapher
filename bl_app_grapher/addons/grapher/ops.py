import bpy
from typing import Set
from .util import TMP_PNG_PATH, example_plot, get_context_for_area


class refresh_plot(bpy.types.Operator):
    bl_idname = 'grapher.refresh_plot'
    bl_label = 'Refresh plot'
    bl_description = 'Refreshes the plot image'

    @classmethod
    def poll(cls, _) -> bool:
        return True

    def execute(self, context: bpy.types.Context) -> Set[str]:
        print('grapher.refresh_plot.execute()')
        example_plot(context.scene.grapher_n)
        image = bpy.data.images.load(TMP_PNG_PATH)

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


classes = [refresh_plot]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)