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

from scipy.stats import chi2

from numpy.linalg import inv, det

import math

########################################################
#
#	LOCAL IMPORTS
#

from .Ellipse import Ellipse

from .Segmentation import segmentRegionFromProbImage

########################################################
#
#	FUNCTIONS DEFINITIONS
#

def fitEllipseOnProbImage( probImage, confLvl: float = 0.997 ):
    '''Fit ellipse on probability mask by weighted mean and weighted SD. method. 
        1. Segmentation probability image. create mask of each region
        2. apply the mask to probability image.
        3. replace value on prob image with the outside binary mask to 0
        4. calculate weighted mean and cov_matrix. the weighted mean is the center of ellipse
        5. find the eigenvalue, eigenvector of covariance matrix
        6. calculate rotationAngle and radius from eigen component

    The output `ellipseParams` was filtered. 
    Those parameters will be non-finite number and non-zero radius.
    So the number of output parameters will note equal to the number of mask input. 

    Parameters
    -------------
    probImage : numpy.ndarray with shape ( imageHeight, imageWidth ) 
        The probability image

    confLvl : float, default = 0.997
        The confidence level for fitting with the data

    Return
    ---------
    ellipseObjectList : list of Ellipse object with number of finite ellipse parameters length
        The ellipse object, from ellipse parameter and covariance from fitting ellipse

    Exception
    ----------
    ValueError : The zero candidate regions was input

    '''
    #   Get the shape of probability image
    imageHeight, imageWidth = probImage.shape

    #   Get the segmentation image. The values in pixel refer to the region label
    segmentImage = segmentRegionFromProbImage( probImage )

    #   Get the unique region label
    uniqueRegionLabel = np.unique( segmentImage )

    #   Find number of region label input
        #   The subtraction 1, is not consider region 0.
    nRegion = len( uniqueRegionLabel ) - 1

    #   The input mask come with zero values
    if nRegion <= 0:
        raise ValueError( f'Zero candidate regions' )

    #   Scaling factor determine the covering to data
    factor = chi2.ppf( confLvl, df = 2 )

    #   Create storage array
        #   Mean array with shape ( nRegionidate, 2 )
    meanArr = np.empty( shape = ( nRegion, 2 ) )

        #   Covariance matrix store in array with shape ( nRegionidate, 2, 2 )
    covArr = np.empty( shape = ( nRegion, 2, 2 ) )

        #   Eigenvector array with shape ( nRegionidate, 2, 2 )
    eigenVecArr = np.empty( shape = ( nRegion, 2, 2 ) )

        #   Eigenvalue array with shape ( nRegionidate, 2 )
    eigenValArr = np.empty( shape = ( nRegion, 2 ) )
    
    #   Loop for all candidate mask
    for regionLabel in uniqueRegionLabel:

        #   Skip the label == 0, Which mean the not region values ( default values )
        if regionLabel == 0 :
            continue

        #   Find the position of regionLabel in segmentation image
        labelIndices = np.argwhere( segmentImage == regionLabel )

        #   Create the binary mask
        maskImage = np.zeros( shape = ( imageHeight, imageWidth ), dtype=np.bool_ )

        #   Assign True value to the mask image with labelIndices
        maskImage[ labelIndices[ :, 0 ], labelIndices[ :, 1 ] ] = True
        
        #   Calculate the minimum boundary of mask
        minY, minX = np.min( labelIndices, axis = 0 )

        #   Calculate the maximum boundary of mask
        maxY, maxX = np.max( labelIndices, axis = 0 )

        #   Create coordinate of each position of probability image
        x = np.arange( minX, maxX + 1 ).astype( np.uint32 )
        y = np.arange( minY, maxY + 1 ).astype( np.uint32 )
        X, Y = np.meshgrid( x, y )

        #   Apply mask on probability image
        regionImage = probImage.copy()
        regionImage[ ~maskImage ] = 0
        
        #   Crop only the region area.
            #   MaxY and MaxX must include in the `regionImage`, additional 1 for handle it
        regionImage = regionImage[ minY:maxY + 1, minX:maxX + 1 ]

        #   Sum of weight terms -> \sigma{ w_i }
        sumTerm = np.sum( regionImage )

        #   Find weighted mean
        meanX = np.sum( X * regionImage ) / sumTerm
        meanY = np.sum( Y * regionImage ) / sumTerm

        #   Find weighted variance and covariance
        varX = np.sum( regionImage * np.power( X - meanX, 2 ) ) / sumTerm
        varY = np.sum( regionImage * np.power( Y - meanY, 2 ) ) / sumTerm
        covXY = np.sum( regionImage *  ( X - meanX ) * ( Y - meanY ) ) / sumTerm

        #   Construct covariance matrix
        covMatrix = np.array( [ [ varX , covXY ], 
                                [ covXY, varY ] ] )
        
        #   Calculate Eigenvalue and Eigenvector of covariance matrix
        eigenVal, eigenVec = np.linalg.eig( covMatrix )

        #   Store mean, covariance, eigenvector, eigen values every candidate mask
        meanArr[ regionLabel - 1 ] = [ meanX, meanY ]
        covArr[ regionLabel - 1 ] = covMatrix
        eigenVecArr[ regionLabel - 1 ] = eigenVec
        eigenValArr[ regionLabel - 1 ] = eigenVal

    #   Calculate angle in degrees: shape ( nRegionidate, )
    angle_deg = np.rad2deg( np.arctan( eigenVecArr[ :, 0, 1 ], eigenVecArr[ :, 0, 0 ] ) )

    #   Calculate major and minor radius: shape ( nRegionidate, )
    majorRadius, minorRadius = np.sqrt( np.abs( factor * eigenValArr ) ).swapaxes( 0, 1 )

    #   Stack ( r1, r2, theta )
    stack1dArr = np.stack( [ majorRadius, minorRadius, angle_deg ], axis = 1 )

    #   Concatenate [ ( c_x, c_y ) , ( r1, r2, theta ) ] into 2d array
    ellipseParams = np.concatenate( [ meanArr, stack1dArr ], axis = -1 )

    #   Filter indices the non-finite number from output
    finiteIndices = np.all( np.isfinite( ellipseParams ) == True, axis = 1 )

    #   Apply finite indices
    ellipseParams = ellipseParams[ finiteIndices ]
    covArr = covArr[ finiteIndices ]

    #   Get the indices which the zero radius
    nonZeroIndices = np.logical_and( majorRadius > 0, minorRadius > 0 )
    
    #   Apply non-zero indices
    ellipseParams =  ellipseParams[ nonZeroIndices ]
    covArr = covArr[ nonZeroIndices ]

    #   Construct the ellipse object in list
    ellipseObjectList = [ Ellipse( *ellipseParam, cov=cov ) for ellipseParam, cov in zip( ellipseParams, covArr ) ]

    return ellipseObjectList

