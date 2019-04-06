
import os
from skimage.external import tifffile as tf
import numpy as np
import matplotlib.pyplot as plt


def main():
    os.chdir("/home/c/Documents/Academic/BI3002 Biosciences Erasmus "
             "Placement Research Project/CellCounter")
    tifobj = tf.TiffFile("testack.lsm")
    arr = tifobj.asarray()

    lsm1 = LSM

    tf.imsave('SUMoutput.tiff', lsm1.blue_sum)
    tf.imsave('MAXoutput.tiff', lsm1.blue_max)

    rgb = np.dstack([lsm1.red_max,    # R
                     lsm1.green_max,  # G
                     lsm1.blue_max])  # B
    rgb = np.moveaxis(rgb, -1, 0)
    tf.imsave('rgb.tiff', rgb)

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


if __name__ == "__main__":
    main()



#
#tifobj = tf.TiffFile("rgb.tiff")
# metadata = tifobj.info()
# metadata = metadata + "\nalalala"
# metadata
# metadata.split("\n")
# tifobj.info().split("\n")
#
# dic = {'rub': 1.2, "dab": 23}
#
#
#
#
# tifobjj = tf.TiffFile("rgb (copy).tiff")
# metadataj = tifobjj.info()
# metadataj
#
#
#
#
# ['TIFF file: rgb (copy).tiff, 795 KiB, big endian, imagej',
#  '',
#  'Series 0: 3x512x512, uint8, CYX, 1 pages, memmap-offset=27640',
#  '',
#  'Page 0: 3x512x512, uint8, 8 bit, palette, raw, imagej|contiguous',
#  '* 254 new_subfile_type (1I) 0',
#  '* 256 image_width (1I) 512',
#  '* 257 image_length (1I) 512',
#  '* 258 bits_per_sample (1H) 8',
#  '* 262 photometric (1H) 3',
#  "* 270 image_description (56s) b'ImageJ=1.52a\\nimages=3\\nchannels=3\\nmode=color\\",
#  '* 273 strip_offsets (1I) (27640,)',
#  '* 277 samples_per_pixel (1H) 1',
#  '* 278 rows_per_strip (1H) 512',
#  '* 279 strip_byte_counts (1I) (786432,)',
#  '* 320 color_map (768H) (0, 256, 512, 768, 1024, 1280, 1536, 1792, 2048, 2304, 2',
#  '* 50838 imagej_byte_counts (6I) (28, 25754, 6, 10, 8, 48)',
#  "* 50839 imagej_metadata (25854B) b'IJIJinfo\\x00\\x00\\x00\\x01labl\\x00\\x00\\x00\\x03",
#  '',
#  'IMAGEJ_TAGS',
#  '* ImageJ: 1.52a',
#  '* channels: 3',
#  '* images: 3',
#  '* info: ImageDescription: {"metadata_raw": "TIFF file: testack.lsm, 230 MiB, li',
#  "* labels: ['Red', 'Green', 'Blue']",
#  '* loop: False',
#  '* mode: color',
#  '* ranges: (0.0, 255.0, 0.0, 255.0, 0.0, 255.0)']
# #def project_channel_sum(channelid):
#    """ Takes a 6 dimensions tiff array and projects the Z axis into X, Y.
#    Uses the max intensity value of each Z slice.
#    """
#    arr = main()
#    channel_sum = np.zeros((512, 512), dtype=np.int8)
#    for i in range(0, np.size(arr, 2)):
#        channel_sum = np.add(channel_sum, arr[0, 0, i, channelid, :, :])
#    # Normalize, first 0 - 1, then to max = 255
#    channel_sum = channel_sum.astype(np.float64) / channel_sum.max()
#    channel_sum = 255 * channel_sum
#    channel_sum = channel_sum.astype(np.uint8)
#    return channel_sum
#
#spam = project_channel_sum(2)
#spam
#
#
#










#
#
## two main modules:
## - ndimage
##   https://docs.scipy.org/doc/scipy/reference/ndimage.html
## - skimage
##   https://scikit-image.org/
##
## each have multiple submodules for morphology, filters, measurements, etc.
#
## usage for binarisation, morphological processing and labeling
#import skimage.measure as skime
#import skimage.morphology as skimo
#from skimage.filters import threshold_otsu
#from scipy import ndimage
#from matplotlib.pyplot import imshow
#
## you may need to do some preprocessing of the images to have a clearer distinction
## between background and signal, e.g.:
##
##   - edge preserving smoothing
##     https://en.wikipedia.org/wiki/Edge-preserving_smoothing
##     the simples method is despeckling with a median filter:
##     http://scipy-lectures.org/advanced/image_processing/
##     other more complicated ones we can try:
##     http://scikit-image.org/docs/dev/auto_examples/filters/plot_nonlocal_means.html
##
##   - you may want to despeckle each z-position in the stack, and then project!
##
##   - some blurring may be advantageous (gaussian filter) but also lead to more
##     fusion of objects
#
## after that you will be ready to "threshold", for which there are multiple
## possibilities:
##  - Otsu thresholding (very popular and already implemented)
##  - Entropy thresholding (a bit more permissive than Otsu, depending on the images, implemented by me below)
##  - Triangle threshold (invented for biological images, implemented by me below)
#
#bw = img < threshold_otsu(img) # binarisation, all image pixels are True/1 or False/0
#
## now you might need a bit of "mathematical morphology", operations with binary
## images that modify the edges of the objects:
#
#bw_fill = ndimage.binary_fill_holes(bw) # all objects are solid (no holes)
## (there are MANY other operations, more sophisticated, but we need to have a look first)
#
## to visualise:
#imshow(np.hstack([bw, bw_fill])) # hstack puts together two arrays side to side
#                                 # (h for horizontal), but they need to have the
#                                 # same size in that dimension
