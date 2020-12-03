import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st
import time

from PIL import Image
from scipy.linalg import eigvals
from scipy.ndimage import sobel
from sklearn.covariance import LedoitWolf
from tqdm import tqdm


#################################################
class Region:
    def __init__(self, vertex0, vertex1, parent):
        # Save information
        self.vertex0 = vertex0
        self.vertex1 = vertex1
        self.vertex1n = (vertex1[0] + 1, vertex1[1] + 1)
        self.parent = parent

        # Lazily instantiate parameters
        self.matrix = None
        self.c1 = None
        self.c2 = None
        self.c3 = None
        self.c4 = None
        self.c5 = None

    # Partition image in two
    def half_image(self, horizontal=True):
        # Create regions
        if horizontal:
            partition = int((self.vertex1[1] + self.vertex0[1]) / 2)

            vertex1 = (self.vertex1[0], partition - 1)
            first = Region(self.vertex0, vertex1, self.parent)

            vertex0 = (self.vertex0[0], partition)
            second = Region(vertex0, self.vertex1, self.parent)
        else:
            partition = int((self.vertex1[0] + self.vertex0[0]) / 2)

            vertex1 = (partition - 1, self.vertex1[1])
            first = Region(self.vertex0, vertex1, self.parent)

            vertex0 = (partition, self.vertex0[1])
            second = Region(vertex0, self.vertex1, self.parent)

        return first, second

    # Get rectangular patch
    def get_patch(self, index):
        if index == 0:
            color = 'w'
        elif index == 1:
            color = 'b'
        else:
            color = 'r'

        vertex1 = self.vertex1[::-1]
        vertex0 = self.vertex0[::-1]

        width = vertex1[0] - vertex0[0]
        height = vertex1[1] - vertex0[1]

        return patches.Rectangle(vertex0, width, height, fill=False,
                                 edgecolor=color, linewidth=2)

    # Create feature matrix
    def create_matrix(self):
        self.matrix = []
        parent_matrix = self.parent.get_matrix()
        for x in range(self.vertex0[0], self.vertex1n[0]):
            for y in range(self.vertex0[1], self.vertex1n[1]):
                self.matrix.append(parent_matrix[:, x, y].copy())

                # Transform coordinates
                x_t = x - self.vertex0[0]
                y_t = y - self.vertex0[1]

                self.matrix[-1][:2] = [y_t, x_t]

        self.matrix = np.array(self.matrix)

    def create_derivatives(self):
        intensity = self.get_intensity()

        # First derivative
        self.der_imagex = sobel(intensity, axis=1)
        self.der_imagey = sobel(intensity, axis=0)

        # Second derivative
        self.der2_imagex = sobel(self.der_imagex, axis=1)
        self.der2_imagey = sobel(self.der_imagey, axis=0)

    # Get feature matrix
    def get_matrix(self):
        if self.matrix is None:
            self.create_matrix()

        return self.matrix

    # Calculate and store c1
    def create_c1(self, cov):
        self.c1 = cov.fetch(self.get_matrix())

    def get_c1(self, cov):
        if self.c1 is None:
            self.create_c1(cov)

        return self.c1

    # Calculate and store c2, c3
    def create_c2_c3(self, cov):
        left, right = self.half_image()

        self.c2 = left.get_c1(cov)
        self.c3 = right.get_c1(cov)

    def get_c2_c3(self, cov):
        if self.c2 is None:
            self.create_c2_c3(cov)

        return self.c2, self.c3

    # Calculate and store c4, c5
    def create_c4_c5(self, cov):
        up, down = self.half_image(horizontal=False)

        self.c4 = up.get_c1(cov)
        self.c5 = down.get_c1(cov)

    def get_c4_c5(self, cov):
        if self.c4 is None:
            self.create_c4_c5(cov)

        return self.c4, self.c5