def calculateKLDivergence( mean1: np.ndarray, cov1: np.ndarray, 
                           mean2: np.ndarray, cov2: np.ndarray, debugMode: bool = False ):
    '''Calculate the Kullback-Leibler divergence between two multivariate normal distributions
    The equation formula proof here https://statproofbook.github.io/P/mvn-kl.html

    Parameters
    ------------
    mean1 : numpy.ndarray with shape ( nDim, ) 
        Mean of distribution 1

    cov1 : numpy.ndarray with shape ( nDim, nDim ) 
        Covariance matrix of distribution 1

    mean2 : numpy.ndarray with shape ( nDim, ) 
        Mean of distribution 2

    cov2 : numpy.ndarray with shape ( nDim, nDim ) 
        Covariance matrix of distribution 2

    debugMode : bool, default = False
        if True, this function will print each terms of calculation.

    Returns
    --------
    divergenceScore : float
        Kullback-Leibler divergence from distribution 1 to distribution 2 or the reference to observe

    Exceptions
    -----------
    np.linalg.LinAlgError : when the cov_matrix is [ [ 0, 0 ], [ 0, 0 ] ]

    '''
    #   Get dimension of mean
    nDim = len( mean1 )
    
    #   Compute the inverse of covariance matrices
    try:
        inv_cov1 = inv( cov1 )
        
    except np.linalg.LinAlgError:

        #   This case occur when cov_matrix is [ [ 0, 0 ], [ 0, 0 ] ] or small value, this mean the ellipse is zero radius
        #   return inf for ignore them but still consider this index
        return math.inf
    
    #   Compute the trace of the matrix product of inverse covariance matrices
    traceTerm = np.trace( np.matmul( inv_cov1, cov2 ) )
    
    #   Difference between means
    diffMean = mean2 - mean1

    #   Calculate mahalanobis term
    mahalanobisTerm = np.matmul( np.matmul( diffMean, inv_cov1 ), diffMean )

    #   Calculate log covariance ratio
    logCovRatio = np.log( np.divide( det( cov1 ), det( cov2 ) + 1e-15 ) )
    
    #   Compute the KL divergence
    divergenceScore = 0.5 * ( mahalanobisTerm + traceTerm + logCovRatio - nDim )

    if debugMode:
        print( f'1). Mahalanobis term: { mahalanobisTerm }')
        print( f'2). Trace term: { traceTerm }')
        print( f'3). Log cov ratio: { logCovRatio }')
        print( f'4). Divergence : { divergenceScore }')

    return divergenceScore
