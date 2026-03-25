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

from scipy.ndimage import convolve

########################################################
#
#	LOCAL IMPORTS
#

########################################################
#
#	GLOBALS
#

#   SD. values for create Gaussian kernel
SIGMA = 1

#   Default padding mode for sliding window and colvove function
DEFAULTPADMODE = 'reflect'

#   Default stride number
DEFAULTSTRIDENUMBER = 1

#   Default kernel size using for slidingWindow function
DEFAULTKERNELSHAPE = ( 3, 3 )

#   Default mode for edge detection
DEFAULTEDGEDETECTIONMODE = 'sobel3D'

#   Gradient kernel 3x3 on x-axis
GRADIENTKERNEL_X = np.array( [[ -1, 0, 1 ], [ -2, 0, 2 ], [ -1, 0, 1 ]] )

#   Gradient kernel 3x3 on y-axis
GRADIENTKERNEL_Y = GRADIENTKERNEL_X.T

#   Declare variable to store Gaussian kernel; initial when used
    #   Potentially use when call `edgeDetection()`
GAUSSIANKERNEL = None

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

########################################################
#
#	FUNCTIONS DEFINITIONS
#

def createGaussianKernel( size: int, sigma: float = SIGMA ):
    '''Create Gaussian kernel function

    Parameters
    -----------
    size : int
        The size of the output symmetric kernel

    sigma : float, default = 1
        The sigma of the modeling Gaussian kernel

    Return
    --------
    kernel : ndarray with shape ( size, size )
        The gaussian kernel with the symetric Gaussian weight respective on sigma
    
    '''

    #   Scaling term
    scalingTerm = ( 1 / ( 2 * np.pi * sigma**2 ) )

    #   Mahalanobis term
    mahalanobisTerm = lambda y, x: np.exp( -( ( x - size // 2 )**2 + ( y - size // 2 )**2 ) / ( 2 * sigma**2 ) )
    
    #   Create the Gaussian kernel
    kernel = np.fromfunction( lambda y, x: scalingTerm * mahalanobisTerm( y, x ), ( size, size ), dtype = np.float32 ) 
    
    #   Nomalize kernel
    kernel /= np.sum( kernel )

    return kernel

def slideWindow2D( input : np.ndarray,
                   kernelShape: tuple = DEFAULTKERNELSHAPE, 
                   padMode: str = DEFAULTPADMODE, 
                   stride: int = DEFAULTSTRIDENUMBER
                  ):
    '''Slide window on the 2D-input array with the window size equal to kernel size, sliding on the 2D input

    Parameters
    -----------

    input : ndarray with shape ( imageHeight, imageWidth )
        The input array or the source for sliding window on..
    
    kernelShape : tuple, default = ( 3, 3 )
        The size of kernel using for determine the shape of window to sliding on the input.
        

    padMode : str, default = 'reflect'
        The padding mode from the `np.pad`, if padMode is None the output shape will not equal to the source.
        see the np.pad document here: https://numpy.org/devdocs/reference/generated/numpy.pad.html

    stride : int, default = 1
        The number of strding or skip the sliding window with the number of stride

    Return
    -------
    windowArr: ndarray with shape ( imageHeight, imageWidth, kSize, kSize )
        The window array from sliding kernel with kSize, the windowArr represent ( kSize**2 - 1 ) neighbor pixel on each pixel

    Exception
    ----------
    ValueError : the input dimension not compatible with this function ( not 2D input )

    '''

    #   Assert the dimension of input, must be 2 dimensions
    if input.ndim != 2:
        raise ValueError( f'Incompatible with shape{ input.shape }, the input must be 2-dimension' )

    #   If padMode was input use as the parameter to np.pad, calculate pading size
    if padMode is not None:

        #  Calculate padding size from kernelShape
        padSize_y = kernelShape[ 0 ] // 2
        padSize_x = kernelShape[ 1 ] // 2

        #   Padding the input
        input = np.pad( input, ( ( padSize_y, padSize_y ), ( padSize_x, padSize_x ) ), mode = padMode )

    #   Slide window with input kernel shape along 2D input
    windowArr = np.lib.stride_tricks.sliding_window_view( input, kernelShape )

    #   Stride or skip the unconsidered index, out shape ( _, _, kernelSize, kernelSize )
    windowArr = windowArr[ ::stride, ::stride ]

    return windowArr
    
def slideWindow3D( input : np.ndarray,
                   kernelShape: tuple = DEFAULTKERNELSHAPE, 
                   padMode: str = DEFAULTPADMODE, 
                   stride: int = DEFAULTSTRIDENUMBER
                  ):
    '''Slide window on the 3D-input array with the window size equal to kernel size

    Parameters
    -----------

    input : ndarray with shape ( imageHeight, imageWidth, imageDepth )
        The input array or the source for sliding window on
    
    kernelShape : tuple, default = ( 3, 3 )
        The size of kernel using for determine the shape of window to sliding on the input.
    
    padMode : str, default = 'reflect'
        The padding mode from the `np.pad`, if padMode is None the output shape will not equal to the source.
        see the np.pad document here: https://numpy.org/devdocs/reference/generated/numpy.pad.html

    stride : int, default = 1
        The number of strding or skip the sliding window with the number of stride
    Return
    -------
    windowArr: ndarray with shape ( imageHeight, imageWidth, kSize, kSize, imageDepth )
        The window array from sliding kernel with kSize, the windowArr represent ( kSize**2 - 1 ) neighbor pixel on each pixel
    
    Exception
    ----------
    ValueError : the input dimension not compatible with this function ( not 3D input )

    '''

    #   Get the input shape
    inputShape = input.shape
    
    #   Assert the dimension of and input, must be 3 dimensions
    if input.ndim != 3:
        raise ValueError( f'Incompatible with shape{ inputShape }, the input must be 3-dimension' )

    #   Get the depth of input
    _, _, inputDepth = inputShape

    #   `WindowArr` list of array store output from slideWindow2D, call slideWindow2D every channel of input to slide window on
    slidingWindowList = [ slideWindow2D( input[ :, :, channelIdx ], kernelShape, padMode, stride ) for channelIdx in range( inputDepth )]

    #   Stack window each channel into array with shape ( imageHeight, imageWidth, kSize, kSize, imageDepth )
    windowArr = np.stack( slidingWindowList, axis = -1 )
        
    return windowArr

def extractStdImage( image: np.ndarray, 
                     kernelShape: tuple = DEFAULTKERNELSHAPE, 
                     padMode: str = DEFAULTPADMODE, 
                     stride: int = DEFAULTSTRIDENUMBER
                  ):
    '''Extract the standarad deviation of the image given, and the number of neighbor depend on the `kernelShape`, 
    calculate all the pixel in image. The output will be the stdImage with the same size as image input.

    Parameters
    -----------
    image : ndarray with shape ( imageHeight, imageWidth, imageDepth )
        The input image for calculating the standarad deviation image.
    
    kernelShape : tuple, default = ( 3, 3 )
        The size of kernel using for determine the shape of window to sliding on the input.

    padMode : str, default = 'reflect'
        The padding mode from the `np.pad`, if padMode is None the output shape will not equal to the source.
        see the np.pad document here: https://numpy.org/devdocs/reference/generated/numpy.pad.html

    stride : int, default = 1
        The number of strding or skip the sliding window with the number of stride
    
    Return
    -------
    stdImage: ndarray with shape ( imageHeight, imageWidth, imageDepth )
        The standard deviation image, the neighbor for find the SD values depend on the `windowArr` shape

    Exception
    ----------
    ValueError : error when the input dimension was not 2 or 3

    '''
    #   Assert the dimension of and input, must be 2 or 3 dimensions
    if image.ndim != 2 and image.ndim != 3:
        raise ValueError( f'Check your input image, the dimension did not match' )

    #   If input was 2D image, utilize slidWindow2D to get 
        #   `windowArr` with shape ( imageHeight, imageWidth, kSize, kSize )
    if image.ndim == 2:
        windowArr = slideWindow2D( image, kernelShape, padMode, stride )

    #   If input was 3D image, utilize slidWindow3D to get
        #   `windowArr` with shape ( imageHeight, imageWidth, kSize, kSize, imageDepth )
    elif image.ndim == 3:
        windowArr = slideWindow3D( image, kernelShape, padMode, stride )


    #   Calculate the standard deviation image
    stdImage = np.std( windowArr, axis = ( 2, 3 ) )

    return stdImage

def convolve2D( input, kernel: np.ndarray, padMode: str = DEFAULTPADMODE, stride: int = DEFAULTSTRIDENUMBER ):
    '''Convolve the kernel on the 2D-input array

    Parameters
    -----------

    input : ndarray with shape ( imageHeight, imageWidth )
        The input array or the source for convolution
    
    kernel : ndarray with shape ( kernelHeight, kernelWidth )
        The kernel with specific weight to apply on image

    padMode : str, default = 'reflect'
        The padding mode from the `np.pad`, if padMode is None the output shape will not equal to the source.
        see the np.pad document here: https://numpy.org/devdocs/reference/generated/numpy.pad.html

    stride : int, default = 1
        The number of strding or skip the sliding window with the number of stride

    Return
    -------
    convArr : ndarray with shape ( imageHeight, imageWidth )
        The result of convolution, if the stride is not None the output will skip every number of stride.

    Exception
    ----------
    ValueError : the input dimension not compatible with this function ( must be 2D input )
    
    '''
    #   Assert the dimension of input, must be 2 dimensions
    if input.ndim != 2:
        raise ValueError( f'Incompatible with shape{ input.shape }, the input must be 2-dimension' )

    #   Convolve the input with the kernel, convArr with shape ( imageHeight, imageWidth )
    convArr = convolve( input, kernel, mode = padMode )

    #   Stride image, skip every `stride` index
    convArr = convArr[ ::stride, ::stride ]

    #   Return the array with shape ( imageHeight, imageWidth )
    return convArr

def convolve3D( input, kernel: np.ndarray, padMode:str = DEFAULTPADMODE, stride:int = DEFAULTSTRIDENUMBER ):
    '''Convolve the kernel on the 3D-input array by for-loop

    Parameters
    -----------

    input : ndarray with shape ( imageHeight, imageWidth, imageDepth )
        The input array or the source for convolution
    
    kernel : ndarray with shape ( kernelHeight, kernelWidth )
        The kernel with specific weight to apply on image

    padMode : str, default = 'reflect'
        The padding mode from the `np.pad`, if padMode is None the output shape will not equal to the source.
        see the np.pad document here: https://numpy.org/devdocs/reference/generated/numpy.pad.html

    stride : int, default = 1
        The number of strding or skip the sliding window with the number of stride

    Return
    -------
    output : ndarray with shape ( imageHeight, imageWidth, imageDepth )
        The result of convolution, if the stride is not None the output will skip every number of stride.
        
    Exception
    ----------
    ValueError : the input dimension not compatible with this function ( must be 3D input )
    
    '''
    #   Assert the dimension of input, must be 3 dimensions
    if input.ndim != 3:
        raise ValueError( f'Incompatible with shape{ input.shape }, the input must be 3-dimension' )

    #   Get input depth
    _, _, inputDepth = input.shape

    #   Store output from convolve2D in list, call convolve2D every channel of image
    convList = [ convolve2D( input[ :, :, channelIdx ], kernel, padMode, stride ) for channelIdx in range( inputDepth ) ]

    #   Stack the array along last channel
    convArr = np.stack( convList, axis = -1 )

    return convArr

def edgeDetection( image: np.ndarray, mode: str = DEFAULTEDGEDETECTIONMODE, smooth: bool = True ):
    '''Convolve the edge detection kernel on the input image

    Parameters
    ------------
    image : ndarray with shape ( imageHeight, imageWidth )
        The source image for perform edge detection. Specially for mode = 'sobel3D', the input image must be 3D image
    
    mode : str, default = 'sobel3D'
        The mode of edge detection consist of [ 'sobel', 'sobel3D' ]
        - 'sobel': The original sobel edge detection, using on the gray-scale image
        - 'sobel3D': The extended from sobel, by detect edge of each channel of image,
                     The input of this function must be color image.

    smooth : bool, default = True
        The smooth flag, if `True` the gaussian smoothing 3x3 will performed before edge detection

    Return
    ----------
    edgeImage : ndarray with shape ( imageHeight, imageWidth )
        The magnitude of the gradient, 
        if mode == 'sobel3D' the output shape will be ( imageHeight, imageWidth, imageDepth )

    Exception
    ----------
    ValueError : raise error when the input image can not perform by the selected mode
    '''
    #   Using the `GaussianKerenl` from the globabl variable
    global GAUSSIANKERNEL

    #   Get the dimension of input image
    imageDimension = image.ndim
    
    #   If mode didn't match the image provided, raise value error
    if ( mode == 'convolve3D' ) and ( imageDimension != 3 ):
        raise ValueError( f'The input image dimension and the edge detection mode did not match' )

    #   If smooth = True, convolve by Gaussian kernel
    if smooth:

        #   Initial the GAUSSIANKERNEL
        if GAUSSIANKERNEL is None:
            GAUSSIANKERNEL = createGaussianKernel( 3 )

        #   Convolve input image, depend on the image dimension
        if imageDimension == 3:
            image = convolve3D( image, GAUSSIANKERNEL, padMode = DEFAULTPADMODE )
        else:
            image = convolve2D( image, GAUSSIANKERNEL, padMode = DEFAULTPADMODE )

    #   Sobel 2D mode
    if mode == 'sobel':

        #   Convolve on image on x and y axis, the gradient kernel on was the global variable
        gradX = convolve2D( image, GRADIENTKERNEL_X, padMode = DEFAULTPADMODE )
        gradY = convolve2D( image, GRADIENTKERNEL_Y, padMode = DEFAULTPADMODE )

        #   Calculate the magnitude of the gradient result in x & y axis
            #   np.hypot: sqrt(x1**2 + x2**2)
        edgeImage = np.hypot( gradX, gradY )

        return edgeImage
    
    #   Sobel 3D mode
    elif mode == 'sobel3D':

        #   Convolve on image on x and y axis, the gradient kernel on was the global variable
        gradX = convolve3D( image, GRADIENTKERNEL_X, padMode = DEFAULTPADMODE )
        gradY = convolve3D( image, GRADIENTKERNEL_Y, padMode = DEFAULTPADMODE )

        #   Calculate the magnitude of the gradient result in x & y axis
            #   np.hypot: sqrt( x1**2 + x2**2 )
        edgeImage = np.hypot( gradX, gradY )

        return edgeImage

def scaleMinMax( data, axis = None ):
    '''Scale data with min,max method

    Parameters
    -----------
    data : ndarray
        The original data for normalize
    
    axis : tuple
        The tuple of axis to apply min and max along

    Return
    ---------
    output : ndarray
        The scaled data from the given data
    
    '''
    #   Calculate minimum along axis input
    min = np.min( data, axis = axis )

    #   Calculate maximom along axis input
    max = np.max( data, axis = axis )

    #   Return the normalize, scaled data with the same shape of input data
    return ( data - min ) / ( max - min + 1e-15 )
