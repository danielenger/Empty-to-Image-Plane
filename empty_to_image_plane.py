import bpy


def get_image_by_filepath(filepath):
    """find image by filepath"""

    for img in bpy.data.images.values():
        if img.filepath == filepath:
            return img


def image_plane_at_image_emtpy(empty, prefix="Image Plane"):
    """add image plane at given empty"""

    if not empty.data:
        return
    else:
        if not empty.data.filepath:
            return
        else:
            img = get_image_by_filepath(empty.data.filepath)

    cursor = bpy.context.scene.cursor
    cursor.location = (0, 0, 0)

    bpy.ops.mesh.primitive_plane_add(
        size=1, enter_editmode=False, location=(0, 0, 0))
    plane = bpy.context.object

    x = img.size[0] / 2000
    y = img.size[1] / 2000

    if x <= y:
        plane.scale.x = x / y
    else:
        plane.scale.y = y / x

    lx = plane.location.x
    ly = plane.location.y
    sx = plane.scale.x
    sy = plane.scale.y
    e_offx = empty.empty_image_offset[0]
    e_offy = empty.empty_image_offset[1]

    cursor.location.x = lx - sx / 2 - sx * e_offx
    cursor.location.y = ly - sy / 2 - sy * e_offy

    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # set loc, rot, scale
    plane.location = empty.location
    plane.rotation_euler = empty.rotation_euler
    plane.scale.x = empty.empty_display_size * empty.scale.x
    plane.scale.y = empty.empty_display_size * empty.scale.y

    # material setup
    mat = bpy.data.materials.new(img.name)
    mat.use_nodes = True
    plane.data.materials.append(mat)
    
    mat.node_tree.nodes.clear()
        
        #create the nodes
    mat_output = mat.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
    img_node = mat.node_tree.nodes.new(type="ShaderNodeTexImage")
    emit_node = mat.node_tree.nodes.new(type='ShaderNodeEmission')
    invert_node = mat.node_tree.nodes.new(type='ShaderNodeInvert')
    transparent_node = mat.node_tree.nodes.new(type='ShaderNodeBsdfTransparent')
    mix_node = mat.node_tree.nodes.new(type='ShaderNodeMixShader')
    
        #create the links    
    mat.node_tree.links.new(img_node.outputs['Color'], emit_node.inputs['Color'])
    mat.node_tree.links.new(emit_node.outputs[0], mix_node.inputs[1])
    mat.node_tree.links.new(img_node.outputs['Alpha'], invert_node.inputs['Color'])
    mat.node_tree.links.new(invert_node.outputs['Color'], mix_node.inputs['Fac'])
    mat.node_tree.links.new(transparent_node.outputs[0], mix_node.inputs[2])
    mat.node_tree.links.new(mix_node.outputs[0], mat_output.inputs['Surface'])
    
        #make the transparent areas transparent in the viewport
    mat.blend_method = 'CLIP'
    
        #node positionning
    img_node.image = img
    img_node.location.x = -700
    invert_node.location.x = -400
    invert_node.location.y = 150
    emit_node.location.x = -400
    transparent_node.location.x = -400
    transparent_node.location.y = -150
    mix_node.location.x = -200    

    plane.name = prefix + img.name

    return True


class EMPTPYTOIMAGEPLANE_PT_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Empty to Image Plane"
    bl_context = "objectmode"
    bl_category = "Empty to Image Plane"

    def draw(self, context):
        self.layout.operator('object.add_planes')


class EMPTPYTOIMAGEPLANE_OT_add_planes(bpy.types.Operator):
    bl_idname = "object.add_planes"
    bl_label = "Add Image Planes"
    bl_description = "Add an Image Plane at every (selected) Image Empty"
    bl_options = {'REGISTER', 'UNDO'}

    bool_selected: bpy.props.BoolProperty(
        name="Selected Image Empty", default=True)

    prefix: bpy.props.StringProperty(
        name="Prefix", default="Image Plane ")

    def execute(self, context):

        cx, cy, cz = bpy.context.scene.cursor.location

        if self.bool_selected:
            objects = bpy.context.selected_objects
        else:
            objects = bpy.data.objects.values()

        for obj in objects:
            if obj.type == 'EMPTY':
                if obj.empty_display_type == 'IMAGE':
                    if not image_plane_at_image_emtpy(obj, self.prefix):
                        self.report(
                            {'INFO'}, "No Image in '{0}'".format(obj.name))

        bpy.context.scene.cursor.location = (cx, cy, cz)

        return {'FINISHED'}
