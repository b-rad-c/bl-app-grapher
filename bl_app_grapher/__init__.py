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
from pathlib import Path
from typing import Optional, Dict

import bpy
from bpy.app.handlers import persistent
from bl_app_override.helpers import AppOverrideState

import matplotlib.pyplot as plt
import numpy as np
import PIL


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
            view, "context", data_highlight=view,
            property_highlight="tab_search_results", icon_only=True,
        )
    else:
        #breakpoint()
        layout.prop_tabs_enum(view, "context", icon_only=True)


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
# app
#

def get_context_for_area(area: bpy.types.Area, region_type="WINDOW") -> Dict:
    for region in area.regions:
        if region.type == region_type:
            ctx = {}

            # In weird cases, e.G mouse over toolbar of filebrowser,
            # bpy.context.copy is None. Check for that.
            if bpy.context.copy:
                ctx = bpy.context.copy()

            ctx["area"] = area
            ctx["region"] = region
            ctx["screen"] = area.id_data
            return ctx
    return {}


@persistent
def load_background_image(dummy: None):
    # get background image
    graph = Path(__file__).absolute().parent / 'myfig.png'
    image = bpy.data.images.load(graph.as_posix(), check_existing=True)
    image.name = graph.stem

    breakpoint()
    
    # init wm
    wm = bpy.data.window_managers['WinMan']
    win = wm.windows[0]
    screen = win.screen
    screen.show_statusbar = False
    
    # customise spaces
    for area in screen.areas:
        for space in area.spaces:

            if space.type == 'IMAGE_EDITOR':
                print('found img edit')

                space.show_region_header = False
                area.spaces.active.image = image    
                bpy.ops.image.view_all(get_context_for_area(area), fit_view=True)

            if space.type == 'PROPERTIES':
                print('found properties')
                items = space.rna_type.properties['context'].enum_items
                #breakpoint()


def example_plot(opacity=1.0):
    print('example_plot()')
    col = np.linspace(0, 2 * np.pi, 200)
    row = np.sin(col)

    fig, ax = plt.subplots()
    ax.plot(col, row)

    fig.canvas.draw()
    canvas = fig.canvas
    

    width, height = canvas.get_width_height()
    rgb = canvas.tostring_rgb()
    
    print(f'\tcanvas {width=} {height=} {len(rgb)=}')
    print(f'\t{width*height*3=} {width*height*4=}')
    img = PIL.Image.frombytes('RGB', (width, height),  rgb)

    # breakpoint()

    value = lambda n: n * (1/255)

    pixels = []

    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            pixels.extend([value(r), value(g), value(b), opacity])
    
    assert len(pixels) == width * height * 4
    print('\treturning...')
    
    plt.close()
    return width, height, pixels

@persistent
def load_background_image2(_: None):
    # init wm
    wm = bpy.data.window_managers['WinMan']
    win = wm.windows[0]
    screen = win.screen
    screen.show_statusbar = False

    width, height, pixels = example_plot()

    image = bpy.data.images.new('bl-app-grapher-output', width, height)
    # image.scale(width, height)

    print(f'\n...\n{width=} {height=} {len(pixels)}')
    # breakpoint()
    # image.source = 'GENERATED'
    

    # index = 0
    # increment = 4

    print('setting...')

    image.pixels.foreach_set(pixels)

    #image.pixels[:] = pixels
    image.update()

    # breakpoint()

    # for pixel in pixels:
    #     print(f'{index=}')
    #     image.pixels[index:index + increment] = pixel
    #     index += increment

    print('set...')

    #breakpoint()
    
    # customise spaces
    for area in screen.areas:
        for space in area.spaces:

            if space.type == 'IMAGE_EDITOR':
                print('found img edit')

                space.show_region_header = False
                area.spaces.active.image = image    
                bpy.ops.image.view_all(get_context_for_area(area), fit_view=True)

            if space.type == 'PROPERTIES':
                print('found properties')
                items = space.rna_type.properties['context'].enum_items
    


#
# register
#

app_state = AppStateStore()
active_load_post_handlers = [example_plot, load_background_image2]


def register():
    print("Template Register", __file__)
    app_state.setup()

    for handler in active_load_post_handlers:
        bpy.app.handlers.load_post.append(handler)

def unregister():
    print("Template Unregister", __file__)
    app_state.teardown()

    for handler in reversed(active_load_post_handlers):
        bpy.app.handlers.load_post.remove(handler)
