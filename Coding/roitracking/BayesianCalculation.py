#!/usr/bin/env python3
#
# Copyright (C) 2023 Yannix Technologies
#			Written by Kongphop (kongton) Tongdee
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

########################################################
#
#	GLOBALS
#

#	Number of program cycles to complete in K-means clustering funciton 
MAXITERS = 100

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

class BayesianParam():
    '''This class create for calculate Bayesian parameter ( including prior, mean, covariance, dimension of color channels, and weight ) 
    and get multivariate Gaussian PDF and mulitmodal PDF
    '''
    def __init__( self ):
        '''Initial Bayesian parameter, create the storage of Bayesian parameter ( including Prior, Mean, Covariance, and weight ).
		'''
		#	Declare the storage of prior, which assign 0.
        self.prior = 0
		
        #	Declare the storage of mean, which create empty ndarray.
        self.mean = np.array( [] )

        #	Declare the storage of covariance, which create empty ndarray.
        self.cov = np.array( [] )

        #	Declare the storage of weight in each cluster, which create empty list.
        self.weightClusterList = []

        #	Declare the storage of dimension in color channels, which assign 0.
        self.nDim = 0

    def calMultivariateParam( self, colorClusterROI, colorNotROI ):
        '''Function of calculate multivariate Gaussian PDF parameter for ~ROI region, which storing ~ROI prior, mean of ~ROI
        ,dimension of color channels, and covariance ~ROI.

        Parameters
        ----------
        colorClusterROI : list of list of tuple [ [ ( colorChannelsR, colorChannelsG, colorChannelsB ),... ]
                                                ,...,
                                                [ ( colorChannelsR, colorChannelsG, colorChannelsB ),... ] ]
            Color value separated in cluster group. Represented in list, the index refer to the cluster labels
            which can easily represent with ( nCluster, nSample, nDim )
            the outer layer of the list is nCluster, the middle layer of the list is nSample, and the inner layer of the ndarray is color channels.
            NOTE: There are nCluster(the group which store the similar color value in the group, depend on user input) that each group have 
            nSample( the sample in the group which seperate by k-mean, the sample of each group not equal, depend on the similar color )
            with nDim( dimension is depend on color channels, RGB color channels ) 

        colorNotROIArr : ndarray of shape ( nSample, nDim )
		    Color value in ~ROI region.
        '''
		#	Declare the storage of number of sample of data in ROI region.
        nSampleROI = 0

        #	Loop for calculate the all sample in ROI region.
        for colorEachClusterList in colorClusterROI:

            #	Sum the sample of each cluster in `colorClusterROI`, and store in `nSampleROI`, which refer to sample of ROI region.
            nSampleROI += len( colorEachClusterList )

        #	Sum all the sample with sample of ROI region and sample of not ROI region. 
        sumSample = nSampleROI + len( colorNotROI )

		#   Assign the calculation of prior of ~ROI region into `self.prior` by using sample of not ROI region divide of sumSample.
        self.prior = len ( colorNotROI ) / sumSample 

        #   Assign the calculation of mean of ~ROI region into `self.mean`
        self.mean = np.mean( colorNotROI, axis = 0 )

        #   Assign the calculation of dimension of color channels of ~ROI region into `self.nDim`
        self.nDim = len( self.mean )

        #   Assign the calculation of covariance of ~ROI region into `self.cov`
        self.cov = np.cov( colorNotROI.T )

    def calMultimodalParam( self, colorClusterROI, colorNotROI ):
        '''Function for calculate multimodal PDF parameter and storing ROI prior, mean of each cluster in ROI, 
	    covariance of each cluster in ROI, and dimension of color channels.
         
        Parameters
        ----------
        colorClusterROI : list of list of tuple [ [ ( colorChannelsR, colorChannelsG, colorChannelsB ),... ]
                                                ,...,
                                                [ ( colorChannelsR, colorChannelsG, colorChannelsB ),... ] ]
            Color value separated in cluster group. Represented in list, the index refer to the cluster labels
            which can easily represent with ( nCluster, nSample, nDim )
            the outer layer of the list is nCluster, the middle layer of the list is nSample, and the inner layer of the ndarray is color channels.
            NOTE: There are nCluster(the group which store the similar color value in the group, depend on user input) that each group have 
            nSample( the sample in the group which seperate by k-mean, the sample of each group not equal, depend on the similar color )
            with nDim( dimension is depend on color channels, RGB color channels ) 

        colorNotROIArr : ndarray of shape ( nSample, nDim )
		    Color value in ~ROI region.
        
        '''
        #   Get the number of cluster in ROI region.
        nCluster = len( colorClusterROI )

        #	Declare the storage of number of sample of data in ROI region.
        nSampleROI = 0
        
        #	Declare the storage of mean for calculate mean in each cluster with shape of ( nDim, ).
        meanClusterROI = []
        
        #	Declare the storage of covariance for calculate covariance in each cluster with shape of ( nDim, nDim ).
        covClusterROI = []

        #	Loop for calculate the all sample in ROI region.
        #	Loop for calculate the mean of each cluster in ROI region.
        #	Loop for calculate covariance matrix in each cluster in ROI region.
        for colorEachClusterList in colorClusterROI:

            #	Sum the sample of each cluster in `colorClusterROI`, and store in `nSampleROI`.
            nSampleROI += len( colorEachClusterList )
            
            #	Calculate mean of each cluster in ROI region.
                #	Which can easily represented with shape ( nCluster, nDim )
            meanClusterROI.append( np.mean( colorEachClusterList, axis = 0 ) )

            #	Convert list of tuple [ ( colorR, colorG, colorB ), ... ] into ndarray with shape of ( nSample, nDim )
            colorROIArr = np.array( colorEachClusterList )

            #	Calculate covariance matrix in each cluster and store the output in storage of covariance.
            covClusterROI.append( np.cov( colorROIArr.T ) )

        #	Sum all the sample with sample of ROI region and sample of not ROI region. 
        sumSample = nSampleROI + len( colorNotROI )

		#   Assign the calculation of prior of ROI region into `self.prior` by using sample of ROI region divide of sumSample.   
        self.prior = nSampleROI / sumSample

        #	Convert list of tuple [ ( muR, muG, muB ), ... ] into ndarray with shape ( nCluster, nDim )
        self.mean = np.array( meanClusterROI )

        #   Assign the calculation of dimension of color channels of ROI region into `self.nDim` by calculate with sample in first index of mean
        self.nDim = len( self.mean[ 0 ] ) 

        #	Convert list of ndarray [ array( varianceR, varianceRG, varianceRB ),... ] into ndarray with shape of ( nCluster, nDim, nDim )
        self.cov = np.array( covClusterROI )   

        #	`nSampleClusterList` is store the number of sample in each cluster
		    #	The index refer to the cluster group
        nSampleClusterList = []

        #	Loop for count the amount of color value in each cluster.
        for number in range( nCluster ):

            #	Append the sample of each cluster in `nSampleClusterList`.
            nSampleClusterList.append( len( colorClusterROI[ number ] ) )

        #	Calculate the weight of each cluster from divide the number of sample each cluster with total number of sample
        self.weightClusterList = [ nSampleCluster / nSampleROI for nSampleCluster in nSampleClusterList ]

    def getMultivariatePDF( self, image ):
        '''Function for caluculate multivariate gaussian density(PDF) 

        Parameters
        ----------
        image : ndarray of shape ( imageHeight, imageWidth, nDim )
            Original image

        Returns
        ----------
        multivariatePDF : ndarray of shape ( imageHeight, imageWidth )
            Multivariate Gaussian probability density of input image.
        '''
        #	Convert the mean data from ndarray ( nDim, ) to ndarray ( 1, 1, nDim ), 
            #	which can broadcasting to `image` with shape ( imageHeigth, imageWidth, nDim )
        mean = self.mean[ :, np.newaxis, np.newaxis ].T

        #	Calculate the numerator term or mahalanobis term by using eisum
            #	Calculate formula ( image - mean ).T @  inverse covariance @ ( image - mean )  
            #	The calculate formula will be the shape of [ ( nDim, imageWidth, imageHeight ) @ ( nDim, nDim ) @ ( imageHeight, imageWidth, nDim ) ]
            #	So the eisum will convert the shape into [ ( imageHeight, imageWidth, nDim ) @ ( nDim, nDim ) @ ( imageHeight, imageWidth, nDim ) ]
            #	The output shape of `mahalanobisTerm` will be ( imageHeight, imageWidth )
        mahalanobisTerm = np.einsum( 'ijn,nm,ijm->ij',
                                    image - mean,
                                    np.linalg.inv( self.cov ),
                                    image - mean )
        
        #	Calculate the numerator term or exponential term
            #	The `mahalanobisTerm` with shape ( imageHeight, imageWidth )
            #	Calculate formula exp( -0.5 * ( colorValue - mean ).T @ covariance @ ( colorValue - mean ) )
            #	The `expTerm` calculate in shape of [ exp( ( 1, 1 ) * ( imageHeight, imageWidth ) ) ]
            #	The	`expTerm` with shape ( imageHeight, imageWidth )
        expTerm = np.exp( -0.5 * mahalanobisTerm )
    
        #	Calculate the multivariate gaussian distribution density
            #	Calculate formula np.sqrt( ( 2 * pi )** nDim * det( covariance ) )
            #	The	`multivariatePDF` with shape ( imageHeight, imageWidth )
        multivariatePDF = expTerm / ( np.sqrt( ( np.power( ( 2 * np.pi ), self.nDim ) * np.linalg.det( self.cov ) ) ) )

        return multivariatePDF
    
    @staticmethod
    def getMultivariatePDFForMultimodal( nDim, cov, mean, image ):
        '''Function for caluculate multivariate gaussian density(PDF) 

        Parameters
        ----------
        nDim : int
            Number of color channels.

        cov : ndarray of shape ( nDim, nDim )
            Covariance matrix of color channel RGB.

        mean : ndarray of shape ( nDim, )
            Mean of color channel RGB, which data of ndarray( meanR meanG meanB ).

        image : ndarray of shape ( imageHeight, imageWidth, nDim )
            Original image

        Returns
        ----------
        multivariatePDF : ndarray of shape ( imageHeight, imageWidth )
            Multivariate Gaussian probability density of input image.
        '''
        #	Convert the mean data from ndarray ( nDim, ) to ndarray ( 1, 1, nDim ), 
            #	which can broadcasting to `image` with shape ( imageHeigth, imageWidth, nDim )
        mean = mean[ :, np.newaxis, np.newaxis ].T

        #	Calculate the numerator term or mahalanobis term by using eisum
            #	Calculate formula ( image - mean ).T @  inverse covariance @ ( image - mean )  
            #	The calculate formula will be the shape of [ ( nDim, imageWidth, imageHeight ) @ ( nDim, nDim ) @ ( imageHeight, imageWidth, nDim ) ]
            #	So the eisum will convert the shape into [ ( imageHeight, imageWidth, nDim ) @ ( nDim, nDim ) @ ( imageHeight, imageWidth, nDim ) ]
            #	The output shape of `mahalanobisTerm` will be ( imageHeight, imageWidth )
        mahalanobisTerm = np.einsum( 'ijn,nm,ijm->ij',
                                    image - mean,
                                    np.linalg.inv( cov ),
                                    image - mean )
        
        #	Calculate the numerator term or exponential term
            #	The `mahalanobisTerm` with shape ( imageHeight, imageWidth )
            #	Calculate formula exp( -0.5 * ( colorValue - mean ).T @ covariance @ ( colorValue - mean ) )
            #	The `expTerm` calculate in shape of [ exp( ( 1, 1 ) * ( imageHeight, imageWidth ) ) ]
            #	The	`expTerm` with shape ( imageHeight, imageWidth )
        expTerm = np.exp( -0.5 * mahalanobisTerm )
    
        #	Calculate the multivariate gaussian distribution density
            #	Calculate formula np.sqrt( ( 2 * pi )** nDim * det( covariance ) )
            #	The	`multivariatePDF` with shape ( imageHeight, imageWidth )
        multivariatePDF = expTerm / ( np.sqrt( ( np.power( ( 2 * np.pi ), nDim ) * np.linalg.det( cov ) ) ) )

        return multivariatePDF
        
    def getMultimodalPDF( self, image ):
        '''Function for caluculate multimodal density(PDF) 

        Parameters
        ----------
        image : ndarray of shape ( imageHeight, imageWidth, nDim )
            Original image

        Returns
        ----------
        multimodalPDF : ndarray of shape ( imageHeight, imageWidth )
            Multimodal probability density of input image.
        
        '''
        #	Get number of cluster from  `self.weightClusterList`.
            #	weight was an list which can easily be represented with shape ( nCluter, )
        nCluster = len( self.weightClusterList )

        #	Declare `multimodalPDF` to store the value that obtained from the ( weight * multivariate gaussian distribution value ).
        multimodalPDF = 0

        #	Loop for calculate multivariate gaussian distribution of each cluster and combine them to multimodal distribution.
        for clusterIdx in range( nCluster ):

            #	Calculate multivariate gaussian distribution of each cluster
                #	Which can easily represented with shape ( imageHeight, imageWidth, nDim ) 
            multivariatePDF = self.getMultivariatePDFForMultimodal( self.nDim, 
													                self.cov[ clusterIdx ], 
													                self.mean[ clusterIdx ], 
													                image ) 
            
            #	Calculate multimodal distribution by summation multivariate gaussian distribution of each cluster
                #	Which can easily represented with shape ( imageHeight, imageWidth, nDim ) 
            multimodalPDF += ( self.weightClusterList[ clusterIdx ] * multivariatePDF )

        return multimodalPDF
        

