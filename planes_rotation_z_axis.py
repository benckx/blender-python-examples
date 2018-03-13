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

max_x = 6
max_y = 6
plane_size = 2

planes = init_basic_planes_scene(max_x, max_y, plane_size)

# animate
frame_begin = 0
frame_end = 20
bpy.context.scene.frame_end = frame_end

i = 0
for x in range(max_x):
    for y in range(max_y):
        plane = planes[x][y]
        add_rotation(plane, 'z', 90, frame_begin, frame_end)
