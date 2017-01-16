import os
import sys

old_path = os.path.abspath(sys.argv[1])
dir_name, base_name = os.path.split(old_path)
new_path = os.path.join(dir_name, base_name + "_renamed")

dir_ = os.listdir(old_path)
os.mkdir(new_path)

for i, file_ in enumerate(dir_):
    new_name = "img-{05d}.jpg".format(i)
    old = os.path.join(old_path, file_)
    new = os.path.join(old_path, new_name)
    os.rename(old_path, new_path)