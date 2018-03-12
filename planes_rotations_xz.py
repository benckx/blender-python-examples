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

planes = init_basic_planes_scene(max_x, max_y, plane_size)

# animate
frame_end = 400
frame_begin = frame_end * 0.1
bpy.context.scene.frame_end = frame_end

for x in range(max_x):
    for y in range(max_y):
        plane = planes[x][y]
        add_rotation(plane, 'x', 360, frame_begin, frame_end)
        add_rotation(plane, 'z', 180, frame_begin, frame_end)
