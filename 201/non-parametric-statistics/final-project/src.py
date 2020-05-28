import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st
from PIL import Image
from scipy.linalg import eigvals
from scipy.ndimage import sobel
from sklearn.covariance import LedoitWolf


class ImageHandler:
    def __init__(self, directory, array=None):
        if array is None:
            self.image = Image.open(directory)
        else:
            self.image = Image.fromarray(array, 'RGB')
        self.directory = directory

        # Modes for the image
        self.intensity = np.array(self.image.convert("L"))
        self.rgb = np.array(self.image.convert("RGB"))

        # Derivative information
        self.der_imagex = np.array([])
        self.der_imagey = np.array([])
        self.der2_imagex = np.array([])
        self.der2_imagey = np.array([])

        self.calculate_derivatives()

        # Regions information
        self.regions = []

    # Calculates derivatives of an image
    def calculate_derivatives(self):
        # First derivative
        self.der_imagex = sobel(self.intensity, axis=1)
        self.der_imagey = sobel(self.intensity, axis=0)

        # Second derivative
        self.der2_imagex = sobel(self.der_imagex, axis=1)
        self.der2_imagey = sobel(self.der_imagey, axis=0)

    # Calculates the feature for a position
    def features(self, pos_x, pos_y):
        f_xy = np.zeros((9, 1))

        f_xy[0, 0] = pos_y
        f_xy[1, 0] = pos_x

        f_xy[2:5, 0] = self.rgb[pos_x, pos_y, :]

        f_xy[5, 0] = np.abs(self.der_imagex[pos_x, pos_y])
        f_xy[6, 0] = np.abs(self.der_imagey[pos_x, pos_y])

        f_xy[7, 0] = np.abs(self.der2_imagex[pos_x, pos_y])
        f_xy[8, 0] = np.abs(self.der2_imagey[pos_x, pos_y])

        return f_xy

    # Calculate matrix of features
    def matrix_features(self):
        rows = []
        for x in range(self.intensity.shape[0]):
            for y in range(self.intensity.shape[1]):
                rows.append(self.features(x, y)[:, 0])
        return np.array(rows)

    # Mode to find desired regions
    def mode_draw_region(self):
        first = True
        while True:
            # Continue to draw regions
            if not first:
                answer = input("Do you want to add another region? [y/n] ")
                if "y" not in answer:
                    break
            else:
                first = False

            # Start drawing regions
            while True:
                range_x = self.intensity.shape[1] - 1
                range_y = self.intensity.shape[0] - 1

                x0 = int(input("x0 [0 - {}]: ".format(range_x)))
                y0 = int(input("y0 [0 - {}]: ".format(range_y)))

                x1 = int(input("x1 [> x0]: "))
                y1 = int(input("y1 [> y0]: "))

                region = self.create_region((x0, y0), (x1, y1))
                plt.close('all')
                self.show(cont=True, regions=[region], rect=True,
                          subimg=region[2].image)

                ans = input("Continue? [y/n] ")
                if "y" not in ans:
                    break

            self.add_region((x0, y0), (x1, y1))

        ans = input("Want to export the regions found? [y/n] ")
        if "y" in ans:
            try:
                self.export_info()
            except:
                self.export_info("temp_file.imgh")

    # Create region
    def create_region(self, vertex_sup_left, vertex_bot_right):
        # Find coordinates
        x1 = vertex_sup_left[0]
        x2 = vertex_bot_right[0]

        y1 = vertex_sup_left[1]
        y2 = vertex_bot_right[1]

        region = self.rgb[y1:y2, x1:x2, :]

        return (vertex_sup_left, vertex_bot_right,
                ImageHandler(self.directory, array=region))

    # Add region
    def add_region(self, vertex_sup_left, vertex_bot_right):
        self.regions.append(self.create_region(vertex_sup_left,
                                               vertex_bot_right))

    # Save information of image in file
    def export_info(self, directory=None):
        if directory is None:
            new_directory = self.directory.split(".")[0]
            directory = new_directory + ".imgh"

        output = open(directory, "w")
        for region in self.regions:
            output.write(str(region[0]) + "\t")
            output.write(str(region[1]) + "\n")
        output.close()

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
            self.add_region(vertex0, vertex1)

    # Partition image in two
    def half_image(self, horizontal=True):
        if horizontal:
            partition = int(self.rgb.shape[1] / 2)

            first = self.rgb[:, :partition, :]
            second = self.rgb[:, partition:, :]
        else:
            partition = int(self.rgb.shape[0] / 2)

            first = self.rgb[:partition, :, :]
            second = self.rgb[partition:, :, :]

        first_im = ImageHandler(self.directory, array=first)
        second_im = ImageHandler(self.directory, array=second)
        return first_im, second_im

    # Array of square for given scale
    def get_regions(self, regions, index_region, scale):
        # Calculate width and height
        vertex0 = regions[index_region][0]
        vertex1 = regions[index_region][1]

        width = abs(vertex0[0] - vertex1[0])
        height = abs(vertex1[0] -  vertex1[1])

    # Show image in pyplot
    def show(self, rect=False, regions=None, cont=False, subimg=None):
        if subimg is not None:
            fig, (ax, ax2) = plt.subplots(nrows=2)
        else:
            _, ax = plt.subplots(1)

        ax.imshow(self.rgb, interpolation="none")

        # Draw selected regions
        if rect:
            if regions is None:
                regions = self.regions

            for region in regions:
                vertex = region[0]
                width = region[1][0] - vertex[0]
                height = region[1][1] - vertex[1]

                rectangle = patches.Rectangle(vertex, width, height,
                                              fill=False, edgecolor='w',
                                              linewidth=2)
                ax.add_patch(rectangle)

        if subimg is not None:
            ax2.imshow(subimg)

        plt.show(block=(not cont))