def kmeans( data, nCluster, maxIters = MAXITERS ):
	'''Function for clustering the data into the group
	
	Parameters
	----------
	data : ndarray of shape ( nSample, nDim )
		Color value of RGB color channels.

	nCluster : int
		Number for clustering the data into group.

	maxIters : int
		Number of the maximum program cycles(deflaut = 100) to complete in K-means clustering function.
	
	Returns
	-------
	centroids : ndarray of shape ( nCluster, nDim )
		The centroids of each cluster.
		
	labels : list of int [ value,...,value ]
		The labels group for data store in list with nSample lengths 
		which can easily represent with ndarray with shape ( nSample, )
	'''
	#	Create centroids randomly with number cluster by random in data.
	centroidsList = data[ np.random.choice( data.shape[ 0 ], nCluster, replace = False ) ]

	#	Loop for calculate the euclidean distance for each color value compared with all random centroids.
		#	If any color value is near any random centroids, assign the color value in the nearest centroids group.
		#	Calculate the new centroids and do it again until the centroids don't change.
	for round in range( maxIters ):

		#	Assign each data point to the nearest centroid.
			#	Convert 2D array to 3D array: 2D array with shape ( nSample, nDim ) into 3D array with shape ( nSample, nCluster, nDim )
		data3DArr = data[ :, np.newaxis ]

			#	Calculate the distance of each color value and compared with every n cluster centroids.
				#	Which can easily represent `distClusterData` with shape ( nSample, nCluster, nDim )
		distClusterData = data3DArr - centroidsList

			#	Calculate the euclidean distance from every distance that compared with every n cluster centroids.
				#	Which can easily represent `euclidean` with shape ( nSample, nCluster )
		euclidean = np.linalg.norm( distClusterData, axis=2 )

			#	Select the lowest value from each row of `euclidean` and return as index.
				#	For represent Which group should this color value be in?.
				#	Which can easily represent `euclidean` with shape ( nSample, )
		groupIndex = np.argmin( euclidean, axis=1 )

		#	Declare the storage of new centroids.
		newCentroids = []

		#	Update centroids
			#	Loop for calculate the mean of each cluster.
		for nGroup in range( nCluster ):

				#	Compare the n group with the `groupIndex`. 
					#	If the `groupIndex` value is the same as the n Group, store that color value.
					#	After store the color value in each n group, calculate the mean of each n group to represent the new centroid.
					#	Append the new centroid in list of `newCentroids`
			newCentroids.append( data[ groupIndex == nGroup ].mean( axis=0 ) )

		#	Convert	list of ndarray [ ( nDim, ) ] into ndarray with shape ( nCluster, nDim )
		newCentroidArr = np.array( newCentroids )

		#	Check for convergence
			#	Checking the equal value with `centroidsList` and `newCentroidArr` if equal break the loop.
		if np.allclose( centroidsList, newCentroidArr ):
			break

		#	Update new centroids to old centroids.
			#	Which can easily represent with ( nCluster, nDim )
		centroidsList = newCentroidArr

	return centroidsList, groupIndex

