#!/usr/bin/env python3
#
# Copyright (C) 2023 Yannix Technologies
#			Written by Thanachart (Ultra) Satianjarukarn
#
########################################################
#
#	STANDARD IMPORTS
#

# from optparse import OptionParser

import argparse

import os

import cv2 as cv

import json

import numpy as np

import matplotlib.pyplot as plt

########################################################
#
#	LOCAL IMPORTS
#

from utils.Image import ImageData

from utils.Ellipse import Ellipse

from roitracking.ROITracker import ROITracker

from regionmatching.RegionMatching import RegionMatching

from homotracking.HomogeneousAreaTracker import HomogeneousAreaTracker


########################################################
#
#	GLOBALS
#

#   Main file directory
CURRENTFILEDIR = os.path.dirname( __file__ )

#   Model path
MODELPATH = os.path.join( CURRENTFILEDIR, 'model/homoModelParams.json' )

#   Input json file directory
INPUTJSONPATH = os.path.join( CURRENTFILEDIR, 'input.json' )

########################################################
#
#	EXCEPTION DEFINITIONS
#

########################################################
#
#	HELPER FUNCTIONS
#

########################################################
#
#	FUNCTIONS DEFINITIONS
#

def getArgumentFromUser():
    '''Get index from user via command line argument for access the `input.json`.
    Use the index as a keys of dictionary to specify the input arguments
    
    Return
    -------
    imageDir: str
        The directory store the image in sequence

    ellipseParam: list
        The ellipse parameters involved [ c_x, c_y, r1, r2, angle_deg ]

    startFrame: int
        The number of frame to start the system

    nCluster: int
        The number of cluster in the ROI
    '''  
    #   Add parser
    parser = argparse.ArgumentParser( description = "usage: %prog index [options path]" )
    
    #   Add argument,store index at 'index'.
        #   The paser require argument form user, if user doesn't fill in it gonna be error.
    parser.add_argument( 'index', action = 'store', type = int, help = 'Input the index of .json data to tracking' )
    
    #   Add argument, store image directory at 'inputImagePath'.
        #   The paser require argument form user, if user doesn't fill in it gonna be error.
    parser.add_argument( 'inputImagePath', action = 'store', nargs='+', type = str, help = 'Input the image directory' )

    #   Add argument, store image directory at 'inputSaveTempImagePath'.
        #   The paser require argument form user, if user doesn't fill in it gonna be error.
    parser.add_argument( 'inputSaveTempImagePath', action = 'store', type = str, help = 'Input the save temp image directory' )

    #   Add argument, store image directory at 'inputSaveSubFeatureImagePath'.
        #   The paser require argument form user, if user doesn't fill in it gonna be error.
    parser.add_argument( 'inputSaveSubFeatureImagePath', action = 'store', type = str, help = 'Input the save sub feature image directory' )

    #   Get arguments
    args = parser.parse_args()
    
    #   Get the input index
    inputIdx = args.index

    #   Assign the image directory from user
    imageDir = args.inputImagePath

    #   Assign the save temp image directory from user
    saveTempImageDir = args.inputSaveTempImagePath

    #   Assign the save sub feature image directory from user
    saveSubFeatureImageDir = args.inputSaveSubFeatureImagePath

    #   Read data from the json file
    with open( INPUTJSONPATH, mode = 'r' ) as f:

        #   Get the dictionary of input
        inputData = json.load( f )

    #   Extract the input from specific keys from input index access on dictionary of `inputData`
    category, ellipseParam, startFrame, nCluster = inputData[ inputIdx ].values()

    #   `ellipseParam` contain [ ( c_x, c_y ), r1, r2, angle_deg ] flatten into list of 5 parameters
    center, r1, r2, angle_deg = ellipseParam
    ellipseParam = [ center[ 0 ], center[ 1 ], r1, r2, angle_deg ]

    return imageDir, saveTempImageDir, saveSubFeatureImageDir, ellipseParam, startFrame, nCluster

if __name__ == '__main__':

