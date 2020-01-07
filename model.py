import os
import sys
from multiprocessing import cpu_count

import matplotlib
# set matplotlib to headless mode
matplotlib.use("Agg")
import json
from timeit import default_timer as timer
from matplotlib.pylab import imshow, jet, savefig, ion
import numpy as np
from numba import jit

# adapted from https://numba.pydata.org/numba-doc/dev/user/examples.html

@jit
def mandel(x, y, max_iters):
    """
    Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the Mandelbrot
    set given a fixed number of iterations.
    """
    i = 0
    c = complex(x,y)
    z = 0.0j
    for i in range(max_iters):
        z = z*z + c
        if (z.real*z.real + z.imag*z.imag) >= 4:
            return i

    return 255

@jit
def create_fractal(min_x, max_x, min_y, max_y, image, iters):
    height = image.shape[0]
    width = image.shape[1]

    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height
    for x in range(width):
        real = min_x + x * pixel_size_x
        for y in range(height):
            imag = min_y + y * pixel_size_y
            color = mandel(real, imag, iters)
            image[y, x] = color

    return image

if __name__ == '__main__':
    # print some debugging info
    print('Python Version: ' + sys.version)
    print('Platform: ' + sys.platform)
    print('CPU Count: ' + cpu_count())
    print ('Environment: ')
    print(str(dict(os.environ)))
    #load config.json
    config = json.load(open('config.json'))
    print('Config: ' + config)
    image = np.zeros((500 * 2, 750 * 2), dtype=np.uint8)
    s = timer()
    print("Creating Fractal")
    create_fractal(config['min_x'], config['max_x'], config['min_y'], config['max_y'], image, config['iters'])
    e = timer()
    print(e - s)
    imshow(image)
    #jet()
    #ion()
    print("Saving image")
    savefig('fractal.png')
