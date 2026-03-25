#!/usr/bin/env python3
#
# Copyright (C) 2023 Yannix Technologies
#			Written by Thanachart (Ultra) Satianjarukarn
#
########################################################
#
#	STANDARD IMPORTS
#

import cv2 as cv

import numpy as np

########################################################
#
#	CLASS DEFINITIONS
#

class ImageData():
    '''This class create for storing the buffer image in any color model
    '''
    def __init__( self, imagePath: str ):
        '''
        Parameters
        ----------

        imagePath : str
            The image path for reading
        
        '''
        #   Read image, default openCV was BGR channel
        imageBGR = cv.imread( imagePath )

        #   Convert to float 32 image
        imageBGR = imageBGR.astype( np.float32 ) / np.iinfo( imageBGR.dtype ).max

        #   Declare image in 3 colors space
        self.imageGray = cv.cvtColor( imageBGR, cv.COLOR_BGR2GRAY )
        self.imageYCrCb = cv.cvtColor( imageBGR, cv.COLOR_BGR2YCrCb )
        self.imageRGB = cv.cvtColor( imageBGR, cv.COLOR_BGR2RGB )

    def size( self ):
        '''Return the shape of 2D image, just imageHeight, imageWidth
        '''
        return self.imageGray.shape
    

    def getPixelValue( self, points ):
        '''Function that recieve the pixels points and return the color value of each 
        pixels points by extract the color in input image with points.

        Parameters
        ----------
        points : ndarray of shape ( nSample, 2 )
            The coordinate in of ellipse region. Input coordinate in form [ posY, posX ]

        Returns
        ----------
        colorValueArr : ndarray of shape ( nSample, nDim )
            Color value that extract from image.

        '''
        # 	Store the color value in `colorValueArr` by extracting color value from the posY and posX pixels in points input.
            #	Which can easily represent with ( nSample, nDim ).
        colorValueArr = self.imageRGB[ points[ :, 0 ], points[ :, 1 ], : ]

        return colorValueArr

def drawEllipseOnImage( image: np.ndarray, ellipseObjectList: list, offset: tuple = None ):
    '''Drawing ellipse on image for all candidate ellipse

    Parameters
    -----------

    image : ndarray with shape ( imageHeight, imageWidth )
        The input image for visualize

    ellipseObjectList : list of Ellipse object
        The list store the ellipse object

    offset : tuple, default = None
        The offset values on x & y axis, for offset the center of ellipse

    Return
    ---------
    image : ndarray with shape ( imageHeight, imageWidth )
        The input image for visualize with already draw ellipse

    
    '''
    #   Loop for all ellipse object list
    for ellipseObject in ellipseObjectList:

        #   Extract the ellipse parameters
        c_x, c_y, r1, r2, angle_deg = ellipseObject.params
        
        #   Draw the ellipse on image
            #   If offset is None
        if offset is None:

            #   Draw without offset
            cv.ellipse( image, ( int( c_x ), int( c_y ) ), ( int( r1 ), int( r2 ) ), 360-angle_deg, 0, 360, color = ( 1, 0, 0 ) , thickness = 3 )

            #   If offet was input
        else:

            #   Draw ellipse with offset
            x, y = offset
            cv.ellipse( image, ( int( x+c_x ), int( y+c_y ) ), ( int( r1 ), int( r2 ) ), 360-angle_deg, 0, 360, color = ( 0, 1, 0 ) , thickness = 3 )

    return image