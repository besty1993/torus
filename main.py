import math
import time

from render import Render
from object3d import Torus

class TORUS_CFG:
    R = 2
    r = 1
    center = [1, 0.5, 0.7]
    density = 200

class RENDER_CFG:
    light_vector = [1, 1, 1]
    window_size = (70,35)


if __name__ == '__main__':
    torus = Torus(
        R=TORUS_CFG.R,
        r=TORUS_CFG.r,
        center=TORUS_CFG.center,
        density=TORUS_CFG.density
    )
    points, norm_vectors = torus()

    renderer = Render(
        light_vector=RENDER_CFG.light_vector,
        window_size=RENDER_CFG.window_size
    )

    for t in range(100):
        rot_x = t*2*math.pi/10
        rot_y = t*2*math.pi/50
        rot_z = 0

        rot_points = renderer.rotate(points, rot_x, rot_y, rot_z)
        rot_norms = renderer.rotate(norm_vectors, rot_x, rot_y, rot_z)

        print(renderer(rot_points, rot_norms))
        time.sleep(0.1)