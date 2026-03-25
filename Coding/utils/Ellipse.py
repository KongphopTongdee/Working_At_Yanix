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

import matplotlib.patches

########################################################
#
#	LOCAL IMPORTS
#

########################################################
#
#	GLOBALS
#

#   The scaling factor to determine the covering of data
CONFIDENCEFACTOR = chi2.ppf( 0.90, df = 2 )

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

class Ellipse:
    '''The Ellipse classs, store the ellipse paramerters, calculate covariance matrix and return point inside ellipse.
    The Ellipse class use the `matplotlib.patches.Ellipse for getting the pixel inside the ellipse `
    '''
    def __init__( self, centerX: float, centerY: float, majorRadius: float, minorRadius: float, angle_deg: float, cov = None ):
        '''The ellipse parameters include
        1. center in x-axis
        2. center in y-axis
        3. major radius
        4. minor radius
        5. rotate angle in unit degree

        Parameters
        ----------
        centerX : float
            The center position in x-axis of an ellipse 
        
        centerY : float
            The center position in y-axis of an ellipse

        majorRadius : float
            The major radius of an ellipse

        minorRadius : float
            The minor radius of an ellipse

        angle_deg : float
            The rotation angle of an ellipse in degrees units

        cov : ndarray with shape ( 2, 2 ), default = None
            covariance matrix of an ellipse, if the cov is not provided, 
            call `getCovMatrix` for calculate the covariance matrix from ellipse parameters

        Exceptions
        -------------
        valueError : The major and minor radius less than or equal to zero
            
        '''
        #   Raise ValueError when the major or minor radius less than or equal to zero
        if majorRadius <= 0 or minorRadius <= 0:
            raise ValueError( f'The major and minor radius must be more than 0, got ({ majorRadius, minorRadius })' )

        #   Store the ellipse parameters to self.params
        self.params = np.array( [ centerX, centerY, majorRadius, minorRadius, angle_deg ] )

        #   The covariance matrix of the ellipse paramters
        self.cov = cov

        #   The center of ellipse
        self.center = np.array( [ centerX, centerY ] )

        #   The rotation angle in unit degree
        self.angle_deg = angle_deg

        #   Major radius
        self.majorRadius = majorRadius

        #   Minor radius
        self.minorRadius = minorRadius

        #   Contruct the Ellipse object
            #   `patches.Ellipse` parameters using ( center, width, heigh )
        self.ellipse = matplotlib.patches.Ellipse( self.center, 2 * majorRadius, 2 * minorRadius, angle = angle_deg, fill = False )

    def getCovMatrix( self ):
        '''Calculate the covariance matrix from the ellipse parameters

        Return
        -------
        self.cov : ndarray with shape
            The covaraince matrix of an ellipse

        '''
        #   if self.cov is not None, return self.cov
            #   This mean the covariance is already input
        if self.cov is not None:
            return self.cov
        
        #   Convert rotation angle to radians
        angle_rad = np.radians( self.angle_deg )

        #   Construct the covariance matrix based on axes lengths
            #   The CONFIDENCEFACTOR is the confidence level to scale the base of Gaussian distributions represented by the chi2 distributions
        covMatrix = np.array( [ [ ( self.majorRadius**2 ) / CONFIDENCEFACTOR,                       0                       ],
                                [                   0,                         ( self.minorRadius**2 ) / CONFIDENCEFACTOR   ] ] )
        
        #   Construct the rotation matrix
        rotationMatrix = np.array([ [ np.cos( angle_rad ), -np.sin( angle_rad ) ],
                                    [ np.sin( angle_rad ),  np.cos( angle_rad ) ]])
        
        #   Rotate the covariance matrix
            #   First dot terms is to rotate the covariance matrix into the orginal axis
            #   Second dot terms is undo the rotated to align the covariance matrix into the rotated angle of ellipse
        rotatedCovMatrix = np.dot( np.dot( rotationMatrix, covMatrix ) , rotationMatrix.T  )

        #   Store the rotated covaraince matrix to `self.cov`
        self.cov = rotatedCovMatrix

        return self.cov


    def getPointInsideEllipse( self ):
        '''Get all position inside the ellipse by create Ellipse object and check the boundary points

        Return
        -------
        insidePos : ndarray with shape ( nSample, 2 )
            The position inside the ellipse 
        '''
        #   Get the image boundary
        x, y, w, h = self.getBoundingBoxParam()

        #   Create meshgrid
        xRange = np.arange( x, x + w )
        yRange = np.arange( y, y + h )

        #   Create meshgrid
        y, x = np.meshgrid( yRange, xRange )

        #   Flatten
        y, x = y.flatten(), x.flatten()

        #   Get all pixel position in the image
        points = np.vstack( ( x, y ) ).T

        #   Check boundary point on Ellipse 
        indices = self.ellipse.contains_points( points )

        #   Flip position from ( x, y ) into ( y, x )
        insidePos = np.flip( points[ indices ], axis = -1 )
        
        return insidePos
    

    def getPointOutsideEllipse( self, imageShape: tuple ):
        '''Get all pixels outside the ellipse by create Ellipse object and check the boundary points
        
        Parameters
        -----------
        imageShape : tuple
            Shape of input image to create image boundary

        Return
        -------
        outsidePos : ndarray with shape ( nSample, 2 )
            The position outside the ellipse.
        '''
        #   Get the image shape
        imageHeight, imageWidth = imageShape[ :2 ]

        #   Create meshgrid
        y, x = np.meshgrid( np.arange( imageHeight ), np.arange( imageWidth ))

        #   Flatten
        y, x = y.flatten(), x.flatten()

        #   Get all pixel position in the image
        points = np.vstack( ( x, y ) ).T

        #   Check boundary point on Ellipse 
        indices = self.ellipse.contains_points( points )
            
        #   Get boundary point outside the ellipse by invert the boundary point on ellipse.
        invertIndices = np.logical_not( indices )
        
        #   Flip position from ( x, y ) into ( y, x )
        outsidePos = np.flip( points[ invertIndices ], axis=-1 )
        
        return outsidePos
    
    def getBoundingBoxParam( self ):
        '''Get bounding box parameters ( x, y, w, h ) by calculate minimum and maximum bound from ellipse parameters
            
        Return
        -------
        bboxParam : list
            The bounding box parameters include ( x, y, w, h )
            
        '''

        #   Get the corner of ellipse
        cornerList = self.ellipse.get_corners()

        #   Clip value not lower than zero
        cornerList = np.clip( cornerList, a_min = 0, a_max = np.inf )

        #   Maximum pos ( y, x )
        maxPos = np.max( cornerList, axis = 0 )

        #   Minimum pos ( y, x )
        x, y =  np.min( cornerList, axis = 0 )

        #   Calculate width, heigh
        w, h = maxPos - [ x, y ]
        
        #   The boundingg box parameters
        bboxParam = np.array( [ x, y, w, h ], dtype = int )

        return bboxParam
    