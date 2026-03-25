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

from utils.EllipseHelper import fitEllipseOnProbImage

from utils.FeatureExtraction import scaleMinMax

########################################################
#
#	HELPER FUNCTION
#

def calculateCosineSimilarity( x, y ):
    '''Calculate the similarity of vector using dot product then normalize the vector, 
    see also https://scikit-learn.org/stable/modules/metrics.html#cosine-similarity
    
    Parameters
    -----------
    x : ndarray with shape ( 1, nFeature )
        Vector array

    y : ndarray with shape ( 1, nFeature )
        Vector array

    Returns
    -------
    cosineSimilarity : float, scalar value
        The cosine similarity values 
        
    '''
    
    #   Compute dot product of 2 vector
    similiarity = np.dot( x, y.T )

    #   Normalize by the size of 2 vector
    normalizeTerm = np.linalg.norm( x ) * np.linalg.norm( y )

    #   Calculate cosine similarity
    cosineSimilarity = ( similiarity / normalizeTerm ).squeeze()

    return cosineSimilarity


########################################################
#
#	CLASS DEFINITIONS
#

class RegionMatching:
    '''The RegionMatching class using for matching the region from probability image. 
    First fittingEllipseOnProbImage, then matching each region by 3 similarity score.
    [ center_score, radius_score, ratation_score ]
    This class require the reference ellipse object store in list ( `self.refEllipseList` ) to be the reference ellipse
    for matching the candidate ellipse.
    '''
    def __init__( self, refEllipseList: list ):
        '''
        Parameters
        -----------
        refEllipseList : list
            The list of ellipse object using for reference in matching process
        '''
        #   Store reference ellipse object in this class
            #   Initial in the training phase by storage the ROI reference Gaussian parameters from Ellipse parameters from user
            #   Convert the ellipse parameters into Gaussian parameters then store in the class
        self.refEllipseList = refEllipseList

        #   Number of reference ellipse object, using for loop in self.selectBestFitEllipseParams function
        self.nRefEllipse = 0

        #   If there are any reference ellipse object list, find the number of reference
        if self.refEllipseList:

            self.nRefEllipse = len( refEllipseList )

            #   Declare the different position vector of previous frame with shape ( nRef, 2 )
                #   Update on matching process
            self.diffPosVec = np.zeros( shape = ( self.nRefEllipse, 2 ) )

        #   The weight for scale the score
        self.weightScore = np.array( [ 0.6, 0.3, 0.1 ] )

        #   The flag for note that, the first matching or not
            #   The first frame match on this system was the re-generated process
        self.isFirstMatch = True

        #   The number of frame that already tracked
        self.numberFrameTracked = 0


    def match( self, probImage: np.ndarray, debugMode: bool = False ):
        '''Matching the region from probability image,
        1. Fit ellipse on probability image return the ellipse object store in list
        2. Calculate the similarity score from the candidate ellipse 
           using the reference Ellipse object store from training phase 
        After matching process done, replace the old `refEllipseList` with the best match ellipse object
        
        Parameters
        -----------
        probImage : ndarray with shape ( imageHeight, imageWidth )
            The probability image
        
        debugMode : bool, default = False
            if True, the function will return bestFitEllipseList, bestSimilarityScore.
            Otherwise, return only bestFitEllipseList

        Return
        --------
        bestMatchEllipseList : list of ellipse object
            The best match ellipse object store in list, the length of list equal to `self.refEllipseList`

        bestSimilarityScore : ndarray with shape ( `self.nRefEllipse`, )
            The most score from `self.refEllipseList`
        '''

        #   Fit ellipse on probability image, return the ellipse object store in list 
        ellipseObjectList = fitEllipseOnProbImage( probImage, confLvl=0.95 )

        #   No reference ellipse provided in the initial
        if self.refEllipseList is None:

            #   Store all candidate params at n frame into self.refEllipseList, 
                #   Using for tracking in n+1 frame 
            self.refEllipseList = ellipseObjectList

            #   Store number of reference ellipse
            self.nRefEllipse = len( self.refEllipseList )

            #   Declare the different position vector of previous frame with shape ( nRef, 2 )
                #   Update on matching process
            self.diffPosVec = np.zeros( shape = ( self.nRefEllipse, 2 ) )

            return self.refEllipseList
    
        #   Select best fit Gaussian parameters to the `self.refEllipseList`
        bestMatchEllipseList, bestSimilarityScore = self.selectBestFitEllipse( candEllipseObjectList = ellipseObjectList, 
                                                                               debugMode = debugMode )

        #   Update reference ellipse list and number of reference ellipse and diff pos
        self.nRefEllipse = len( bestMatchEllipseList )
        
        #   The array range from 0 to number of reference
        nRefRangeArr = np.arange( self.nRefEllipse )

        #   If the system track more than 1 image,
            #   Calculate the different position of reference ellipse parameters
        if self.numberFrameTracked > 1 :
            
            #   Loop for all ellipse to calculate the different position P_(n-1) - P_(n-2)
            for refIdx, matchEllipse, refEllipse in zip( nRefRangeArr, bestMatchEllipseList, self.refEllipseList ):
                self.diffPosVec[ refIdx ] = matchEllipse.center - refEllipse.center
            
        #   Store the bestMatchEllipse list
        self.refEllipseList = bestMatchEllipseList

        #   Plus number of tracking time
        self.numberFrameTracked += 1
        
        #   Using on debug mode for return the bestMatchEllipseList, similarity score
        if debugMode:
            return bestMatchEllipseList, bestSimilarityScore
        
        return bestMatchEllipseList
    
    def selectBestFitEllipse( self, candEllipseObjectList: list, debugMode: bool = False ):
        '''Using ellipse similiarity score for matching `self.refEllipseList`, 
        the ellipse similarity score involved 3 component
        1. centerDistance: L2_norm( p_ref + diff( p ), p_cand ) 
           Then scale minmax all candidate to be in range [ 0, 1 ]
           convert distance into score: ( 1 - scaleDistance )

        2. radiusDistance: L2_norm( r_ref, r_cand )
           Then scale minmax all candidate to be in range [ 0, 1 ]
           convert distance into score: ( 1 - scaleDistance )
           
        3. rotationScore: similarity( minor_radius_ref, minor_radius_cand )

        The ellipse similarity score was in range [ 0, 1 ], more values indicating the similiarity ellipse

        Parameters
        -----------
        candEllipseObjectList : list
            The candidate Ellipse object store in list, 
            the length of this list assume to be the number of candidate.

        debugMode : bool, default = False
            If true print the necessary information

        Return
        -------
        bestMatchEllipseList : list of Ellipse object
            The best matching Ellipse object from `self.refEllipseList`, 
            the length of this list equal to the `self.nRefEllipse`

        bestSimilarityScore : ndarray with shape ( `self.nRefEllipse`, )
            The most score from `self.refEllipseList`

        Note
        -----
        The refernce can also say frame n-1, and the candidate is current frames

        Exception
        ----------
        ValueError : The number of candidate parameters is less than 1 
        
        '''

        #   Get the number of candidate Ellipse
        nCand = len( candEllipseObjectList )

        #   Candidate paramters is 0, mean no finite ellipse from filtering on `fitEllipseOnProbImage` function
        if nCand <= 0:
            raise ValueError( f'The candidate Ellipse object is zero, check candidateParams input' )

        #   Declare center distance matrix with shape ( nRef, nCand )
        centerDistanceArr = np.empty( shape=( self.nRefEllipse, nCand ) )

        #   Declare radius distance matrix with shape ( nRef, nCand )
        radiusDistanceArr = np.empty( shape=( self.nRefEllipse, nCand ) )

        #   Declare rotation score matrix with shape ( nRef, nCand )
        rotationScore = np.empty( shape=( self.nRefEllipse, nCand ) )

        #   Loop for all number of reference params
        for refIdx in range( self.nRefEllipse ):
            
            #   Get the reference ellipse object
            refEllipse = self.refEllipseList[ refIdx ]

            #   Convert the rotation degrees into radius
            refAngle_rad = np.deg2rad( refEllipse.angle_deg )

            #   Construct radius projection [ r1cos(theta), r1sin(theta) ]
                #   Array with shape ( 1, 2 )
            refProjectionRadius = np.array( [ [ 
                                                refEllipse.majorRadius * np.cos( refAngle_rad ), #  r1 * cos( theta )
                                                refEllipse.majorRadius * np.sin( refAngle_rad )  #  r1 * sin( theta )
                                              ] ] )
            
            #   Get the radius vector with shape ( 2, 1 )
            refRadiusVector = np.array( [ refEllipse.majorRadius, 
                                          refEllipse.minorRadius ] )[ :, np.newaxis ]

            #   Estimate the current position using the velocity from previus frame
                #   Reshape from array ( 2, ) into array ( 2, 1 ) 
            estimateRefCenter = ( np.array( refEllipse.center ) + self.diffPosVec[ refIdx ] )[ :, np.newaxis ]

            #   Loop for all number of candidate params
            for candIdx in range( nCand ):

                #   Get the candidate ellipse object
                candEllipse = candEllipseObjectList[ candIdx ]

                #   Convert the rotation degrees into radius
                candAngle_rad = np.deg2rad( candEllipse.angle_deg )

                #   Construct radius projection [ r1cos(theta), r1sin(theta) ]
                    #   Array with shape ( 1, 2 )
                candProjectionRadius = np.array( [ [ 
                                                    candEllipse.majorRadius * np.cos( candAngle_rad ), #  r1 * cos( theta )
                                                    candEllipse.majorRadius * np.sin( candAngle_rad )  #  r1 * sin( theta )
                                                    ] ] )
                
                #   Get the radius vector with shape ( 2, 1 )
                candRadiusVector = np.array( [ candEllipse.majorRadius, 
                                               candEllipse.minorRadius ] )[ :, np.newaxis ]

                #   Get the candidate ellipse center
                    #   Reshape from array ( 2, ) into array ( 2, 1 )
                candCenter = np.array( candEllipse.center )[ :, np.newaxis ]

                #   Calculate the center distance between ( ref, cand )
                centerDistanceArr[ refIdx, candIdx ] = np.linalg.norm( estimateRefCenter - candCenter )

                #   Calculate the radius distance between ( ref, cand )
                radiusDistanceArr[ refIdx, candIdx ] = np.linalg.norm( refRadiusVector - candRadiusVector )

                #   Calculate the rotation score
                rotationScore[ refIdx, candIdx ] = calculateCosineSimilarity( refProjectionRadius, candProjectionRadius )

        #   Normalize the distance metrics into range [ 0, 1 ]
            #   Then convert distance to score = ( 1 - distance )
        centerScoreArr = 1 - scaleMinMax( centerDistanceArr )
        radiusScoreArr = 1 - scaleMinMax( radiusDistanceArr )

        if not self.isFirstMatch:
            #   Find average score, axis=0 is to find mean along the component
            similarityScoreArr = np.sum( [  centerScoreArr * self.weightScore[ 0 ], 
                                            radiusScoreArr * self.weightScore[ 1 ], 
                                            rotationScore  * self.weightScore[ 2 ]  ], axis=0 )

        else:
            #   The first frame track using only the center parameters to define the best match
            similarityScoreArr = centerScoreArr

            #   Update state to False
            self.isFirstMatch = False

        #   Get sorting indices
        indices = np.argsort( similarityScoreArr )

        #   Flip the indices from ascending to decending
        indices = np.flip( indices, axis=1 )

        #   Get the best match ellipse object, and bestSimilarity score
            #   by take the input list with the index of the first row of indices
        bestMatchEllipseList = np.take( candEllipseObjectList, indices[ :, 0 ] )
        bestSimilarityScore = np.take_along_axis( similarityScoreArr, indices, axis=1 )[ :, 0 ]

        #   Using when the debugMode arg is True
        if debugMode:

            #   Convert reference ellipse object list, into parameters list
            _refEllipseParamList = [ refEllipse.params for refEllipse in self.refEllipseList ]
            print( f'reference param: { _refEllipseParamList }' )

            #   Convert best match ellipse object list into parameters list
            _matchEllipseParamList = [ matchEllipse.params for matchEllipse in bestMatchEllipseList ]
            print( f'Match param: { _matchEllipseParamList }' )

            #   Print the score: [ 'center_score', 'radius_score', 'rotation_score' ]
                #   Those score is the score which not weighted yet
            print( f'Center Score: {   np.take_along_axis( centerScoreArr , indices, axis=1 )[ :, 0 ] }' )
            print( f'Radius Score: {   np.take_along_axis( radiusScoreArr , indices, axis=1 )[ :, 0 ] }' )
            print( f'Rotation Score: { np.take_along_axis( rotationScore  , indices, axis=1 )[ :, 0 ] }' )

            #   Print the summarize score with weighted
            print( f'All Score: { bestSimilarityScore }' )

        return bestMatchEllipseList, bestSimilarityScore