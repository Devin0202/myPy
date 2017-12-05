import tensorflow as tf
# NumPy is often used to load, manipulate and preprocess data.
import numpy as np
import logging
################################################################################################
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s\n%(message)s',
                datefmt='%d %b %Y %H:%M:%S',
                filename='my.log',
                filemode='w')
#Output logging on screen              
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
################################################################################################
MnistDataRoute = "/home/devin/Desktop/Caffe2Model/mnist/caffe2_notebooks/tutorial_data/mnist/"
TrainData = "train-images-idx3-ubyte"
TrainLabel = "train-labels-idx1-ubyte"
TestData = "t10k-images-idx3-ubyte"
TestLabel = "t10k-labels-idx1-ubyte"

def MnistDataLoad(ObjStr):
    if -1 != ObjStr.find("image"):
        logging.debug("Images!\n%s"%(ObjStr))
        return ImageLoad(ObjStr)
    elif -1 != ObjStr.find("label"):
        logging.debug("Labels!\n%s"%(ObjStr))
        return LabelLoad(ObjStr)
    else:
        logging.debug("Invalid object!")

def ImageLoad(ObjStr):
    with open(ObjStr, 'r') as f:
        dt = np.dtype(np.uint32).newbyteorder('>')
        tmp = np.frombuffer(f.read(16), dtype=dt)
        MagicNum = tmp[0]
        ImgCount = tmp[1]
        ImgRow = tmp[2]
        ImgCol = tmp[3]

        arr = np.empty([ImgCount, ImgRow, ImgCol], dtype = np.uint8)
        for j in range(ImgCount):
            for i in range(ImgRow):
                arr[j, i] = np.frombuffer(f.read(ImgCol), dtype=np.uint8)
    logging.debug("Images refs:\nMagicNum %d\nImgCount %d\nImgRow %d\nImgCol %d"%(MagicNum, ImgCount, ImgRow, ImgCol))
    return arr
    
def LabelLoad(ObjStr):
    with open(ObjStr, 'r') as f:
        dt = np.dtype(np.uint32).newbyteorder('>')
        tmp = np.frombuffer(f.read(8), dtype=dt)
        MagicNum = tmp[0]
        LabelCount = tmp[1]

        arr = np.frombuffer(f.read(LabelCount), dtype=np.uint8)
    logging.debug("Labels refs:\nMagicNum %d\nLabelCount %d"%(MagicNum, LabelCount))
    return arr

dt4Train = MnistDataLoad(MnistDataRoute + TrainData)
print(dt4Train.shape)

lb4Train = MnistDataLoad(MnistDataRoute + TrainLabel)
print(lb4Train[25555])













