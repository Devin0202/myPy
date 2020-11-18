# -*- coding: utf-8 -*-
"""
Language:   python3
Goal:       Convert NV21 to jpg or png
"""
import os
import sys
import time
import cv2
import shutil
import numpy
import numpy as np

def bgr2NV(img_mat: numpy.ndarray, isNV21 = True, isForced = False) -> numpy.ndarray:
  rtv = None
  height, width, channel = img_mat.shape
  if 3 != channel or height <= 0 or width <= 0:
    print("Image is invalid!")
  else:
    if (not isForced) and (0 != height % 4 or 0 != width % 4):
      print("Height and Width should be divided by 4!")
      return rtv
    elif isForced:
      pad_h = 0 if 0 == height % 4 else 4 - (height % 4)
      pad_w = 0 if 0 == width % 4 else 4 - (width % 4)
      mat_tmp = cv2.copyMakeBorder(img_mat.copy(), 0, pad_h, 0, pad_w, cv2.BORDER_REPLICATE)
      print("New shape of image(HWC): " + mat_tmp.shape)
    else:
      mat_tmp = img_mat.copy()
    
    # Y =  0.299R + 0.587G + 0.114B
    # U = -0.147R - 0.289G + 0.436B
    # V =  0.615R - 0.515G - 0.100B
    newH, newW, newC = mat_tmp.shape
    rtv = np.ndarray((newH * 3 // 2, newW, 1), dtype=np.uint8)
    for i in range(newH):
      for j in range(newW):
        y = 0.114 * mat_tmp[i][j][0] + 0.587 * mat_tmp[i][j][1] + 0.299 * mat_tmp[i][j][2]
        y = min(max(0, round(y)), 255)
        rtv[i][j] = y

    for i in range(newH, newH * 3 // 2):
      for j in range(0, newW, 2):
        ii = (i - newH) * 2
        jj = j // 2 * 2
        u = 0.436 * mat_tmp[ii][jj][0] - 0.289 * mat_tmp[ii][jj][1] - 0.147 * mat_tmp[ii][jj][2]
        v = -0.100 * mat_tmp[ii][jj][0] - 0.515 * mat_tmp[ii][jj][1] + 0.615 * mat_tmp[ii][jj][2]
        u += 128
        v += 128
        u = min(max(0, round(u)), 255)
        v = min(max(0, round(v)), 255)
        if isNV21:
          rtv[i][j], rtv[i][j + 1] = v, u
        else:
          rtv[i][j], rtv[i][j + 1] = u, v
  return rtv

if __name__ == "__main__":
  src = "/Users/daiyi/Projects/tmp/pypg/src/ori.jpg"
  dstRoot = "/Users/daiyi/Projects/tmp/pypg/dst/formats/"

  print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
  if not os.path.exists(dstRoot):
    os.makedirs(dstRoot)

  img_bgr = cv2.imread(src)

  # Reverse -> cv::COLOR_YUV2BGR_NV21
  nv21 = bgr2NV(img_bgr, isNV21=True)
  with open(dstRoot + os.sep + "NV21.dat", "wb") as fw:
    byteSize = fw.write(nv21.data)
    print(byteSize)
  
  # Reverse -> cv::COLOR_YUV2BGR_NV12
  nv12 = bgr2NV(img_bgr, isNV21=False)
  with open(dstRoot + os.sep + "NV12.dat", "wb") as fw:
    byteSize = fw.write(nv12.data)
    print(byteSize)

  # Reverse -> cv::COLOR_RGB2BGR
  img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
  # cv2.imwrite(dstRoot + os.sep + "RGB888.jpg", img_rgb)
  with open(dstRoot + os.sep + "RGB888.dat", "wb") as fw:
    byteSize = fw.write(img_rgb.data)
    print(byteSize)

  # Reverse -> cv::COLOR_RGBA2BGR
  img_rgba = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGBA)
  # cv2.imwrite(dstRoot + os.sep + "RGBA8888.png", img_rgba)
  with open(dstRoot + os.sep + "RGBA8888.dat", "wb") as fw:
    byteSize = fw.write(img_rgba.data)
    print(byteSize)

  # Reverse -> cv::COLOR_BGRA2BGR
  img_bgra = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2BGRA)
  # cv2.imwrite(dstRoot + os.sep + "BGRA8888.png", img_bgra)
  with open(dstRoot + os.sep + "BGRA8888.dat", "wb") as fw:
    byteSize = fw.write(img_bgra.data)
    print(byteSize)

  # Reverse -> cv::COLOR_YUV2BGR_YV12
  img_yuv_yv12 = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YUV_YV12)
  with open(dstRoot + os.sep + "YV12.dat", "wb") as fw:
    byteSize = fw.write(img_yuv_yv12.data)
    print(byteSize)

  # Reverse -> cv::COLOR_YUV2BGR_I420
  img_yuv_i420 = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YUV_I420)
  with open(dstRoot + os.sep + "YUV_420_888.dat", "wb") as fw:
      byteSize = fw.write(img_yuv_i420.data)
      print(byteSize)

  # Reverse -> cv::COLOR_YUV2BGR_IYUV
  img_yuv_420p = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YUV_IYUV)
  with open(dstRoot + os.sep + "YUV420P.dat", "wb") as fw:
    byteSize = fw.write(img_yuv_420p.data)
    print(byteSize)

  print(os.linesep)
  print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
