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
    planes = [[0 for x in range(max_y)] for y in range(max_x)]

    # put my planes in the array
    for obj in bpy.data.objects:
        x = int(obj.location.x / plane_size)
        y = int(obj.location.y / plane_size)
        planes[x][y] = obj

    return planes


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
        cam_z = -((max_x + 2) * 2)
    else:
        cam_z = -cam_distance

    # position the camera so (0, 0) is in the top left corner
    cam_rotation = (0, math.radians(180), math.radians(180))
    bpy.ops.object.camera_add(location=(cam_x, cam_y, cam_z), rotation=cam_rotation)

    # one light in the middle of each side of the rectangle, at the same distance
    distance_from_planes = 40
    locations = []
    locations.append((-distance_from_planes, max_y * plane_size / 2))
    locations.append((max_x * plane_size / 2, -distance_from_planes))
    locations.append((max_x * plane_size + distance_from_planes, max_y * plane_size / 2))
    locations.append((max_x * plane_size / 2, max_y * plane_size + distance_from_planes))

    light_z = -40
    for location in locations:
        bpy.ops.object.lamp_add(type='AREA', location=(location[0], location[1], light_z), rotation=cam_rotation)

    return planes
