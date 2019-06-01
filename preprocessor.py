import os

import numpy as np
from skimage import filters
from skimage.external import tifffile as tf
from skimage.morphology import disk


def main():
    """ TODO the system to choose a file is slow, not extensive and not very
    beautiful."""
    os.chdir()
    print('user? [JOAQUIN, CARLOS]')
    USER = input()
    JOAQUIN = "/Users/JQ/repos"
    CARLOS = "/home/c/Documents/Academic/BI3002 Biosciences Erasmus "
    "Placement Research Project/Report/Preliminary results"
    os.chdir(USER)

    print('name?:')
    file_name = input()
    # preprocessor = PreProcessor("testack.lsm")
    preprocessor = PreProcessor(file_name)
    preprocessor.save_tiff()


class PreProcessor:
    """Requires argument: tiff_name (str)
    Generates an instance with all pre-processing steps ready"""

    def __init__(self, tiff_name):
        self.tiff_name = tiff_name
        self.tiff_array = self.create_tiff_array()

        self.red_summation = self.project_channel_summation(0)
        self.green_summation = self.project_channel_summation(1)
        self.blue_summation = self.project_channel_summation(2)

        self.red_max = self.project_channel_max(0)
        self.green_max = self.project_channel_max(1)
        self.blue_max = self.project_channel_max(2)

        self.red_filtered = self.median_filter(self.red_max)
        self.green_filtered = self.median_filter(self.green_max)
        self.blue_filtered = self.median_filter(self.blue_max)

        self.projected_array = self.stack_channels(self.red_max,
                                                   self.green_max,
                                                   self.blue_max)
        self.filtered_array = self.stack_channels(self.red_filtered,
                                                  self.green_filtered,
                                                  self.blue_filtered)

    def create_tiff_array(self):
        tiff_object = tf.TiffFile(self.tiff_name)
        tiff_array = tiff_object.asarray()
        return tiff_array

    def project_channel_summation(self, channel_id):
        """ Takes a 6 dimensions tiff array and projects the Z axis into X, Y.
        Uses the max intensity value of each Z slice.
        """

        channel_summation = np.zeros((512, 512), dtype=np.int8)
        for i in range(0, np.size(self.tiff_array, 2)):
            channel_summation = np.add(channel_summation, self.tiff_array[0, 0,
                                                          i, channel_id, :, :])
        # Normalize, first 0 - 1, then to max = 255 (uint8)
        channel_summation = channel_summation.astype(np.float64) \
                            / channel_summation.max()
        channel_summation = 255 * channel_summation
        channel_summation = channel_summation.astype(np.uint8)
        return channel_summation

    def project_channel_max(self, channel_id):
        """ Takes a 6 dimensions tiff array and projects the Z axis into X, Y.
        Uses the max intensity value of each Z slice.
        """

        channel_max = np.zeros((512, 512), dtype=np.int8)
        for i in range(0, np.size(self.tiff_array, 2)):
            channel_max = np.fmax(channel_max, self.tiff_array[19, 0, i,
                                               channel_id, :, :],
                                  dtype=np.int8)
        # Normalize, first 0 - 1, then to max = 255
        channel_max = channel_max.astype(np.float64) / channel_max.max()
        channel_max = 255 * channel_max
        channel_max = channel_max.astype(np.uint8)
        return channel_max

    @staticmethod
    def stack_channels(red, green, blue):
        stacked_array = np.dstack([red, green, blue])
        stacked_array = np.moveaxis(stacked_array, -1, 0)
        return stacked_array

    @staticmethod
    def median_filter(channel, disk_size=1):
        """ Median filtering using the optimal disk_size for our images; 1.
        """

        filtered_array = filters.median(channel, disk(disk_size))
        return filtered_array

    def save_tiff(self):
        file_name = self.tiff_name + ".tiff"
        tf.imsave(file_name, self.filtered_array)


if __name__ == '__main__':
    main()
