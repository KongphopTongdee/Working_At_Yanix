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

########################################################
#
#	LOCAL IMPORTS
#

from homotracking.PyramidFeatureExtraction import PyramidFeatureExtractor

from utils.Bayesian import MultivaraiteGaussianBayesian

########################################################
#
#	GLOBALS
#

#   Total number of pyramid level
NUMPYRAMIDLVL = 5

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
#	CLASS DEFINITIONS
#

class HomogeneousAreaTracker:
    '''Homogeneous area tracker is the submodule integrated the whole homogeneous part.
    The process of tracking process is as followed:
    
    1. Initialize `PyramidFeatureExtractor( image )`
    2. Extract min, max, edge features store in `self.featureExtractor.storage` 
    3. Call `getPyramidFeature()` for get list of feature with length `self.numPyramidLvl`
    4. Calculate homogeneous probability

    '''

    def __init__( self, modelPath: str, numPyramidLvl: int = NUMPYRAMIDLVL ):
        '''Initial homogeneous area tracker by load the Bayesian model from specific path
        Parameters
        -----------
        modelPath : str
            The path store Bayesian model parameters

        numPyramidLvl : int, default = 5
            The number of layer in pyramid structures
        '''
        #   The pyramid level or the layer of gaussian image performed
        self.numPyramidLvl = numPyramidLvl
        
        #   The minimum pixel required to perform the pyramid image
        self.minPixelRequire = 2 ** ( numPyramidLvl - 1 )

        #   The Bayesian model object, loadParams when initialize
        self.model = MultivaraiteGaussianBayesian.loadParams( modelPath )

        #   The featureExtractor object, update in `self.track` function
        self.featureExtractor = None

    def track( self, image: np.ndarray, debugMode: bool = False ):
        '''Tracking the homogeneous area in image the input must be YCbCr color image
        for compatible to the default model parameters.

        Parameters
        -----------
        image : ndarray with shape ( imageHeight, imageWidth, imageDepth )
            The source image with YCrcb color model for the model compatibility

        debugMode : bool, default = False
            if True, return the list of feature array ( `featureList` ), 
                different of joint log-likelihood ( `deltaJllList` ) 
                and homogeneous probability image ( `homoProbImageList` ).
            Otherwise, return only homogeneous probability image

        Return
        -------
        featureList : list of ndarray
            The list of feature array with shape ( nSample, nDim, nFeature ), the index of list refer to the pyramid level

        deltaJllList : list of ndarray
            The different between class ( non-homo & homo ) of joint log-likelihood ( jll ) of each feature
            storing in `feature`. The index of list lead to the pyramid level with 
            each index of list contain the feature array with shape ( nClass, nFeature, imageHeight, imageWidth )

        homoProbImageList : list of ndarray with shape ( imageHeight, imageWidth )
            List of probability images indicate the homogeneous probability of each pixel, each level of pyramid stroing in list

        Exception
        ----------
        ValueError : The input image shape is too small to pergorm Gaussian image pyramid

        '''

        #   Check the minimum shape of input image, must be more than minmum require pixel
        if np.min( image.shape[ :2 ] ) <= self.minPixelRequire:
            raise ValueError( f'The image size is too small to perform Gaussian image pyramid, got { image.shape } ' )

        #   Initialize the featureExtractor object, The inside class perform the Gaussian pyramid process to the image
            #   Input image was array shape ( imageHeight, imageWidth, imageDepth )
        self.featureExtractor = PyramidFeatureExtractor( image, self.numPyramidLvl )

        #   Extract min( SD ), max( SD ) features. The features store in `self.featureExtractor.storage`
        self.featureExtractor.extractFeature( mode = 'minmax' )

        #   Extract edge features. The features store in `self.featureExtractor.storage`
        self.featureExtractor.extractFeature( mode = 'edge' )

        #   Get feature from pyramid: return list of array [  array0( imageHeight * imageWidth, imageDepth, nFeature ), 
            #                                                 ...,  
            #                                                 arrayN( imageHeight * imageWidth, imageDepth, nFeature ) ]
        featureList = self.featureExtractor.getPyramidFeature( flatten = True )

        #   Calculate homogeneous probability
            #   NOTE: The the shape of feature is not match the requirement of `self.getHomogeneousProb` 
                #   but inside `getHomoProbImage function` restructure 
                #   from ( nSample, nDim, nFeature ) into ( nSample, nFeature, nDim )
        deltaJllList, homoProbImageList = self.getHomoProbImage( featureList, returnJll = True )
        
        #   Using for debug, return the necessary data
        if debugMode:
            return featureList, deltaJllList, homoProbImageList
        
        return homoProbImageList
    
    def getHomoProbImage( self, x: np.ndarray, returnJll: bool = False ):
        '''Calculate the homogeneous probability of each layer in the pyramid
        
        Parameters
        ----------
        x : list of feature array [ [ array( nSample, nDim, nFeature ) ] ... [ array( nSample, nDim, nFeature ) ] ]
            The input data for calculate the probability in list each index refer to the level of pyramid
        
        outShape : list of tuple [ ( imageHeight, imageWidth ), ( imageHeight, imageWidth ) ]
            Using for reshape the 1D-probability into probability image

        returnJll : bool, default = False
            if True the output of this function will be list of jll and list of probability

        Return
        -------
        homoProbImageList : list of homogeneous probability image array list[ prob0, ..., probN ], 
            The homogeneous probability image shape ( imageHeight, imageWidth )

        deltaJllList : list of ndarray
            The different between class ( non-homo & homo ) of joint log-likelihood ( jll ) of each feature
            storing in `feature`. The index of list lead to the pyramid level with 
            each index of list contain the feature array with shape ( nClass, nFeature, imageHeight, imageWidth )
        '''

        #   Declare varible for storing output
        homoProbImageList = []
        deltaJllList = []

        #   Get the image shape each pyramid layers. 
            #   Each index will store the shape ( imageHeight, imageWidth )
        pyramidImageShapeList = self.featureExtractor.pyramidShapeList
        
        #   Loop the feature, and output shape in every pyramid level
            #   The data each loop have shape ( nSample, nDim, nFeature )
        for data, imageShape in zip( x, pyramidImageShapeList ):

            #   Reshape data from ( nSample, nDim, nFeature ) into ( nSample, nFeature, nDim )
                #   For compatibility to model.getProb function
            data = data.swapaxes( 1, 2 )

            #   Get the probability with shape ( nSample, 2 )
                #   and get Jll in case of debugging, jll with shape ( nClass, nFeature, nSample )
            jll, prob = self.model.getProb( data, returnJll = True )
            
            #   Reshape the probability ( nSample, 2 ) into ( imageHeight, imageWidth, 2 )
            probImage = prob.reshape( imageShape + ( 2, ) )

            #   Calculate the differential of joint log-likehood of each class, 
                #   the delta with shape ( nFeature, nSample )
            deltaJll = jll[ 0 ] - jll[ 1 ]

            #   Reshape `deltaJll` from shape ( nFeature, nSample ) into ( nFeature, imageHeight, imageWidth )
            deltaJllImage = deltaJll.reshape( -1, imageShape[ 0 ], imageShape[ 1 ] )

            #   Store probability ( only homogeneous prob ) and joint log-likelihood in every pyramid level
            homoProbImageList.append( probImage[ :, :, 1 ] )
            deltaJllList.append( deltaJllImage )

        if returnJll:
            return deltaJllList, homoProbImageList
        
        else:
            return homoProbImageList