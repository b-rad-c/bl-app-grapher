import bpy
from typing import Dict


def get_context_for_area(area: bpy.types.Area, region_type='WINDOW') -> Dict:
    for region in area.regions:
        if region.type == region_type:
            ctx = {}

            # In weird cases, e.G mouse over toolbar of filebrowser,
            # bpy.context.copy is None. Check for that.
            if bpy.context.copy:
                ctx = bpy.context.copy()

            ctx['area'] = area
            ctx['region'] = region
            ctx['screen'] = area.id_data
            return ctx

    return {}
