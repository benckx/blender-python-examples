import bpy


def create_planes(max_x, max_y, size):
    # create planes
    for x in range(max_x):
        for y in range(max_y):
            bpy.ops.mesh.primitive_plane_add(location=(x * size, y * size, 0))

    # 2 dimensional array
    my_planes = [[0 for j in range(max_y)] for tho in range(max_x)]

    # put my planes in the array
    for o in bpy.data.objects:
        o.select = False
        x = int(o.location[0] / size)
        y = int(o.location[1] / size)
        my_planes[x][y] = o

    return my_planes
