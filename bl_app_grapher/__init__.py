import os
import bpy
from bpy.app.handlers import persistent
import bl_app_override
from bl_app_override.helpers import AppOverrideState
import bl_ui

from . import ui


def dump_classes(filename):
    classes = [bpy.types.Panel, bpy.types.Header, bpy.types.Menu, bpy.types.Operator]
    with open(filename, 'w+') as f:
        for parent_class in classes:
            f.write(f'{parent_class}\n')
            for cls in parent_class.__subclasses__():
                f.write(f'\t{cls}\n')

# dump_classes('dump_classes.txt')

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

empty = lambda self, context: None

class AppStateStore(AppOverrideState):
    __slots__ = ()

    @staticmethod
    def class_ignore():
               
        bpy.types.IMAGE_HT_header.draw = lambda self, context: None
        bpy.types.TOPBAR_HT_upper_bar.draw_left = draw_left_override
        bpy.types.TOPBAR_HT_upper_bar.draw_right = lambda self, context: None
        bpy.types.TOPBAR_MT_editor_menus.draw = lambda self, context: None

        bpy.types.STATUSBAR_HT_header.draw = lambda self, context: None
        bpy.types.WORKSPACE_PT_main.draw =lambda self, context: None
        bpy.types.PROPERTIES_HT_header.draw = draw_properties_header
        bpy.types.PROPERTIES_PT_navigation_bar.draw = draw_properties_navigation
        #bpy.types.PROPERTIES_PT_navigation_bar.width=1
        #bpy.types.PROPERTIES_PT_navigation_bar.height=1
        #bpy.types.PROPERTIES_PT_options.draw = lambda self, context: None

        bl_ui.space_properties.PROPERTIES_HT_header.draw = lambda self, context: None
        #bpy.types.OBJECT_PT_context_object.draw = lambda self, context: None
        bpy.types.SpaceProperties.show_region_header = False
        bpy.types.SpaceProperties.type = 'EMPTY'
        bpy.types.SpaceProperties.draw = lambda self, context: None
        

        classes = [
            #bpy.types.PROPERTIES_PT_navigation_bar
        ]

        def func(cls):
            ignore = False
            if cls.__name__.startswith('PROPERTIES'):
                ignore = True
            if cls.__name__.startswith('OBJECT'):
                ignore = True

            if ignore:
                print(f'ignoring: {cls.__name__} {cls}')

            return ignore

        for cls in filter(func, bpy.types.Panel.__subclasses__()):
            classes.append(cls)
            #print(type(cls.__name__), cls.__name__)
            # breakpoint()

        # classes.extend(
        #     bl_app_override.class_filter(
        #         bpy.types.Panel,
        #         blacklist=[ui.GrapherPanel]
        #     ),
        # )

        print(f'{len(classes)=}')

        return classes

    # ----------------
    # UI Filter/Ignore

    @staticmethod
    def ui_ignore_classes():
        return (
            # bpy.types.Header,
            # bpy.types.Menu,
            # bpy.types.Panel,
        )

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
        regions = area.regions
        spaces = area.spaces
        def dump_regions():
            for region in regions:
                    print(f'\t{region.type} {region.alignment=} {region.width=} {region.height=} {region.x=} {region.y=}')
        for space in spaces:

            if space.type == 'IMAGE_EDITOR':
                space.show_region_header = False
                print('IMAGE_EDITOR')
                dump_regions()
                #breakpoint()
                

            if space.type == 'PROPERTIES':
                space.show_region_header = False
                #space.use
                print('PROPERTIES')
                dump_regions()
                breakpoint()


@persistent
def init_grapher(_):
    print('init_grapher()')
    updater = lambda self, ctx: bpy.ops.grapher.refresh_plot()
    bpy.types.Scene.grapher_n = bpy.props.IntProperty(name='n', description='modify graph n value', default=2, update=updater)
    bpy.ops.grapher.refresh_plot()


load_post_handlers = [setup_user_preferences, ui_overrides, init_grapher]

#
# register
#

app_state = AppStateStore()


def register():
    print('Template Register', __file__)
    app_state.setup()

    ui.register()

    for handler in load_post_handlers:
        bpy.app.handlers.load_post.append(handler)

def unregister():
    print('Template Unregister', __file__)
    app_state.teardown()

    ui.unregister()

    for handler in reversed(load_post_handlers):
        bpy.app.handlers.load_post.remove(handler)
