import bisect
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st
import time

from PIL import Image, ImageOps
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
        parent_matrix = self.parent.get_matrix()
        self.matrix = parent_matrix[:, self.vertex0[0]:self.vertex1n[0],
                                    self.vertex0[1]:self.vertex1n[1]]
        self.matrix = self.matrix.reshape(-1, 9)

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
class InputImage (Region):
    def __init__(self, directory_input):
        parent = ImageHandler(directory_input)
        vertex0 = (0, 0)
        vertex1 = list(parent.get_intensity().shape)
        vertex1[0] -= 1
        vertex1[1] -= 1
        super().__init__(vertex0, vertex1, parent)

#################################################
class ImageHandler:
    def __init__(self, directory, input_img=None):
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

        # Input information
        self.input_img = input_img
        self.regions = []

    # Adds a region to the regions
    def add_region(self, vertex0, vertex1):
        self.regions.append(Region(vertex0, vertex1, self))

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

    # Calculate matrix of features
    def create_matrix(self):
        intensity = self.get_intensity()

        create_mat = lambda i, j, k: self.pixel_feature(int(j), int(k), int(i))
        self.matrix = np.fromfunction(np.vectorize(create_mat), (9,
                                                                 intensity.shape[0],
                                                                 intensity.shape[1]))

    # Calculates the feature for a pixel given it's position in the array
    def pixel_feature(self, pos_x, pos_y, k_feat):
        if self.der_imagex is None:
            self.create_derivatives()

        rgb = self.get_rgb()
        if k_feat == 0:
            return pos_y
        elif k_feat == 1:
            return pos_x
        elif k_feat == 2:
            return rgb[pos_x, pos_y, 0]
        elif k_feat == 3:
            return rgb[pos_x, pos_y, 1]
        elif k_feat == 4:
            return rgb[pos_x, pos_y, 2]
        elif k_feat == 5:
            return np.abs(self.der_imagex[pos_x, pos_y])
        elif k_feat == 6:
            return np.abs(self.der_imagey[pos_x, pos_y])
        elif k_feat == 7:
            return np.abs(self.der2_imagex[pos_x, pos_y])
        return np.abs(self.der2_imagey[pos_x, pos_y])

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
    def get_regions(self, scale, index, best_cs, locations, key):
        rgb = self.get_rgb()

        # Calculate width and height
        vertex0 = self.input_img.vertex0
        vertex1 = self.input_img.vertex1

        width = int(scale*(vertex1[0] - vertex0[0]))
        height = int(scale*(vertex1[1] -  vertex0[1]))

        if width == 0 or height == 0:
            return

        # Find all regions
        step = int(1.15 ** index * 3)
        for x in range(0, rgb.shape[0], step):
            if x + width >= rgb.shape[0]:
                break
            for y in range(0, rgb.shape[1], step):
                if y + height >= rgb.shape[1]:
                    break
                vertex1 = (x, y)
                vertex2 = (x+width, y+height)
                region_aux = Region(vertex1, vertex2, self)
                ImageHandler.add_to_locs(best_cs, key, region_aux, locations)

        for x in range(0, rgb.shape[0], step):
            if x + height >= rgb.shape[0]:
                break
            for y in range(0, rgb.shape[1], step):
                if y + width >= rgb.shape[1]:
                    break
                vertex1 = (x, y)
                vertex2 = (x+height, y+width)
                region_aux = Region(vertex1, vertex2, self)
                ImageHandler.add_to_locs(best_cs, key, region_aux, locations)
        return locations

    @staticmethod
    def add_to_locs(best_cs, key, elem, locations):
        c_elem = key(elem)
        if best_cs[0] == -1:
            best_cs[0] = c_elem
            locations[0] = elem
            return
        if best_cs[-1] != -1:
            max_cs = np.max(best_cs)
            if c_elem > max_cs:
                return

        index_to_change = np.argmax(best_cs > c_elem)
        best_cs[(index_to_change + 1):] = best_cs[index_to_change:-1]
        best_cs[index_to_change] = c_elem

        locations[(index_to_change + 1):] = locations[index_to_change:-1]
        locations[index_to_change] = elem

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

    @staticmethod
    def all_covariances():
        return range(5)

    @staticmethod
    def covariances_names(index):
        if index == 0:
            return "Usual"
        elif index == 1:
            return "Comedian"
        elif index == 2:
            return "Spearman"
        elif index == 3:
            return "Kendall"
        elif index == 4:
            return "LW"

