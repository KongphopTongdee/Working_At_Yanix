#!/usr/bin/env python3
#
# Copyright (C) 2023 Yannix Technologies
#			Written by Kongphop (kongton) Tongdee
#

########################################################
#
#	STANDARD IMPORTS
#

########################################################
#
#	LOCAL IMPORTS
#

from roitracking import BayesianCalculation as bayesCal

########################################################
#
#	GLOBALS
#

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

class ROITracker():
	'''The ROI tracker is a class for training from previous frames that user provided region of interest(ROI) with ellipse shape in the frame 
 	and tracking in after frames. This class consists of 2 main functions as follows.
	1. train means training mean and variance of color in region of interest(ROI) region from ellipse provided by user in training image.
	2. track means create probability image from image we want to track by apply Bayesian formula and statistical data 
		from training image together.
	'''
	def __init__( self, classImage, 
			  	  pointsInsideEllipse, 
			  	  pointsOutsideEllipse,
			  	  nCluster):
		'''Initial region of interest(ROI) tracker, create class of Bayesian for calculate multimodal(ROI region) 
		and class of Bayesian for calculate multivariate(~ROI region).
		'''
		#	Declare the class of Bayesian paramter of ROI region.
		self.multimodalROI = bayesCal.BayesianParam()

		#	Declare the class of Bayesian paramter of ~ROI region.
		self.multivariateNotROI = bayesCal.BayesianParam()

		self.train( classImage, pointsInsideEllipse, pointsOutsideEllipse, nCluster )

	def train( self, classImage, pointsInsideEllipse, pointsOutsideEllipse, nCluster ):
		'''The training process of Region of interested tracking system. Extract color feature. Seperate the color data group. 
		Create multimodal distribution parameter and multivariate Gaussian parameter.

        Parameters
        -----------
		classImage : object of image
			The class object of image for training, which store the source image.

		pointsInsideEllipse : ndarray of shape ( nSample, 2 )
			Array of all pixel coordinate that supposedly within the region of interest(ROI) ellipse region. 
   
		pointsOutsideEllipse : ndarray of shape ( nSample, 2 )
			Array of all pixel coordinate that supposedly without the region of interest(ROI) ellipse region. 
		
		nCluster : int
			The number of cluster group
		'''
		#	Extract the RGB color with the pixels points.
			#   Input image was array shape ( imageHeight, imageWidth, imageDepth )
			#	Input points was pixels with the ndarray of shape ( nSample, 2 )
			#	Get the color value of region of interest(ROI) region, which represent of shape ( nSample, nDim )
		colorValueROIArr = classImage.getPixelValue( pointsInsideEllipse )
  
			#	Get the color value of ~region of interest(ROI) region, which represent of shape ( nSample, nDim )
		colorValueNotROIArr = classImage.getPixelValue( pointsOutsideEllipse )
  
		#	Seperate the color data into nCluster groups with K-means clustering algorithms 
			#   Input `colorValueROIArr` was the ndarray of shape ( nSample, nDim )
			#	Output `colorClusterList` was list of list of tuple [ [ ( colorChannelsR, colorChannelsG, colorChannelsB ),...,],...,] ]
				#	which can easily represent with ( nCluster, nSample, nDim )
				#	The outer layer of the list is nCluster, the middle layer of the list is nSample, and the inner layer of the tuple is color channels.
				#	NOTE: There are nCluster(the group which store the similar color value in the group, depend on user input) that each group have 
				#	nSample(the sample in the group which seperate by k-mean, the sample of each group not equal, depend on the similar color)
				#	with nDim(dimension is depend on color channels, RGB color channels) 
		colorClusterList = bayesCal.clusteringColor( colorValueROIArr, nCluster )

		#	Calculate the multimodal parameter in class of `multimodalROI`
		self.multimodalROI.calMultimodalParam( colorClusterList, colorValueNotROIArr )

		#	Calculate the multivariate gaussian parameter in class of `multivariateNotROI`
		self.multivariateNotROI.calMultivariateParam( colorClusterList, colorValueNotROIArr )

	def track( self, image ):
		''' The tracking process of Region of interested tracking system. Apply multimodal distribution with Bayesian formula to
		create probability image.

		Parameters
        -----------
		image : ndarray of shape ( imageWidth, imageHeight, nDim )
			The source image use to be tracked.

        Return
        ----------
		probImage : ndarray of shape ( imageWidth, imageHeight, nDim )
			The probability image.

		'''
		#	Create probability image that apply multimodal distribution with Bayesian formula.
		probImage = bayesCal.getProbImage( image, self.multimodalROI, self.multivariateNotROI )

		return probImage