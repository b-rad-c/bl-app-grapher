import os
import bpy
import bl_ui
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
    layout.label(text='Grapher configuration')
    #layout.template_header()

empty = lambda self, context: None

class AppStateStore(AppOverrideState):
    __slots__ = ()

    @staticmethod
    def class_ignore():
        bpy.types.IMAGE_HT_header.draw = empty
        bpy.types.TOPBAR_HT_upper_bar.draw_left = draw_left_override
        bpy.types.TOPBAR_HT_upper_bar.draw_right = empty
        bpy.types.TOPBAR_MT_editor_menus.draw = empty

        bpy.types.STATUSBAR_HT_header.draw = empty
        bpy.types.WORKSPACE_PT_main.draw = empty
        bpy.types.PROPERTIES_HT_header.draw = draw_properties_header

        bl_ui.space_properties.PROPERTIES_HT_header.draw = empty
        bpy.types.SpaceProperties.show_region_header = False       

        classes = []

        def func(cls):
            ignore = False
            if cls.__name__.startswith('PROPERTIES'):
                ignore = True
            if cls.__name__.startswith('OBJECT'):
                ignore = True

            if ignore:
                pass
                # print(f'ignoring: {cls.__name__} {cls}')

            return ignore

        for cls in filter(func, bpy.types.Panel.__subclasses__()):
            classes.append(cls)

        # print(f'{len(classes)=}')

        return classes

    # ----------------
    # UI Filter/Ignore

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
def setup_user_preferences(_):
    print('setup_user_preferences()')
    prefs = bpy.context.preferences
    prefs.use_preferences_save = False

    apps = prefs.apps
    apps.show_corner_split = False
    apps.show_regions_visibility_toggle = False
    #apps.show_edge_resize = False

@persistent
def ui_overrides(_: None):
    print('ui_overrides()')
    
    # init wm
    wm = bpy.data.window_managers['WinMan']    
    win = wm.windows[0]
    screen = win.screen
    screen.show_statusbar = False

    # customise spaces
    for area in screen.areas:
        spaces = area.spaces
        for space in spaces:

            if space.type == 'IMAGE_EDITOR':
                space.show_region_header = False
                
            if space.type == 'PROPERTIES':
                space.show_region_header = False


@persistent
def init_grapher(_):
    print('init_grapher()')
    def updater(self, ctx):
        bpy.ops.grapher.generate_plot()
        
    bpy.types.Scene.grapher_n = bpy.props.IntProperty(name='n', description='modify graph n value', default=2, update=updater)
    bpy.ops.grapher.generate_plot()


load_post_handlers = [setup_user_preferences, ui_overrides, init_grapher]

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
