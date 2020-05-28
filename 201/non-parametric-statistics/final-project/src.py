import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.ndimage import sobel


class ImageHandler:
    def __init__(self, directory):
        self.image = Image.open(directory)
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

        f_xy[2:5, 0] = self.rgb[x, y, :]

        f_xy[5, 0] = self.der_imagex[x, y]
        f_xy[6, 0] = self.der_imagey[x, y]

        f_xy[7, 0] = self.der2_imagex[x, y]
        f_xy[9, 0] = self.der2_imagey[x, y]

        return f_xy

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
                          subimg=region[2])

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

    def create_region(self, vertex_sup_left, vertex_bot_right):
        # Find coordinates
        x1 = vertex_sup_left[0]
        x2 = vertex_bot_right[0]

        y1 = vertex_sup_left[1]
        y2 = vertex_bot_right[1]

        region = self.rgb[y1:y2, x1:x2, :]

        return (vertex_sup_left, vertex_bot_right,
                Image.fromarray(region, 'RGB'))

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
    def read_information(self, directory=None):
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


image = ImageHandler("exp-pics/og4.jpeg")
image.mode_draw_region()
