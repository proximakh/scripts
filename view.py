import sys
import cv2
import numpy as np

for filename in sys.argv[1:]:
  print filename
  f = open(filename, "rb")
  d = f.read()
  y = np.ndarray(shape=(720,1280), buffer=d[0:1280*720], dtype=np.uint8)
  u = np.ndarray(shape=(320,640), buffer=d[1280*720:1280*720+1280*720/4], dtype=np.uint8)
  v = np.ndarray(shape=(320,640), buffer=d[1280*720+1280*720/4:1280*720+1280*720/2], dtype=np.uint8)
  
  cv2.imshow('Y', y)
  cv2.imshow('U', u)
  cv2.imshow('V', v)
  cv2.waitKey()
  
  f.close()
