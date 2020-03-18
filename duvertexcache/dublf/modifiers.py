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

# Modifiers tools and methods

def collect_modifiers( obj, modifier_type = 'SUBSURF', remove = False):
    """
    Collects all modifiers of a given type from an object.

    :arg obj: The object to get the modifiers from.
    :type obj: Object(ID)
    :arg modifier_type: The type of modifier to get.
    :type modifier_type: enum in [‘DATA_TRANSFER’, ‘MESH_CACHE’, ‘MESH_SEQUENCE_CACHE’, ‘NORMAL_EDIT’, ‘WEIGHTED_NORMAL’, ‘UV_PROJECT’, ‘UV_WARP’, ‘VERTEX_WEIGHT_EDIT’, ‘VERTEX_WEIGHT_MIX’, ‘VERTEX_WEIGHT_PROXIMITY’, ‘ARRAY’, ‘BEVEL’, ‘BOOLEAN’, ‘BUILD’, ‘DECIMATE’, ‘EDGE_SPLIT’, ‘MASK’, ‘MIRROR’, ‘MULTIRES’, ‘REMESH’, ‘SCREW’, ‘SKIN’, ‘SOLIDIFY’, ‘SUBSURF’, ‘TRIANGULATE’, ‘WIREFRAME’, ‘WELD’, ‘ARMATURE’, ‘CAST’, ‘CURVE’, ‘DISPLACE’, ‘HOOK’, ‘LAPLACIANDEFORM’, ‘LATTICE’, ‘MESH_DEFORM’, ‘SHRINKWRAP’, ‘SIMPLE_DEFORM’, ‘SMOOTH’, ‘CORRECTIVE_SMOOTH’, ‘LAPLACIANSMOOTH’, ‘SURFACE_DEFORM’, ‘WARP’, ‘WAVE’, ‘CLOTH’, ‘COLLISION’, ‘DYNAMIC_PAINT’, ‘EXPLODE’, ‘OCEAN’, ‘PARTICLE_INSTANCE’, ‘PARTICLE_SYSTEM’, ‘FLUID’, ‘SOFT_BODY’, ‘SURFACE’]
    :arg remove: Removes the collected modifier from the object
    :type remove: bool
    :return: The list of modifiers.
    :rtype: Modifier[] if remove is False, dict[] if remove is True, each dict containing a copy of the origianl Modifier attributes
    """
    # Collect and remove
    modifiers = []
    for mod in reversed(obj.modifiers):
        if mod.type == modifier_type:
            if remove:
                backupMod = {}
                for attr in dir(mod):
                    backupMod[attr] = getattr(mod, attr)
                modifiers.append(backupMod)
                obj.modifiers.remove(mod)
            else:
                modifiers.append(mod)
    return modifiers

def remove_all_modifiers(obj, modifier_type=''):
        """
	    Removes all modifiers from an object.
	
	    :arg obj: The object to remove the modifiers from.
	    :type obj: Object(ID)
	    :arg modifier_type: The type of modifier to remove. All of them if ''
	    :type modifier_type: enum in [‘DATA_TRANSFER’, ‘MESH_CACHE’, ‘MESH_SEQUENCE_CACHE’, ‘NORMAL_EDIT’, ‘WEIGHTED_NORMAL’, ‘UV_PROJECT’, ‘UV_WARP’, ‘VERTEX_WEIGHT_EDIT’, ‘VERTEX_WEIGHT_MIX’, ‘VERTEX_WEIGHT_PROXIMITY’, ‘ARRAY’, ‘BEVEL’, ‘BOOLEAN’, ‘BUILD’, ‘DECIMATE’, ‘EDGE_SPLIT’, ‘MASK’, ‘MIRROR’, ‘MULTIRES’, ‘REMESH’, ‘SCREW’, ‘SKIN’, ‘SOLIDIFY’, ‘SUBSURF’, ‘TRIANGULATE’, ‘WIREFRAME’, ‘WELD’, ‘ARMATURE’, ‘CAST’, ‘CURVE’, ‘DISPLACE’, ‘HOOK’, ‘LAPLACIANDEFORM’, ‘LATTICE’, ‘MESH_DEFORM’, ‘SHRINKWRAP’, ‘SIMPLE_DEFORM’, ‘SMOOTH’, ‘CORRECTIVE_SMOOTH’, ‘LAPLACIANSMOOTH’, ‘SURFACE_DEFORM’, ‘WARP’, ‘WAVE’, ‘CLOTH’, ‘COLLISION’, ‘DYNAMIC_PAINT’, ‘EXPLODE’, ‘OCEAN’, ‘PARTICLE_INSTANCE’, ‘PARTICLE_SYSTEM’, ‘FLUID’, ‘SOFT_BODY’, ‘SURFACE’]
	    """
        for mod in reversed(obj.modifiers):
            if modifier_type == '' or modifier_type == mod.type:
                obj.modifiers.remove( mod )
  
class DUBLF_OT_modifiers_remove_all( bpy.types.Operator ):
    """Removes all modifiers from the active object"""
    bl_idname = "object.modifiers_remove_all"
    bl_label = "Remove all modifiers"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(self, context):
        return context.active_object is not None

    def execute( self, context ):
        remove_all_modifiers(context.active_object)
        return {'FINISHED'}

class DUBLF_OT_modifiers_apply_all( bpy.types.Operator) :
    """Applies all modifiers on the current object"""
    bl_idname = "object.modifiers_apply_all"
    bl_label = "Apply all modifiers"
    bl_options = {'REGISTER','UNDO'}

    apply_as: bpy.props.EnumProperty(
        name="Apply as",
        description="How to apply the modifier to the geometry",
        items=(
            ('DATA', "Data", "Object Data, Apply modifier to the object’s data."),
            ('SHAPE', "New Shape Key", "Apply deform-only modifier to a new shape on this object.",)
            ),
            default='DATA'
        )

    @classmethod
    def poll(self, context):
        return context.active_object is not None

    def execute( self, context ):
        oc = context.copy()
        for mod in context.object.modifiers:
            bpy.ops.object.modifier_apply(oc, apply_as=self.apply_as, modifier=mod.name)
        return {'FINISHED'}

classes = (
    DUBLF_OT_modifiers_remove_all,
    DUBLF_OT_modifiers_apply_all,
)

def register():
    # register
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    # unregister
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