def clusteringColor( colorValueArr, nCluster ):
    '''Function for cluster the color value into the group with nearest value.

    Parameters
    ----------
    colorValueList : ndarray of shape ( nSample, nDim )
        Color value of 3 color channels.

    nCluster : int
        The number of clustering group.

    Returns
    ----------
    weightClusterList : list of float [ value,..., value ]
        Weight value of each cluster group.
        Which can easily represent with ( nCluster, )

    colorClusterList : list of list of tuple [ [ ( colorChannelsR, colorChannelsG, colorChannelsB ),... ],...,[ ( colorChannelsR, colorChannelsG, colorChannelsB ),... ] ]
        Color value separated in cluster group. Represented in list, the index refer to the cluster labels
        which can easily represent with ( nCluster, nSample, nDim )
        the outer layer of the list is nCluster, the middle layer of the list is nSample, and the inner layer of the ndarray is color channels.
        NOTE: There are nCluster(the group which store the similar color value in the group, depend on user input) that each group have 
        nSample( the sample in the group which seperate by k-mean, the sample of each group not equal, depend on the similar color )
        with nDim( dimension is depend on color channels, RGB color channels ) 
    '''	
    #	Get the number of sample
    nSample, nDim = colorValueArr.shape

    #	Declare the storage list to separated the color value in each cluster
        #	The index refer to the cluster group 
    colorClusterList = []

    #	`nSampleClusterList` is store the number of sample in each cluster
        #	The index refer to the cluster group
    nSampleClusterList = []

    #	Calculate the labels of each color value, to determine the color value which group should be in.
        #	Which can easily represent `labelsColorList` with ( nSample, )
    centroidsList, labelsColorList = kmeans( colorValueArr, nCluster )

    #	Loop for all cluster index, compare and store the color value into group.
    for clusterIdx in range( nCluster ):

        #	Get the color value that the label is the same as current cluster index
            #	`colorList` is the list with nSample length that have the same cluster index
        colorList = [ colorValueArr[ sampleIdx ] for sampleIdx in range( nSample ) if ( clusterIdx == labelsColorList[ sampleIdx ] ) ]

        #	Extend the color value from n group in the `colorClusterList`.
            #	which can easily represent with ( nCluster, nSample, nDim )
				#	The outer layer of the list is nCluster, the middle layer of the list is nSample, and the inner layer of the ndarray is color channels.
				#	NOTE: There are nCluster(the group which store the similar color value in the group, depend on user input) that each group have 
				#	nSample( the sample in the group which seperate by k-mean, the sample of each group not equal, depend on the similar color )
				#	with nDim( dimension is depend on color channels, RGB color channels ) 
        colorClusterList.extend( [ colorList ] )

    return colorClusterList

