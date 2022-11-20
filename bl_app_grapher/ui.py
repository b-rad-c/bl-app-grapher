import bpy
from typing import Any

#
# properties panel
#

class GrapherPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = 'Properties'
    bl_idname = 'GRAPHER_PT_panel'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'
    #bl_options = {'INSTANCED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(context.scene, 'grapher_n')

        row = layout.row()
        row.operator('grapher.refresh_plot')

#
# topbar (file/window menus)
#

class MV_TOPBAR_MT_file_menu(bpy.types.Menu):
    bl_idname = 'MV_TOPBAR_MT_file_menu'
    bl_label = 'File'

    def draw(self, context: bpy.types.Context) -> None:
        row = self.layout.row(align=True)
        row.operator('wm.quit_blender', text='Quit', icon='QUIT')

class MV_TOPBAR_MT_window_menu(bpy.types.Menu):
    bl_idname = 'MV_TOPBAR_MT_window_menu'
    bl_label = 'Window'

    def draw(self, context: bpy.types.Context) -> None:
        layout: bpy.types.UILayout = self.layout
        row = layout.row(align=True)
        row.operator('wm.window_fullscreen_toggle', icon='FULLSCREEN_ENTER')

def topbar_menu_draw(self: Any, context: bpy.types.Context) -> None:
    self.layout.menu('MV_TOPBAR_MT_file_menu')
    self.layout.menu('MV_TOPBAR_MT_window_menu')

#
# registration
#

classes = [MV_TOPBAR_MT_file_menu, MV_TOPBAR_MT_window_menu, GrapherPanel]
#classes = []
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_editor_menus.append(topbar_menu_draw)

def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(topbar_menu_draw)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)