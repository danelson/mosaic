#rename.py

import os
import sys

path1 = "/Users/danelson/Desktop/images/"
path2 = "/Users/danelson/Desktop/images2/"

old_full_path = os.path.abspath(sys.argv[1])
dirname, basename = os.path.split(old_full_path)
new_full_path = os.path.join(dirname, basename+"_renamed")

dir = os.listdir(old_full_path)
os.mkdir(new_full_path)

for i, file in enumerate(dir):
	new_name = "img-{05d}.jpg".format(i)
    old = os.path.join(old_full_path, file)
    new = os.path.join(old_full_path, new_name)
	os.rename(old_full_path,new_full_path)