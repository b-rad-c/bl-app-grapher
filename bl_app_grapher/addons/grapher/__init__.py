from grapher import ops, ui, util

bl_info = {
    'name': 'Grapher',
    'author': 'Brad Corlett',
    'description': 'A Blender addon to create graphs',
    'blender': (3, 0, 0),
    'version': (0, 1, 0),
    'category': 'Development',
}

_need_reload = 'ops' in locals()


if _need_reload:
    import importlib
    ops = importlib.reload(ops)
    ui = importlib.reload(ui)
    util = importlib.reload(util)


def register():
    print('Addon Register', __file__)
    ops.register()
    ui.register()


def unregister():
    print('Addon Unregister', __file__)
    ops.unregister()
    ui.unregister()


if __name__ == '__main__':
    register()
