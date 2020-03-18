#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#======================= END GPL LICENSE BLOCK ========================

# <pep8 compliant>

import bpy # pylint: disable=import-error

# Animation (actions) tools and methods

def remove_keyframes_from_object(obj):
    """
    Removes all keyframes from fcurves found applying to this object

    :arg obj: The object
    :type onj : Object(ID)
    """
    for curve in obj.animation_data.action.fcurves:
        keyframes = curve.keyframe_points
        for keyframe in reversed(keyframes):
            keyframes.remove(keyframe, fast = True)

def reset_transform(obj):
    """
    Resets all transformation of the object to 0 (1 for scale)

    :arg obj: The object
    :type onj : Object(ID)
    """
    obj.location = [0,0,0]
    obj.rotation_quaternion = [1,0,0,0]
    obj.rotation_euler = [0,0,0]
    obj.scale = [1,1,1]

classes = (

)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
