import math
import os

import bpy

# load modules for IDE
try:
    from utils import *
    from planes_utils import *
except:
    pass

# load modules dynamically for Blender
directory = os.path.basename(bpy.data.filepath)
files_names = ['utils.py', 'planes_utils.py']

for file_name in files_names:
    file_path = os.path.join(directory, file_name)
    exec(compile(open(file_path).read(), file_path, 'exec'))

max_x = 8
max_y = 8
plane_size = 2

set_render_resolution(600, 600)
frame_end = 400
bpy.context.scene.frame_end = frame_end

clear_scene()

planes = create_planes(max_x, max_y, plane_size)

material = make_red()
for x in range(max_x):
    for y in range(max_y):
        plane = planes[x][y]
        set_material(plane, material)

# create camera
cam_x = max_x - plane_size / 2
cam_y = max_y - plane_size / 2
cam_z = 15
bpy.ops.object.camera_add(location=(cam_x, cam_y, cam_z), rotation=(0, 0, math.radians(90)))

# create light
margin = max_x * 4
x_border = max_x * 2
y_border = max_y * 2
light_z = 30

# x
bpy.ops.object.lamp_add(type='AREA', location=(cam_x, -margin, light_z))
bpy.ops.object.lamp_add(type='AREA', location=(cam_x, margin + y_border, light_z))

# y
bpy.ops.object.lamp_add(type='AREA', location=(-margin, cam_y, light_z))
bpy.ops.object.lamp_add(type='AREA', location=(margin + x_border, cam_y, light_z))

# rotate
frame_begin = frame_end * 0.1
for x in range(max_x):
    for y in range(max_y):
        plane = planes[x][y]
        add_rotation(plane, 'y', 360, frame_begin, frame_end)
        add_rotation(plane, 'z', 180, frame_begin, frame_end)
