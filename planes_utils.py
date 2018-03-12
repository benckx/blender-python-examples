import bpy

# load modules for IDE
try:
    from utils import *
except:
    pass


def create_planes(max_x, max_y, plane_size):
    # create planes
    for x in range(max_x):
        for y in range(max_y):
            bpy.ops.mesh.primitive_plane_add(location=(x * plane_size, y * plane_size, 0))

    # 2 dimensional array
    my_planes = [[0 for x in range(max_x)] for y in range(max_y)]

    # put my planes in the array
    for obj in bpy.data.objects:
        x = int(obj.location.x / plane_size)
        y = int(obj.location.y / plane_size)
        my_planes[x][y] = obj

    return my_planes


def init_basic_planes_scene(max_x, max_y, plane_size, cam_distance=None):
    clear_scene()
    set_render_resolution((max_x - 2) * 100, (max_y - 2) * 100)

    planes = create_planes(max_x, max_y, plane_size)

    material = make_red()
    for x in range(max_x):
        for y in range(max_y):
            plane = planes[x][y]
            set_material(plane, material)

    # create camera
    cam_x = max_x - plane_size / 2
    cam_y = max_y - plane_size / 2
    if cam_distance is None:
        cam_z = -(max_x * 2)
    else:
        cam_z = -cam_distance

    # position the camera so (0, 0) is in the top left corner
    cam_rotation = (0, math.radians(180), math.radians(180))
    bpy.ops.object.camera_add(location=(cam_x, cam_y, cam_z), rotation=cam_rotation)

    # create light
    margin = max_x * 5
    x_border = max_x * 2
    y_border = max_y * 2
    light_z = -30

    # x
    bpy.ops.object.lamp_add(type='AREA', location=(cam_x, -margin, light_z), rotation=cam_rotation)
    bpy.ops.object.lamp_add(type='AREA', location=(cam_x, margin + y_border, light_z), rotation=cam_rotation)

    # y
    bpy.ops.object.lamp_add(type='AREA', location=(-margin, cam_y, light_z), rotation=cam_rotation)
    bpy.ops.object.lamp_add(type='AREA', location=(margin + x_border, cam_y, light_z), rotation=cam_rotation)

    return planes
