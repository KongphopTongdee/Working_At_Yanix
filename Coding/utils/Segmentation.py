#!/usr/bin/env python3
#
# Copyright (C) 2023 Yannix Technologies
#			Written by Thanachart (Ultra) Satianjarukarn
#
########################################################
#
#	STANDARD IMPORTS
#

import numpy as np

import os

import ctypes


########################################################
#
#	LOCAL IMPORTS
#

########################################################
#
#	GLOBALS
#

#   The number of range in histogram
Bins = 1000

#   Get the shared library path
FileDir = os.path.dirname( __file__ )

#   The souce .cpp file of regiongrowing function
CppPath = os.path.join( FileDir, 'regiongrowing.cpp' )

#   The output .so file of regiongrowing function
SOPath = os.path.join( FileDir, 'regiongrowing.so' )

#   Check if .so file is existing
if not os.path.exists( SOPath ):
    raise ModuleNotFoundError( 'Run make regiongrowing before using this module' )

#   Get the module from .so file
cppLib = ctypes.CDLL( SOPath )

#   Get `performRegionGrowing` function inside .so file
performRegionGrowing = cppLib.performRegionGrowing

#   Assign the argument type of `performRegionGrowing` function
performRegionGrowing.argtypes = [ np.ctypeslib.ndpointer( dtype = ctypes.c_double, ndim=2 ), 
                                  ctypes.c_int, 
                                  ctypes.c_int,
                                  ctypes.c_double,
                                  ctypes.c_double  ]

#   Assign the return variable type of `performRegionGrowing` function
performRegionGrowing.restype = ctypes.POINTER( ctypes.c_uint32 )

########################################################
#
#	FUNCTIONS DEFINITIONS
#

def calculateOtsuThresholding ( image: np.ndarray, bins: int = Bins, outMode: str = 'threshold' ):
    '''Calculate the optimize threshold to separate data into 2 groups call the Otsu's algorithm
    
    Parameters
    ------------
    image : ndarray with shape ( imageHeight, imageWidth )
        The input image must be 2D image, not compatible wih 3D image

    bins : int, default = 1000
        The number of points to merge the boundary into this point

    outMode : str, default = 'threshold'
        The parameter control the outputlist of outMode: [ 'threshold', 'region_growing' ]
        - threshold: this mode output only the optimal threshold from calculation
        - region_growing: return [ threshold, optimalMean2 ], both parameters was the argument
        for perform the region growing algorithm  

    Return
    --------
    threshold : float
        The optimal threshold for separation the input image into 2 groups

    optimalMean2 : float
        The mean of cluster 2 ( high values ), or the optimal means from separated data into 2 groups 
    
    '''

    #   Compute histogram of input image
    hist, binEdge = np.histogram( image, bins = bins )

    #   Normalize histogram
        #   Convert count to probability P( i ) = n_i / N
    normHist = np.divide( hist.ravel(), np.sum( hist ) )
    
    #   Calculate middle value of each bin -> ([0, n-1] + [1, n])/2
        #   Note that, the `binEdge` from np.histogram was the boundary of each bin
        #   Code below calculate the middle of eachbin
    binMid = ( binEdge[ :-1 ] + binEdge[ 1: ] ) / 2.
    
    #   Iterate over all thresholds (indices) and get the probabilities w1(t), w2(t)
    weight1 = np.cumsum( normHist )
    
    #   Cumsum backward and invert to get the cumsum of existing 
    weight2 = np.cumsum( normHist[ ::-1 ] )[ ::-1 ]
    
    #   Calculate mean( idx or threshold_t ) for all threshold
    mean1 = np.cumsum( binMid * normHist ) / weight1

    #   Same concept as weight2 cumsum backward and invert
    mean2 = ( np.cumsum(( binMid * normHist )[ ::-1 ]) / weight2[ ::-1 ])[ ::-1 ]
    
    #   Not consider last element due to the last element indicate the threshold is maximum x-axis of histogram
        #   The second class should be 0, but when we use cumsum the first element never be 0
    varianceBetweenClass = weight1[ :-1 ] * weight2[ 1: ] * ( mean1[ :-1 ] - mean2[ 1: ]) ** 2
    
    #   The index with have maximum the variance between class
        #   This index have the optimal parameters to separate 2 groups
    optimalIndex = np.argmax( varianceBetweenClass )
    
    #   Get value of bin at maximum variance between class index
    threshold = binMid[ :-1 ][ optimalIndex ]
    
    #   Output only threshold
    if outMode == 'threshold':
        return threshold
    
    #   Output the region growing parameters
    elif outMode == 'region_growing':

        #   The mean of group 2 is the initial seed
        optimalMean2 = mean2[ optimalIndex ]

        #   The criteria threshold is the optimal threshold from algorithm, and optimal mean of group 2
        return [ threshold, optimalMean2 ]


def segmentRegionFromProbImage( probImage: np.ndarray ):
    '''Perform the region growing searching on probability image, 
    First calculate otsu's thresgolding for region growing parameters
    
    Parameters
    -----------
    probImage : ndarray with shape ( imageHeight, imageWidth )
        The probability image

    Return
    --------
    segmentImage : ndarray with shape ( imageHeight, imageWidth )
        The segmentation image the values refer to the region label
    '''
    #   Calculate the region growing parameters by Otsu thresholding
    thresholdValue = calculateOtsuThresholding( probImage, outMode='region_growing' )

    #   Get the shape of probImage
    imageHeight, imageWidth = probImage.shape

    #   Region growing on probability image
    pointerArray = performRegionGrowing( probImage.astype( np.float64 ), 
                                         imageHeight, 
                                         imageWidth, 
                                         *thresholdValue )
    
    #   Convert the pointer into segment 2D image
        #   The value on `segmentImage` is in range [ 0, nRegion ]
        #   0: not a region ( low probability )
        #   [ 1, nRegion ]: The values assign that this pixel was at `regionLabel`
    segmentImage = np.ctypeslib.as_array( pointerArray, shape = ( imageHeight, imageWidth ) )
    
    return segmentImage