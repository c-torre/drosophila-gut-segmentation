
import os
from skimage.external import tifffile as tf
import numpy as np
import matplotlib.pyplot as plt


def main():
    os.chdir("/home/carlos/Documents/Academic/BI3002 Biosciences Erasmus "
             "Placement Research Project/CellCounter")
    tifobj = tf.TiffFile("testack.lsm")
    arr = tifobj.asarray()
    return arr


class LSM:

    def __init__(self):
        self.red_sum = {}
        self.green_sum = {}
        self.blue_sum = {}
        self.red_max = {}
        self.green_max = {}
        self.blue_max = {}

    def project_channel_sum(channelid):
        """ Takes a 6 dimensions tiff array and projects the Z axis into X, Y.
        Uses the max intensity value of each Z slice.
        """
        arr = main()
        channel_sum = np.zeros((512, 512), dtype=np.int8)
        for i in range(0, np.size(arr, 2)):
            channel_sum = np.add(channel_sum, arr[0, 0, i, channelid, :, :])
        # Normalize, first 0 - 1, then to max = 255 (uint8)
        channel_sum = channel_sum.astype(np.float64) / channel_sum.max()
        channel_sum = 255 * channel_sum
        channel_sum = channel_sum.astype(np.uint8)
        return channel_sum

    def project_channel_max(channelid):
        """ Takes a 6 dimensions tiff array and projects the Z axis into X, Y.
        Uses the max intensity value of each Z slice.
        """
        arr = main()
        channel_max = np.zeros((512, 512), dtype=np.int8)
        for i in range(0, np.size(arr, 2)):
            channel_max = np.fmax(channel_max, arr[0, 0, i, channelid, :, :],
                                  dtype=np.int8)
        # Normalize, first 0 - 1, then to max = 255
        channel_max = channel_max.astype(np.float64) / channel_max.max()
        channel_max = 255 * channel_max
        channel_max = channel_max.astype(np.uint8)
        return channel_max

    red_sum = project_channel_sum(0)
    green_sum = project_channel_sum(1)
    blue_sum = project_channel_sum(2)

    red_max = project_channel_max(0)
    green_max = project_channel_max(1)
    blue_max = project_channel_max(2)


lsm1 = LSM

tf.imsave('SUMoutput.tiff', lsm1.blue_sum)
tf.imsave('MAXoutput.tiff', lsm1.blue_max)


if __name__ == "__main__":
    main()