#####################################################################################################################################

    #	Get the input of the system
    imageDir, saveTempImageDir, saveSubFeatureImageDir, ellipseParam, startFrame, nCluster = getArgumentFromUser()

    #   Get list of image path from input image directory
        #   Select the strating index with startFrame parameter 
    imagePathList = sorted( imageDir )[ startFrame: ]

	######################## TRAINING PHASE ########################

    #	Read training image from the first frame of user input directory
    trainingImage = ImageData( imagePath=imagePathList[ 0 ] )

	#	Construct Ellipse from user input for store into the referenceEllipse
        #   The referenceEllipse mean the ellipse using to be the reference of regionMatching system
		#	The input ellipseParam consist of [ centerX, centerY, majorRadius, minorRadius, angle_deg ]
    referenceEllipse = Ellipse( *ellipseParam )

    #   Get position array inside Ellipse, for training ROI color model
    posInsideEllipse = referenceEllipse.getPointInsideEllipse( )
    
    #   Get position array outside Ellipse, for training ROI color model
    posOutsideEllipse = referenceEllipse.getPointOutsideEllipse( trainingImage.size() )

    #	Train ROI color model
    roiTracker = ROITracker( trainingImage, posInsideEllipse, posOutsideEllipse, nCluster )

    #	Declare region matcher object, input is the list of ellipse object
    regionMatcher = RegionMatching( [ referenceEllipse ] )

	######################## TESTING PHASE ########################

	#	Declare homoTracker object, load model
    homoTracker = HomogeneousAreaTracker( modelPath = MODELPATH )
    
    #	Declare subregionMatcher object
    subRegionMatcher = RegionMatching( refEllipseList = None )

	#	loop for all imagePath in the list of image path
    for imageIdx, imagePath in enumerate( imagePathList ):
        
        print( f'\nStart tracking { imagePath }')
    
        #	Read tracking image from the image path parameters
        trackingImage = ImageData( imagePath = imagePath )

		#	Get the region of interested probability image
        roiProbImage = roiTracker.track( trackingImage.imageRGB )

        try:
            #	Match the ROI region, return the best match ellipse object in list
            roiEllipseList = regionMatcher.match( roiProbImage )

        #   The ValueError when function dont have the candidate ellipse
        except ValueError:

            print( '   warnings.warn Region matching AssertionError' )

            #   Skip this image
            continue

        print( 'Done matching ROI region')

        #####################################################################################
        _tempImage = trackingImage.imageRGB.copy()
        c_x, c_y, r1, r2, angle_deg = roiEllipseList[ 0 ].params
        cv.ellipse( _tempImage, ( int( c_x ), int( c_y ) ), ( int( r1 ), int( r2 ) ), 360-angle_deg, 0, 360, color =( 1, 0, 0 ) , thickness=3 )
        plt.imsave( fname=f'{ saveTempImageDir }/{ str( imageIdx ).zfill( 3 ) }.jpg', arr=_tempImage, cmap='viridis' )
        #####################################################################################

        #	Get bounding box parameter from roi ellipse object
            #   Get first index because the roi ellipse was list with length 1 )
        x, y, w, h = roiEllipseList[ 0 ].getBoundingBoxParam( )

        #	Crop image from the boundary of roiEllipse
        cropImage = trackingImage.imageYCrCb[ y:y+h, x:x+w ]
        
        try:
            #	Get the homogeneity probability image ( list of probability image in each pyramid level )
            homoProbImage = homoTracker.track( image = cropImage )
            print( 'Done Homogeneous area tracking' )

        #   The ValueError when the the size of cropImage is less than 16
            #   The size of image must larger than 16 due to the 5 pyramid level ( n ** ( nPyramidLvl -1 ) )
        except ValueError:

            print( f'   warnings.warn Homogeneous model AssertionError, on image shape: { cropImage.shape }' )
            
            #   Skip current loop
            continue
            
        #	Match the subfeatures region, return the best match of subfeature ellipse
            #	the number of output is the same as the number of reference from frame n-1
        subFeatureEllipseList = subRegionMatcher.match( homoProbImage[ 0 ] )

        #####################################################################################
        for subFeatureEllipse in subFeatureEllipseList:
            c_x, c_y, r1, r2, angle_deg = subFeatureEllipse.params
            cv.ellipse( _tempImage, ( int( x+c_x ), int( y+c_y ) ), ( int( r1 ), int( r2 ) ), 360-angle_deg, 0, 360, color =( 0, 1, 0 ) , thickness=3 )
        # plt.imsave( f'{ saveSubFeatureImageDir }/{ str( imageIdx ).zfill( 3 ) }.jpg', arr=_tempImage )
        #####################################################################################

        print( f'   number of sub region: {  subRegionMatcher.nRefEllipse  }\n')

# ###########################################################################################################################