#################################################
class Distance:
    def __init__(self, method=0):
        self.method = method
        self.distances = ['fro', 1, 2, np.inf]

    def fetch(self, c1, c2):
        if self.method == 0:
            return np.real(Distance.author_distance(c1, c2))
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

    @staticmethod
    def all_distances():
        return range(2)

    @staticmethod
    def distances_names(index):
        if index == 0:
            return "Author"
        elif index == 1:
            return "Frobenius"
        elif index == 2:
            return "Norm 1"
        elif index == 3:
            return "Norm 2"
        elif index == 4:
            return "Norm Inf"

#################################################
class ImageProcessor:
    def __init__(self, directory_input, method=0, method_dist=0):
        self.image = InputImage(directory_input)
        self.cov = Cov(method)
        self.dist = Distance(method_dist)

        # Scale changes
        scale1 = [0.85 ** j for j in range(5, -1, -1)]
        scale2 = []

        self.scales = np.array(scale1 + scale2)

    # Find object for a defined region
    def process_image_for_region(self, imagep):
        # Image to process
        region = self.image
        c1 = region.get_c1(self.cov)

        # Regions
        index = 0
        fixedsize = 1000

        locations = np.empty(fixedsize, dtype=object)
        best_cs = -np.ones(fixedsize)

        key = lambda x: self.dist.fetch(c1, x.get_c1(self.cov))
        for scale in self.scales:
            locations = imagep.get_regions(scale, index, best_cs,
                                           locations, key)
            index += 1

        best_locations = locations

        # Covariances
        c2, c3 = region.get_c2_c3(self.cov)
        c4, c5 = region.get_c4_c5(self.cov)

        cs = [c1, c2, c3, c4, c5]

        # Best choice
        min_dis = -1
        min_choice = None
        first = True
        for choice in best_locations:
            if choice is None:
                break
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
        return min_choice, min_dis

    def search_objects(self, dir_process, output_image):
        imagetp = ImageHandler(dir_process, input_img=self.image)
        region, obj_func = self.process_image_for_region(imagetp)
        imagetp.add_region(region.vertex0, region.vertex1)
        imagetp.show(output_dir=output_image, rect=True)

        return region, obj_func


#################################################
class ResultManager:
    def __init__(self, number_of_objs=5, test_per_objs=5, noises=["impulse"]):
        self.output_dir = "results/"
        self.perfomance_file = "results/performance.csv"

        self.images_dirs = []
        for i in range(number_of_objs):
            self.images_dirs.append("img{}/".format(i + 1))
        self.prefix = "images70/"

        self.test_cases = []
        for i in range(test_per_objs):
            self.test_cases.append("test_case{}.jpg".format(i + 1))

        noises = list(map(lambda x: "-" + x, noises))
        noises.append("")
        self.inputs = []
        for noise in noises:
            self.inputs.append("input" + noise + ".jpg")

        self.runs = {}

    def run_test_case(self, img_dir):
        noise = 0
        for input_file in self.inputs:
            for cov in tqdm(Cov.all_covariances()):
                for dist in Distance.all_distances():
                    imgh = ImageProcessor(self.prefix + img_dir + input_file,
                                          method=cov, method_dist=dist)

                    for i in range(len(self.test_cases)):
                        dir_test_case = self.prefix + img_dir + self.test_cases[i]
                        dir_real_case = self.prefix + img_dir + \
                                        "real{}.jpg".format(i + 1)
                        dir_image_out = self.output_dir + img_dir + str(noise) + \
                                        "-" + str(cov) + "-" + str(dist) + "-" + \
                                        self.test_cases[i]

                        region, obj = imgh.search_objects(dir_test_case,
                                                          dir_image_out)

                        real_img = InputImage(dir_real_case)
                        dist_c1 = Distance.author_distance(region.get_c1(imgh.cov),
                                                           real_img.get_c1(imgh.cov))
                        self.add_to_csv(cov, dist, noise, (obj, dist_c1))
            noise += 1

    def print_csv(self):
        csv = open(self.perfomance_file, "w")
        for key in self.runs:
            cov, dist, noise = key.split("-")
            csv.write(cov + "," + dist + "," + noise + "\n")
            csv.write("Obj Function,Distance to Og\n")
            for obj, dist in self.runs[key]:
                csv.write(str(obj) + "," + str(dist) + "\n")

        csv.close()


    def add_to_csv(self, index_cov, index_dist, index_noise, run_info):
        cov = Cov.covariances_names(index_cov)
        dist = Distance.distances_names(index_dist)
        nameExp = cov + "-" + dist + "-" + \
                  ["impulse", "normal"][index_noise]

        if nameExp not in self.runs:
            self.runs[nameExp] = [run_info]
        else:
            self.runs[nameExp].append(run_info)

    def get_results(self):
        for img_dir in self.images_dirs:
            self.run_test_case(img_dir)
        self.print_csv()


# rm = ResultManager()
# rm.get_results()
