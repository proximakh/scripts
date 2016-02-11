#-*- coding: utf-8 -*-

import urllib
import os
import sys

url_format = "http://dl.fullcirclemagazine.org/issue%d_en.pdf"
filename_format = "fcm_%04d.pdf"

no_min = int(sys.argv[1])
no_max = int(sys.argv[2])

for i in range(no_min, no_max+1):
  url = url_format % (i)
  data = urllib.urlopen(url)
  if data.getcode() == 404:
    print "issue %d not found. passing..." % (i)
    continue
  filename = filename_format % (i)

  if os.path.isfile(filename):
    print "issue %d already exists. passing..." % (i)
    continue

  sf = open(filename, "wb")
  print "saving %d..." % (i)
  sf.write(data.read())
  sf.close()
