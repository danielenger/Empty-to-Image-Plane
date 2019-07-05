#    Empty to Image Plane
#    Copyright (C) 2019 Daniel Engler

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

bl_info = {
    "name": "Empty to Image Plane",
    "description": "Add an Image Plane at every (selected) Image Empty",
    "author": "Daniel Engler",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Tools > Toolbar",
    "category": "Object"
}

import bpy

from .empty_image_planes import *

classes = (
    EMPTPYTOIMAGEPLANE_PT_panel,
    EMPTPYTOIMAGEPLANE_OT_add_planes
)

def register():
   for cls in classes:
      bpy.utils.register_class(cls)

    
def unregister():
   for cls in reversed(classes):
      bpy.utils.unregister_class(cls)


if __name__ == "__main__":
   register()