def getProbImage( image, classROIRegion, classNotROIRegion ):
	'''Function for create probability image by apply with multimodal distribution, multivariate Gaussian, and Bayesian formula
	
	Parameters
	----------
	image : ndarray of shape ( imageHeight, imageWidth, nDim )
		Original picture 

	classROIRegion : object of ROI region
        The class object of ROI region, which store Bayesian parameter for calculate multimodal parameter and apply in likelihood term.
	
	classNotROIRegion : object of ~ROI region 
        The class object of ~ROI region, which store Bayesian parameter for calculate multivariate parameter and apply in likelihood term.

	Returns
	----------
	probImage : ndarray of shape ( imageHeight, imageWidth, nDim )				
		The probability image
	'''
	#	Calculate the likelihood of not ROI region in Bayesian formula.
		#	Which can easily represented with shape ( imageHeight, imageWidth, nDim ) 
	likelihoodNotROITerm = classNotROIRegion.getMultivariatePDF( image )

	#	Calculate the likelihood of ROI region in Bayesian formula.
        #	Which can easily represented with shape ( imageHeight, imageWidth, nDim ) 
	likelihoodROITerm = classROIRegion.getMultimodalPDF( image )
	
	#	Calculate probability image with applying multimodalPDF, multivariate Gaussian PDF and Bayesian formula.
		#	Which can easily represented with shape ( imageHeight, imageWidth, nDim ) 
	probImage = 1 / ( 1 + ( ( classNotROIRegion.prior * likelihoodNotROITerm ) / ( classROIRegion.prior * likelihoodROITerm ) ) )

	return probImage