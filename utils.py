import math

import bpy


def set_render_resolution(x, y):
    bpy.data.scenes[0].render.resolution_x = x * 2
    bpy.data.scenes[0].render.resolution_y = y * 2


# found on http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Materials_and_textures
def make_material(name, diffuse, specular, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT'
    mat.diffuse_intensity = 1.0
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 1
    return mat


def make_red():
    return make_material('Red', (1, 0, 0), (1, 1, 1), 1)


def make_blue():
    return make_material('BlueSemi', (0, 0, 1), (0.5, 0.5, 0), 0.5)


def set_material(obj, mat):
    if obj.data.materials:
        # assign to 1st material slot
        obj.data.materials[0] = mat
    else:
        # no slots
        obj.data.materials.append(mat)


def get_objects(prefix):
    result = []
    for o in bpy.data.objects:
        if o.name.startswith(prefix):
            result.append(o)

    return result


# clear all existing objects (Cube, Lamp, Camera)
def clear_scene():
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        obj.select = True

    bpy.ops.object.delete()


def insert_keyframe(obj, data_path, frame):
    for i in range(3):
        obj.keyframe_insert(data_path, index=i, frame=frame)


def insert_location_keyframe(obj, frame):
    insert_keyframe(obj, 'location', frame)


def insert_rotation_keyframe(obj, frame):
    insert_keyframe(obj, 'rotation_euler', frame)


def insert_scale_keyframe(obj, frame):
    insert_keyframe(obj, 'scale', frame)


def add_rotation(obj, axis, angle, frame_begin, frame_end):
    axis_int = ['x', 'y', 'z'].index(axis)
    obj.keyframe_insert('rotation_euler', index=axis_int, frame=frame_begin)
    obj.rotation_euler[axis_int] = math.radians(angle)
    obj.keyframe_insert('rotation_euler', index=axis_int, frame=frame_end)
