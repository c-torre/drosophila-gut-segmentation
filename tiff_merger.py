import os


def main():
    os.chdir("/home/c/Documents/Academic/BI3002 Biosciences Erasmus "
             "Placement Research Project/CellCounter")
    tifobj = tf.TiffFile("testack.lsm")
    arr = tifobj.asarray()





if __name__ == "__main__":
    pass
