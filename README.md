## About
Simple examples of Blender animations based on Python scripts.

## How to
Open in Blender: `blender --python the_script.py`

Convert to GIF: `convert -delay 4 -loop 0 *.png animation.gif`

Make a video: `ffmpeg -framerate 30 -f image2 -i '/tmp/%*.png' -c:v libx264 -profile:v high -crf 16 -pix_fmt yuv420p blender_render.mp4`

## Scripts
##### [trippy_tunnel.py](trippy_tunnel.py)
![](images/trippy.gif)

##### [planes_rotation_x_axis.py](planes_rotation_x_axis.py)
![](images/x_axis.gif)

##### [planes_rotation_z_axis.py](planes_rotation_z_axis.py)
![](images/z_axis.gif)

##### [planes_rotations_xz.py](planes_rotations_xz.py)
![](images/xz.gif)