class Cov:
    def __init__(method):
        self.method = method

    def fetch(self, sample):
        if self.method == 0:
            return np.cov(sample.transpose())

    # Correlation matrix to cov
    def corr_to_cov(data, correlation):
        stds = data.std(axis=0, ddof=1)

        cov = np.zeros(correlation.shape)
        for i in range(correlation.shape[0]):
            for j in range(correlation.shape[1]):
                cov[i, j] = correlation[i, j] * stds[i] * stds[j]

        return cov

    # Calculate comedian for two vectors
    def comedian(u, v):
        median_u = np.quantile(u, 0.5)
        median_v = np.quantile(v, 0.5)

        aux = (u - median_u) * (v - median_v)

        return np.quantile(aux, 0.5)

    # Calculate comedian matrix
    def calculate_com(sample):
        com = np.zeros((sample.shape[1], sample.shape[1]))
        for i in range(sample.shape[1]):
            for j in range(sample.shape[1]):
                com[i, j] = comedian(sample[:, i], sample[:, j])

        return com

    # method =
    #    0 -> Spearman
    #    1 -> Kendall
    def calculate_cov_corr(sample, method=0):
        if method == 0:
            # Calculate Spearman
            spearman = pd.DataFrame(sample).corr(method="spearman").to_numpy()
            cov = corr_to_cov(sample, spearman)
        else:
            # Calculate Kendall
            kendall = pd.DataFrame(sample).corr(method="kendall").to_numpy()
            cov = corr_to_cov(sample, kendall)
        return cov

    # Calculate covariance of shrinkages
    def calculate_cov_shrinkages(sample):
        return LedoitWolf().fit(sample).covariance_


class ImageProcessor:
    def __init__(directory, method=0):
        self.image = ImageHandler(directory)
        self.cov = Cov(method)

        self.regions = []

        # Process image
        self.c1 = []
        # Find features for regions
        self.get_region_1()

        self.c2 = []
        self.c3 = []
        self.c4 = []
        self.c5 = []

    def get_region_1(self):
        for region in self.regions:
            imgh = region[2]
            matrix = imgh.matrix_features()

            self.c1.append(self.cov.fetch(matrix))

    def distance(c1, c2):
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

    def process_image(self, find_object_image, method=0):
        if method == 0:
            calc = lambda matrix: np.cov(matrix.transpose())


image = ImageProcessor("exp-pics/lower_res_images/og1.jpeg")
