import json
from timeit import default_timer as timer
import matplotlib
matplotlib.use("Agg")
from matplotlib.pylab import imshow, jet, savefig, ion
import numpy as np
from numba import jit
from argparse

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
    #load config.json
    config = json.load(open('config.json'))
    image = np.zeros((500 * 2, 750 * 2), dtype=np.uint8)
    s = timer()
    create_fractal(config['min_x'], config['max_x'], config['min_y'], config['max_y'], image, config['iters'])
    e = timer()
    print(e - s)
    imshow(image)
    #jet()
    #ion()
    savefig('fractal.png')