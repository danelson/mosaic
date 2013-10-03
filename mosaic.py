#!/usr/bin/python
# -*- coding: utf-8 -*-

# Daniel Nelson
# https://github.com/danelson

import os
import optparse
import math
import time
import random
import bisect

import cv2
import numpy
from scipy.spatial.distance import cdist


class Mosaic:
    '''
    Class that has functions for creating mosaics and displaying
    collages of images. This class is not optimized for performance.
    If you have a large collection of tiles it is best to scale
    them to a smaller size before using this class. A quick way on
    the command line to scale images using image magick looks like
    the following:
    
    for i in `ls *.jpg`; do convert -resize 25% -quality 80 $i $i; done
    
    This class is only able to handle images of a certain file name. It
    must be of the form "img-{0:0xd}.jpg" where x is a number 1-9. For
    instance img-00000.jpg is a valid file name.
        
    Lastly all tiles that will be included in the mosaic must be
    greater than 50x50 and the base image must be greater than
    100x100.
    '''

    def __init__(self, base_img_path="test.jpg", tile_path="./tiles/",
                                        tile_path_format="img-{0:05d}.jpg"):
        '''
        Initializes fields for the class
        '''
        self.num_tiles = None
        self.sorted_intensities = None
        
        self.img_bank = {}
                
        self.base_img_path = base_img_path
        self.base_img = None
        
        self.tile_path = tile_path
        self.tile_path_format = tile_path_format
        
        self.mosaic_img = None
        
    def load_base_image(self, path):
        '''
        Loads the base image into the object and scales it so that
        its smallest edge is 100 pixels.
        '''
        if path == None:
            exit(" ### Error! No image path detected.")
            
        self.base_img = cv2.imread(path)
        if self.base_img == None:
            exit(" ### Error! '" + str(path) +
                "' failed to load.\n     Please check that it exists.")
            
        self.base_img = self._resize_img(self.base_img, 100)

    def load_tiles(self, path):
        '''
        Loads the all the images from the choosen tile folder. It
        converts them to 50x50 and stores them along with a value
        in a dictionary.
        '''
        self.num_tiles = len(os.listdir(path))
        print "Loading {0} tiles...".format(self.num_tiles)
        
        failed_to_load = 0
        for i in range(self.num_tiles):
            filename = self.tile_path_format.format(i)
            img = cv2.imread(path+filename)
            if img == None:
                failed_to_load += 1
                continue
                
            img = cv2.resize(img, (50,50))

            self._add_to_img_bank(img)
        
        if self.num_tiles-failed_to_load == 0:
            exit(" ### Error! Image tiles did not load. Check the path name.")
    
    def createMosaic(self):
        '''
        Creates a mosaic of the base image with the tiles.
        '''
        rows, cols = self.base_img.shape[0], self.base_img.shape[1]
        
        mosaic_img = numpy.zeros((rows*50, cols*50, 3),
                                    dtype=numpy.uint8)
        vectors = self.img_bank.keys()
        
        print "Creating mosaic...(this may take a while)"
        
        for i in range(rows):
            for j in range(cols):
                # The current position to place a tile.
                row_start = i*50
                row_stop = 50+i*50
                col_start = j*50
                col_stop = 50+j*50
                
                pixel = numpy.array([[self.base_img[i,j,0],
                                    self.base_img[i,j,1],
                                    self.base_img[i,j,2]]])
                
                match = cdist(pixel,numpy.array(vectors))
                index = int(match.argmin())
                            
                mosaic_img[row_start:row_stop, col_start:col_stop] = \
                            random.choice(self.img_bank[vectors[index]])
        
        self.mosaic_img = mosaic_img
        
    def save_mosaic(self, filename):
        cv2.imwrite(filename, self.mosaic_img)
    
    def _add_to_img_bank(self, img):
        '''
        '''
        intensity = (img[:,:,0].sum()/(img.size/3),
                    img[:,:,1].sum()/(img.size/3),
                    img[:,:,2].sum()/(img.size/3))
        
        if intensity in self.img_bank:
            self.img_bank[intensity].append(img)
        else:
            self.img_bank[intensity] = [img]

    def _resize_img(self, img, size):
        '''
        Resizes an image so that its smallest edge is length size
        '''
        rows, cols = img.shape[0:2]
        if cols < rows:
            scale = float(cols) / size 
        else:
            scale = float(rows) / size
            
        rows = max(int(rows/scale),size)
        cols = max(int(cols/scale),size)
            
        return cv2.resize(self.base_img, (cols,rows), interpolation=2)
        
    def _binarySearch(self, L, target):
        '''
        Returns the index of the target.
        '''
        index = bisect.bisect_left(L,target)
        return index if index < len(L) else -1

        
##############################################################################
##############################################################################

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-i", "--image", help="the path of the base image",
                                                        default="input.jpg")
    parser.add_option("-p", "--path",
                        help="the path of the folder containing the tiles",
                        default="./tiles/")
    parser.add_option("-f", "--format", help="the format of the filenames",
                                                    default="img-{0:05d}.jpg")
    options, remain = parser.parse_args()

    start = time.time()
    
    mosaic = Mosaic()
    mosaic.load_base_image(options.image)
    mosaic.load_tiles(options.path)
    mosaic.createMosaic()
    mosaic.save_mosaic("out1.jpg")
    
    stop = time.time()
    
    print "Total time: {0:.2f} sec".format(stop-start)


