#################################################
class ImageHandler:
    def __init__(self, directory):
        self.image = Image.open(directory)
        self.directory = directory

        # Modes for the image
        self.intensity = None
        self.rgb = None
        self.hsv = None

        # Derivative information
        self.der_imagex = None
        self.der_imagey = None
        self.der2_imagex = None
        self.der2_imagey = None

        # Features
        self.matrix = None

        # Regions information
        self.regions = []

    # Calculates derivatives of an image
    def create_derivatives(self):
        intensity = self.get_intensity()

        # First derivative
        self.der_imagex = sobel(intensity, axis=1)
        self.der_imagey = sobel(intensity, axis=0)

        # Second derivative
        self.der2_imagex = sobel(self.der_imagex, axis=1)
        self.der2_imagey = sobel(self.der_imagey, axis=0)

    # Creates RGB array
    def create_rgb(self):
        self.rgb = np.array(self.image.convert("RGB"))

    # Creates intensity array
    def create_intensity(self):
        self.intensity = np.array(self.image.convert("L"))

    def create_hsv(self):
        self.hsv = np.array(self.image.convert("HSV"))

    # Calculate matrix of features
    def create_matrix(self):
        intensity = self.get_intensity()
        self.matrix = np.zeros((9, intensity.shape[0], intensity.shape[1]))
        for x in range(intensity.shape[0]):
            for y in range(intensity.shape[1]):
                self.matrix[:, x, y] = self.pixel_feature(x, y)[:, 0]

    # Calculates the feature for a pixel given it's position in the array
    def pixel_feature(self, pos_x, pos_y):
        if self.der_imagex is None:
            self.create_derivatives()

        rgb = self.get_rgb()
        f_xy = np.zeros((9, 1))

        f_xy[0, 0] = pos_y
        f_xy[1, 0] = pos_x

        f_xy[2:5, 0] = rgb[pos_x, pos_y, :]

        f_xy[5, 0] = np.abs(self.der_imagex[pos_x, pos_y])
        f_xy[6, 0] = np.abs(self.der_imagey[pos_x, pos_y])

        f_xy[7, 0] = np.abs(self.der2_imagex[pos_x, pos_y])
        f_xy[8, 0] = np.abs(self.der2_imagey[pos_x, pos_y])

        return f_xy

    # Adds a region to the regions
    def add_region(self, vertex0, vertex1):
        self.regions.append(Region(vertex0, vertex1, self))

    # Read regions from a file generates by export_regions
    def read_info(self, directory=None):
        if directory is None:
            new_directory = self.directory.split(".")[0]
            directory = new_directory + ".imgh"

        file = open(directory, "r").readlines()
        for line in file:
            vertex0, vertex1 = line.split("\t")
            vertex0 = vertex0[1:-1]
            vertex1 = vertex1[1:-2]
            vertex0 = tuple(map(int, vertex0.split(', ')))
            vertex1 = tuple(map(int, vertex1.split(', ')))
            self.add_region(vertex0[::-1], vertex1[::-1])

    # Getters
    def get_matrix(self):
        if self.matrix is None:
            self.create_matrix()

        return self.matrix

    def get_rgb(self):
        if self.rgb is None:
            self.create_rgb()

        return self.rgb

    def get_intensity(self):
        if self.intensity is None:
            self.create_intensity()

        return self.intensity

    def get_hsv(self):
        if self.hsv is None:
            self.create_hsv()

        return self.hsv

    # Array of square for given scale
    def get_regions(self, region, scale, index):
        rgb = self.get_rgb()

        # Calculate width and height
        vertex0 = region.vertex0
        vertex1 = region.vertex1

        width = int(scale*(vertex1[0] - vertex0[0]))
        height = int(scale*(vertex1[1] -  vertex0[1]))

        if width == 0 or height == 0:
            return

        # Find all regions
        step = int(1.15 ** index * 3)
        locations = []
        for x in range(0, rgb.shape[0], step):
            if x + width >= rgb.shape[0]:
                break
            for y in range(0, rgb.shape[1], step):
                if y + height >= rgb.shape[1]:
                    break
                vertex1 = (x, y)
                vertex2 = (x+width, y+height)
                region_aux = Region(vertex1, vertex2, self)
                locations.append(region_aux)

        for x in range(0, rgb.shape[0], step):
            if x + height >= rgb.shape[0]:
                break
            for y in range(0, rgb.shape[1], step):
                if y + width >= rgb.shape[1]:
                    break
                vertex1 = (x, y)
                vertex2 = (x+height, y+width)
                region_aux = Region(vertex1, vertex2, self)
                locations.append(region_aux)
        return locations

    # Show image in pyplot
    def show(self, output_dir="", rect=False):
        rgb = self.get_rgb()
        _, ax = plt.subplots(1)
        ax.imshow(rgb)

        # Draw selected regions
        if rect:
            index = 0
            for region in self.regions:
                rectangle = region.get_patch(index)
                ax.add_patch(rectangle)
                index += 1

        if len(output_dir) > 0:
            plt.savefig(output_dir, bbox_inches='tight')
            plt.clf()
        else:
            plt.show()


