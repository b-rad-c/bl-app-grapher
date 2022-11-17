# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>
import os

import bpy
from bpy.app.handlers import persistent
from bl_app_override.helpers import AppOverrideState


#
# overrides
#

def draw_left_override(self, context: bpy.types.Context):
    layout: bpy.types.UILayout = self.layout
    bpy.types.TOPBAR_MT_editor_menus.draw_collapsible(context, layout)

def draw_properties_header(self, context: bpy.types.Context):
    layout = self.layout
    layout.template_header()

def draw_properties_navigation(self, context):
    return None
    layout = self.layout

    view = context.space_data

    layout.scale_x = 1.4
    layout.scale_y = 1.4
    if view.search_filter:
        layout.prop_tabs_enum(
            view, 'context', data_highlight=view,
            property_highlight='tab_search_results', icon_only=True,
        )
    else:
        #breakpoint()
        layout.prop_tabs_enum(view, 'context', icon_only=True)


class AppStateStore(AppOverrideState):
    # Just provides data & callbacks for AppOverrideState
    __slots__ = ()

    @staticmethod
    def class_ignore():
        classes = []

        bpy.types.STATUSBAR_HT_header.draw = lambda self, context: None
        bpy.types.IMAGE_HT_header.draw = lambda self, context: None
        bpy.types.SEQUENCER_HT_header.draw = lambda self, context: None
        bpy.types.TEXT_HT_header.draw = lambda self, context: None
        bpy.types.TOPBAR_HT_upper_bar.draw_left = draw_left_override
        bpy.types.TOPBAR_HT_upper_bar.draw_right = lambda self, context: None
        bpy.types.TOPBAR_MT_editor_menus.draw = lambda self, context: None

        bpy.types.PROPERTIES_HT_header.draw = draw_properties_header
        bpy.types.PROPERTIES_PT_navigation_bar.draw = draw_properties_navigation
        bpy.types.PROPERTIES_PT_options.draw = lambda self, context: None

        return classes

    @staticmethod
    def ui_ignore_classes():
        return ()

    @staticmethod
    def ui_ignore_operator(op_id):
        return True

    @staticmethod
    def ui_ignore_property(ty, prop):
        return True

    @staticmethod
    def ui_ignore_menu(menu_id):
        return True

    @staticmethod
    def ui_ignore_label(text):
        return True
    
    @staticmethod
    def addon_paths():
        return (os.path.normpath(os.path.join(os.path.dirname(__file__), 'addons')),)

    @staticmethod
    def addons():
        return ('grapher',)

#
# load_post handlers
#

@persistent
def ui_overrides(_: None):
    
    # init wm
    wm = bpy.data.window_managers['WinMan']
    win = wm.windows[0]
    screen = win.screen
    screen.show_statusbar = False

    # customise spaces
    for area in screen.areas:
        for space in area.spaces:

            if space.type == 'IMAGE_EDITOR':
                space.show_region_header = False

            if space.type == 'PROPERTIES':
                items = space.rna_type.properties['context'].enum_items

@persistent
def init_grapher(_):
    bpy.ops.grapher.generate_example_plot()

load_post_handlers = [ui_overrides, init_grapher]

#
# register
#

app_state = AppStateStore()


def register():
    print('Template Register', __file__)
    app_state.setup()

    for handler in load_post_handlers:
        bpy.app.handlers.load_post.append(handler)

def unregister():
    print('Template Unregister', __file__)
    app_state.teardown()

    for handler in reversed(load_post_handlers):
        bpy.app.handlers.load_post.remove(handler)
