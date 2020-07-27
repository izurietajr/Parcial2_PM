#!/usr/bin/env python3
import matplotlib.image as plt_img
import numpy as np
from PIL import Image as pil_image
from functools import reduce
from math import sqrt
from copy import deepcopy


class Image:

    def __init__(self):
        self.route = "."
        self.image = None
        self.array = None
        self.height, self.width, self.dat = (0,0,0)

    def load_file(self, route):
        self.route = route
        self.image = plt_img.imread(route)
        self.array = self.image.tolist()
        self.height, self.width, self.dat = self.image.shape

    def load_array(self, array):
        self.array = array
        self.height = len(array)
        self.width = len(array[0])

    def I(self, x, y):
        """ Devuelve rgb en x, y """
        return tuple(self.array[x][y])

    def I_m(self, x, y, color=0):
        """ Devuelve un color de x, y """
        triple = self.array[x][y]
        return triple[color]

    def I_normal(self, x, y):
        """ Devuelve rgb en [0, 1] """
        (i, j, k) = self.I(x, y)
        return (i/255, j/255, k/255)

    def I_mnormal(self, x, y, color=0):
        """ Devuelve color en [0, 1] """
        i = self.I_m(x, y, color)
        return i/255

    def show(self, route=None):
        if route:
            self.route = route
        image_arr = np.asarray(self.array, dtype="uint8")
        img_file = pil_image.fromarray(image_arr, 'RGB')
        return img_file

    def iterator(self):
        for i in range(self.height):
            for j in range(self.width):
                yield (i,j)

    def map_over(self, func):
        """ Ejecución de func sobre cada pixel """
        for x, y in self.iterator():
            self.array[x][y] = func(*self.I(x, y))

    def copy(self):
        return deepcopy(self)

    def crop(self, x1, y1, x2, y2):
        cropped_array = []
        for i in range(y1, y2):
            arr = []
            for j in range(x1, x2):
                arr.append(self.I(i, j))
            cropped_array.append(arr)
        cropped_image = Image()
        cropped_image.load_array(cropped_array)
        return cropped_image

    def black_white(self):
        self.map_over(lambda r, g, b: (min(r, g, b), min(r, g, b), min(r, g, b)))
        return self

    def binarize(self, center):
        bound = lambda x: 255 if x > center else 0
        self.map_over(lambda r, g, b: (bound(b), bound(b), bound(b)))
        return self

    def hu_moments(self):
        """ Primeros dos momentos de Hu """
        def moment_pq(p, q):
            """ Momentos geométricos """
            sum = 0
            for x, y in self.iterator():
                sum += x**p * y**q * self.I_mnormal(x, y)
            return sum

        m00 = moment_pq(0, 0)
        m01 = moment_pq(0, 1)
        m11 = moment_pq(1, 1)
        m10 = moment_pq(1, 0)
        m20 = moment_pq(2, 0)
        m02 = moment_pq(0, 2)

        def central_moment_20(a, b, c):
            """ Momentos centrales """
            return (a-(b**2/c))/(c**2)

        n20 = central_moment_20(m20, m10, m00)
        n02 = central_moment_20(m02, m01, m00)
        n11 = central_moment_20(m11, sqrt(m10*m01), m00)

        self.X, self.Y = (n20+n02, (n20-n02)**2+4*(n11**2))

        return (self.X, self.Y)

    def histogram(self):
        # hist = [(x, 0) for x in range(255)]
        hist = [0 for _ in range(256)]
        for x, y in self.iterator():
            pixel = self.I_m(x, y)
            print(pixel)
            hist[pixel] += 1
        return hist


        pass

    def otsu(self):
        pass