#################################################
class Cov:
    def __init__(self, method):
        self.method = method

    def fetch(self, sample):
        if self.method == 0:
            return np.cov(sample.transpose())
        elif self.method == 1:
            return Cov.calculate_com(sample)
        elif self.method == 2:
            return Cov.calculate_spearman(sample)
        elif self.method == 3:
            return Cov.calculate_kendall(sample)
        else:
            return Cov.calculate_cov_shrinkages(sample)

    # Calculate comedian matrix
    @staticmethod
    def calculate_com(sample):
        medians = np.quantile(sample, 0.5, axis=0)
        data_sb = sample - medians

        # Pairwise column multiplication
        data_mult = data_sb[..., None] * data_sb[:, None]

        # Comedian
        com = np.quantile(data_mult, 0.5, axis=0)

        return com

    @staticmethod
    def calculate_spearman(sample):
        corrs, _ = st.spearmanr(sample)
        stds = np.reshape(sample.std(axis=0, ddof=1), (-1, 1))

        # Std mat
        std_mat = stds @ stds.T

        return corrs  * std_mat

    @staticmethod
    def calculate_kendall(sample):
        n = sample.shape[0]
        m = sample.shape[1]

        # Method based on matlab implementation
        indexes = np.argwhere(np.tril(np.ones(n), -1))
        i1, i2 = indexes[:, 0], indexes[:, 1]

        tau = np.sign(sample[i2, :] - sample[i1, :])
        aux = tau.T @ tau
        diagonal = np.resize(np.diag(aux), (m, 1))
        corr = aux / np.sqrt(diagonal @ diagonal.T)

        # Std mat
        stds = np.reshape(sample.std(axis=0, ddof=1), (-1, 1))
        std_mat = stds @ stds.T

        return corr * std_mat

    # Calculate covariance of shrinkages
    @staticmethod
    def calculate_cov_shrinkages(sample):
        return LedoitWolf().fit(sample).covariance_

#################################################
class Distance:
    def __init__(self, method=0):
        self.method = method
        self.distances = ['fro', 1, 2, np.inf]

    def fetch(self, c1, c2):
        if self.method == 0:
            return Distance.author_distance(c1, c2)
        elif self.method - 1 in range(len(self.distances)):
            return np.linalg.norm(c2 - c1, ord=self.distances[self.method - 1])
        return 0

    @staticmethod
    def author_distance(c1, c2):
        if np.isnan(c1.sum()) or np.isnan(c2.sum()):
            return np.inf

        eig_vals = eigvals(c1, c2)

        nans = eig_vals[np.isnan(eig_vals)]
        if nans.size > 0:
            d = np.inf
        else:
            try:
                d = np.sqrt((np.log(eig_vals) ** 2).sum())
            except:
                d = np.inf
        return d

#################################################
class ImageProcessor:
    def __init__(self, directory, method=0, method_dist=0):
        self.image = ImageHandler(directory)
        self.image.read_info()
        self.cov = Cov(method)
        self.dist = Distance(method_dist)

        # Scale changes
        scale1 = [0.85 ** j for j in range(4, 0, -1)]
        scale2 = [1.15 ** j for j in range(0, 5)]

        self.scales = np.array(scale1 + scale2)

    # Find object for a defined region
    def process_image_for_region(self, imagep, index_region):
        # Image to process
        region = self.image.regions[index_region]
        c1 = region.get_c1(self.cov)

        # Regions
        index = 0
        locations = []
        for scale in self.scales:
            locations += imagep.get_regions(region, scale, index)
            index += 1

        # 1000 best regions
        key = lambda x: self.dist.fetch(c1, x.get_c1(self.cov))
        best_locations = list(sorted(locations, key=key))[:1000]

        # Covariances
        c2, c3 = region.get_c2_c3(self.cov)
        c4, c5 = region.get_c4_c5(self.cov)

        cs = [c1, c2, c3, c4, c5]

        # Best choice
        min_dis = -1
        min_choice = None
        first = True
        for choice in best_locations:
            # Partition
            c11 = choice.get_c1(self.cov)
            c22, c23 = choice.get_c2_c3(self.cov)
            c24, c25 = choice.get_c4_c5(self.cov)

            c2s = [c11, c22, c23, c24, c25]

            sum_0 = 0
            ds = []
            for i in range(len(c2s)):
                distance = self.dist.fetch(cs[i], c2s[i])
                sum_0 += distance
                ds.append(distance)

            ds_val = sum_0 - min(ds)
            if first:
                min_dis = ds_val
                min_choice = choice
                first = False
                continue

            if ds_val < min_dis:
                min_dis = ds_val
                min_choice = choice

        # Extract the best region
        return min_choice

    def search_objects(self, dir_process, output_file):
        imagetp = ImageHandler(dir_process)

        for i in range(len(self.image.regions)):
            region = self.process_image_for_region(imagetp, i)

            imagetp.add_region(region.vertex0, region.vertex1)

        imagetp.show(output_dir=output_file, rect=True)

