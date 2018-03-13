import math
import os
import random

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

# parameters
distance = 10
torus_size = 1
torus_count = 50
frame_length = 10
light_distance = 9
angle_limit_max = 20
angle_limit_min = -1 * angle_limit_max


def get_circle_x(radius, angle):
    return radius * math.cos(angle)


def get_circle_y(radius, angle):
    return radius * math.sin(angle)


def go_around(obj, begin, end, radius, direction):
    length = end - begin + 1
    for i in range(begin, end):
        degree = (i - begin) * (360 / length)
        if i % 5 == 0:
            insert_location_keyframe(obj, i)
            insert_rotation_keyframe(obj, i)

            x = get_circle_x(radius, math.radians(degree))
            y = get_circle_y(radius, math.radians(degree))
            obj.location[0] = x * 1.5
            obj.location[2] = direction * y * 1.5

            insert_location_keyframe(obj, i + 10)
            insert_rotation_keyframe(obj, i + 10)


clear_scene()

# world settings
W = bpy.context.scene.world
W.horizon_color = (0, 0, 0)
W.light_settings.use_environment_light = True
W.light_settings.environment_energy = 0.1

# create camera
bpy.ops.object.camera_add(location=(0, -5, 0), rotation=(math.radians(90), 0, 0))
for obj in get_objects('Camera'):
    camera = obj

# create torus and put them in myTorus array
for i in range(0, torus_count):
    bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0))

my_torus = []

i = 0
for obj in get_objects('Torus'):
    my_torus.append(obj)
    obj.name = 'myTorus_' + str(i)
    i += 1

# create materials
colors = []
colors.append(make_material('C1', (51 / 256, 145 / 256, 148 / 256), (1, 1, 1), 1))
colors.append(make_material('C2', (251 / 256, 107 / 256, 65 / 256), (1, 1, 1), 1))
colors.append(make_material('C3', (246 / 256, 216 / 256, 107 / 256), (1, 1, 1), 1))

# rotate torus by 90, change scale and assign color
count = 0

for t in my_torus:
    t.rotation_euler[0] = math.radians(90)
    t.scale = (torus_size, torus_size, torus_size * 2)

    set_material(t, colors[count])
    if count < len(colors) - 1:
        count += 1
    else:
        count = 0

# move and rotate torus
pos_x = 0
pos_y = 0
pos_z = 0
angle1 = 0
angle2 = 0
sign1 = 1
sign2 = 1

for t in my_torus:
    delta1 = random.randint(3, 6) * sign1
    delta2 = random.randint(3, 6) * sign2
    angle1 += delta1
    angle2 += delta2

    t.rotation_euler[1] = math.radians(angle1)
    t.rotation_euler[2] = math.radians(angle2)

    t.location[0] = pos_x - distance * math.sin(math.radians(delta1))
    t.location[1] = pos_y + distance * math.cos(math.radians(delta1))
    t.location[2] = pos_z + torus_size * math.sin(math.radians(delta2))

    pos_x = t.location[0]
    pos_y = t.location[1]
    pos_z = t.location[2]

    # change sign randomly
    if random.randint(0, 10) == 0:
        sign1 *= -1

    if random.randint(0, 10) == 0:
        sign2 *= -1

    # sometimes, create a big delta
    if random.randint(0, 30) == 0:
        delta1 = random.randint(7, 10) * sign1

    if random.randint(0, 30) == 0:
        delta1 = random.randint(7, 10) * sign1

    # limit angle variation
    if angle1 >= angle_limit_max:
        sign1 = -1
    if angle1 <= angle_limit_min:
        sign1 = 1

    if angle2 >= angle_limit_max:
        sign2 = -1
    if angle2 <= angle_limit_min:
        sign2 = 1

# bigger wire torus
material = make_material('C4', (255 / 256, 45 / 256, 48 / 256), (1, 1, 1), 1)
material.type = 'HALO'
material.alpha = 0.2

big_torus_rate = 3

for i in range(0, int(math.floor(torus_count / big_torus_rate))):
    bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0))

big_torus = []

i = 0
for obj in get_objects('Torus'):
    big_torus.append(obj)
    obj.name = 'bigTorus_' + str(i)
    set_material(obj, material)
    i += 1

count = 0
for t in big_torus:
    model = my_torus[count * big_torus_rate]
    t.scale = (torus_size * 5, torus_size * 5, torus_size * 5)
    t.location = model.location
    t.rotation_euler = model.rotation_euler
    count += 1

# create lights
light_counts = 0
for t in my_torus:
    if light_counts % 3 == 0:
        bpy.ops.object.lamp_add(type='POINT', location=(0, t.location[1], light_distance))

    light_counts += 1

# place lights in array and change settings
my_lights = []
for obj in get_objects('Point'):
    my_lights.append(obj)
    obj.data.energy = 15
    obj.data.shadow_method = 'RAY_SHADOW'

# init camera animation
insert_location_keyframe(camera, 0)
insert_rotation_keyframe(camera, 0)

bpy.context.scene.frame_current = 0
bpy.context.scene.frame_end = frame_length * torus_count

# animate camera (synchronize position and rotation with tunnel)
frame_count = 0
count = 2
for t in my_torus:
    camera.location = t.location
    camera.rotation_euler = t.rotation_euler

    insert_location_keyframe(camera, frame_count)
    insert_rotation_keyframe(camera, frame_count)

    frame_count += frame_length

# animate torus scale
shift = 2
frame_count = 0
final_scale = torus_size * 2.5
for i in range(shift, len(my_torus)):
    t = my_torus[i]
    # insert_scale_keyframe(t, frame_count)
    t.keyframe_insert('scale', index=0, frame=frame_count)
    t.keyframe_insert('scale', index=1, frame=frame_count)
    t.keyframe_insert('scale', index=2, frame=frame_count)

    t.scale = (final_scale, final_scale, final_scale)

    # insert_scale_keyframe(t, frame_count + frame_length * random.randint(1, 4) / 3)
    t.keyframe_insert('scale', index=0, frame=frame_count + frame_length * random.randint(1, 4) / 3)
    t.keyframe_insert('scale', index=1, frame=frame_count + frame_length * random.randint(1, 4) / 3)
    t.keyframe_insert('scale', index=2, frame=frame_count + frame_length * random.randint(1, 4) / 3)

    frame_count += frame_length

# animate big torus rotation
sign = 1
frame_count = 0
for t in big_torus:
    sign = sign * -1
    frame_count = 0
    while frame_count <= frame_length * torus_count:
        t.keyframe_insert('rotation_euler', index=1, frame=frame_count)
        t.rotation_euler[1] += sign * math.radians(15)
        t.keyframe_insert('rotation_euler', index=1, frame=frame_count + frame_length)
        frame_count += frame_length

# animate lights
nbr_tours = 15
tour_length = (frame_length * torus_count) / nbr_tours
count = 0

for l in my_lights:
    count += 1
    if count % 2 == 0:
        direction = 1
    else:
        direction = -1

    for i in range(nbr_tours):
        begin_anim = i * int(tour_length)
        end_anim = (i + 1) * int(tour_length)

        go_around(l, begin_anim, end_anim, light_distance, direction)
