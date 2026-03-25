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

import utils.FeatureExtraction as FeatureExtraction

########################################################
#
#	GLOBALS
#

#   The total number of pyramid level
NUMPYRAMIDLVL = 5

#   The kernel size ( symmetric kernel )
KERNELSIZE = 3

#   Create gaussian kernel with KERNELSIZE
GAUSSIANKERNEL = FeatureExtraction.createGaussianKernel( KERNELSIZE )

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

class PyramidFeatureExtractor:
    ''' The PyramidFeatureExtractor perform the pyramid image structure to the source image 
    by convole `GAUSSIANKERNEL` for `numPyramidLvl` time, store in the dictionary ( `self.storage` ).
        
        The pyramid image structure is the structure that each layer of pyramid was 
    scaling down from the higher resolution layer 
    for example layer_0 size ( 1080 x 1080 ) then layer_1 will have size ( 640 x 640 )
    This scaling result from the effect of convolve `GAUSSIANKERNEL` with stride 2

        The image from each layer of pyramid will be extracted to be std image, edge image.
    '''

    def __init__( self, image: np.ndarray, numPyramidLvl: int = NUMPYRAMIDLVL ):

        #   The number of pyramid level
        self.numPyramidLvl = numPyramidLvl

        #   Store the buffer in dictionary, keys: the level of pyramid, vals: the feature dictionary
            #   The storage dictionary structure
            #    ___________________________________________________________________________________________________________
            #   |                        |                                                                                  |
            #   |    Keys: layerIndex    |                                  Values                                          |
            #   |________________________|__________________________________________________________________________________|
            #   |                        |                                                                                  |
            #   |      0 ( layer_0 )     |                                                                                  |
            #   |           .            | dict(                                                                            |
            #   |           .            |        keys: [ 'image', 'stdImage', 'minStdImage', 'maxStdImage', 'edgeImage' ]  |
            #   |           .            |      )                                                                           |
            #   |      n ( layer_n )     |                                                                                  |
            #   |________________________|__________________________________________________________________________________|
        self.storage = dict()
        
        #   The 2D shape of each pyramid level
        self.pyramidShapeList = None

        #   List of the sequence of label that was the keys when update `self.storage`
            #   Using in `getPyramidFeature` function
        self.labelList = []

        #   The Gaussian kernel for smoothing when scaling down
        self.kernel = GAUSSIANKERNEL
        
        #   Initial the pyramid layer by 
            #   convolve gaussian kernel on image ( imageHeight, imageWidth, imageDepth ) 
            #   and extract SD. Image: ( imageHeight, imageWidth )
            #   Store in `self.storage`
        self.initialize( image )

    def initialize( self, image: np.ndarray ):
        '''The initialize function, sequentially create the Gaussian image 
        from high resolution to low resolution, store the result in `self.storage` 
        
        Parameters
        ----------
        image : ndarray of shape ( imageHeight, imageWidth, imageDepth ) for color image
            The original image
        
        '''

        #   Initial layer by source image, extract stdImage of source image
        self.storage[ 0 ] = { 'image': image, 
                              'stdImage': FeatureExtraction.extractStdImage( image ) }
        
        #   Loop in range ( 1, `self.numPyramidLvl` ) to create Gaussian image and SD. image buffer of each pyramid layer
        for pyramidLevel in range( 1, self.numPyramidLvl ):

            #   Convolve gaussian kernel with stride 2, for downsampling each layer of pyramid
                #   Extract SD image by `extractStdImage` function
                #   The storage dict structure // keys: [ pyramidLevel - 1 ] -> mean the previous layer or the higher resolution layer
            self.storage[ pyramidLevel ] = { 'image': FeatureExtraction.convolve3D( input = self.storage[ pyramidLevel - 1 ][ 'image' ],
                                                                                     kernel = self.kernel,
                                                                                     stride = 2 ),
                                       
                                              'stdImage': FeatureExtraction.extractStdImage( self.storage[ pyramidLevel - 1 ][ 'image' ],
                                                                                             stride = 2 ) }
            
        #   Store the each pyramid layer image shape
            #   `dataDict` is the data in dictionary of each pyramid layer
        self.pyramidShapeList = [ dataDict[ 'image' ].shape[ :2 ] for dataDict in self.storage.values() ]
            
    def extractFeature( self, mode: str = 'minmax' ):
        '''Extract the feature each level of pyramid and store extracted features in self.storage,
        moreover, store the keys of dictionary in `self.labelList` each mode of extraction.
        
        Parameters
        -----------
        mode : str, default='minmax'
            The extraction mode: [ 'minmax', 'edge' ]
            - minmax: slide window on stdImage and calculate minimum and maximum of each pixel
            - edge: perform edge detection on image
        '''

        #   `mode == 'minmax'`, for extract min( SD. ), max( SD. ) 
        if mode == 'minmax':

            #   Loop all item in storage, keys is the pyramid level, and values is the buffer dictionary of that pyramid layer
                #   `pyramidData`` is dictionary with buffer of Gaussian image and SD. image
            for pyramidLevel, pyramidData in self.storage.items():

                #   Get the standard deviation image in `pyramidData`
                stdImage = pyramidData[ 'stdImage' ]

                #   Sliding window along stdImage, 
                    #   `windowArr` have shape ( imageHeight, imageWidth, kSize, kSize, imageDepth )
                windowArr = FeatureExtraction.slideWindow3D( stdImage )

                #   Calculate maximum from slidingWindow Array, 
                    #   Axis=( 2,3 ) is to calculate along 8-neighbor axis
                maxStdImage = np.max( windowArr, axis = ( 2, 3 ) )

                #   Calculate minimum from slidingWindow Array
                    #   Axis=( 2, 3 ) is to calculate along 8-neighbor axis
                minStdImage = np.min( windowArr, axis = ( 2, 3 ) )

                #   Store to value `self.storage`
                self.storage[ pyramidLevel ].update( { 'minStdImage': minStdImage, 
                                                       'maxStdImage': maxStdImage } )
            #   Store the keys of features
            self.labelList.extend( [ 'minStdImage', 'maxStdImage' ] )

        #   `mode == 'edge'` for extract edge or convolve the edge detection kernel
        elif mode == 'edge':

            #   Loop all item in storage, keys is the pyramid level, and values is the buffer dictionary of that pyramid layer
                #   `pyramidData`` is dictionary with buffer of Gaussian image and SD. image
            for pyramidLevel, pyramidData in self.storage.items():
                #   Get the image of each layer from `self.storage[ pyramidLevel ]`
                    #   This image mean the source image convolved by Gaussian kernel
                image = pyramidData[ 'image' ]

                #   Get edge image, edge with shape ( imageHeight, imageWidth, imageDepth )
                edgeImage = FeatureExtraction.edgeDetection( image )

                #   Update to pyramid storage
                self.storage[ pyramidLevel ].update( { 'edgeImage': edgeImage } )
            
            #   Store the keys of feature
            self.labelList.append( 'edgeImage' )

    def getPyramidFeature( self, flatten: bool = False ):
        ''' Get the feature in `self.storage` of each pyramid level, 
        the feature depend on the `self.labelList`

        Parameters
        -----------
        flatten : bool, default = False
            If true, the output feature of each layer will flatten
                ( imageHeight, imageWidth, imageDepth, nFeature ) into ( nSample, imageDepth, nFeature )
            otherwise, return the feature with shape ( imageHeight, imageWidth, imageDepth, nFeature ) 

        Return
        --------
        outputList : List of array of feature
            if flatten: [ pyr0( nSample, imageDepth, nFeature ), ... , pyrN( nSample, imageDepth, nFeature ) ]
            else: [ pyr0( imageHeight, imageWidth, imageDepth, nFeature ) , ... , pyrN( imageHeight, imageWidth, imageDepth, nFeature )  ]
            The feature array of each pyramid level store in list structure
        '''

        #   OutputList was the list of array with length according to `self.nPyramidLevel`
        outputList = []

        #   Loop all item in storage, keys is the pyramid level, and values is the buffer dictionary of that pyramid layer
            #   `pyramidData`` is dictionary with buffer of Gaussian image, SD. image and any features extracted
        for pyramidLevel, pyramidData in self.storage.items():
            
            #   Get all feature with specific keys from `self.labelList`
            featureList = [ pyramidData[ label ] for label in self.labelList ]

            #   Stack the list of feature into ( imageHeight, imageWidth, imageDepth, nFeature )
            feautreArr = np.stack( featureList, axis = -1 )

            #   if flatten is true, reshape feature into ( nSample, imageDepth, nFeature ) 
                #   before storing in list
            if flatten:
                imageHeight, imageWidth, imageDepth, nFeature = feautreArr.shape
                feautreArr = feautreArr.reshape( imageHeight * imageWidth, imageDepth, nFeature )

            #   Store the output
            outputList.append( feautreArr )

        #   return outpuList when finishing loop for all pyramid level
        return outputList