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

import json

from scipy.stats import multivariate_normal

########################################################
#
#	GLOBALS
#

#   The EPSILON term
EPSILON = 1e-9

########################################################
#
#	CLASS DEFINITIONS
#

class MultivaraiteGaussianBayesian:
    '''The Multivariate Gaussian Bayesian model is the same as Bayesian interface but 
    utilize the multivariate Gaussian distributions to find the joint log-likelihood terms'''

    def __init__( self, logPrior: np.ndarray, modelParamDict: dict ) :
        '''Initial class by storing the model parameters and log prior 
        into `self.modelParamDict` and `self.logPrior`

        Parameters
        -------------
        logPrior : ndarray( nClass, )
            The prior of each class

        modelParamDict : dict
            The model parameters store in dictionary.
        '''
        #   The dictionary store the Gaussian parameters each class.
            #   The dictionary structure
            #    ___________________________________________________________________
            #   |                        |                                          |
            #   |        Keys            |                Values                    |
            #   |________________________|__________________________________________|
            #   |                        |                                          |
            #   |  0 ( nonhomo_class )   |    dict( keys:[ 'mean', 'sigma'] )       |
            #   |  1 ( homo_class )      |    dict( keys:[ 'mean', 'sigma'] )       |
            #   |________________________|__________________________________________|
        self.modelParamDict = modelParamDict

        #   The prior in log space
        self.logPrior = logPrior

    @staticmethod
    def calculateBayesianParams( data: np.ndarray, labels: np.ndarray ):
        '''Calculate Gaussian parameters ( mu, sigma ) and log prior 
        from the training data and store the parameter into dictionary
        
        Parameters
        -----------
        data : ndarray with shape ( nSample, nFeature, nDim )
            The training data 
            
        labels : ndarray with shape ( nSample )
            The labels or class of the data

        Returns
        ----------

        modelParamDict : dict
            The model parameters store in dictionary.

        logPrior : ndarray( nLabel, )
            The prior of each label

        '''
        #   The dictionary for storage model parameters
        modelParamDict = dict()

        #   Get the number of feature and dimension from data input
        nSample, nFeature, nDim = data.shape

        #   Get the array of uniqueLabel and count each labels
        uniqueLabel, uniqueCount = np.unique( labels, return_counts = True )

        #   calculate the log priors from training data
        logPrior = np.log( uniqueCount / np.sum( uniqueCount ) )

        #   Separate the data from class, in array with shape ( nClass, nSample|Class, nFeature, nDim ), 
            #   The index of separatedData represent the label
        separatedData = [ data[ np.argwhere( labels == label ).squeeze() ] for label in uniqueLabel ]

        #   Loop for all label, classData with shape ( nSample, nFeature, nDim )
        for label, classData in enumerate( separatedData ):

            #   Declare empty array with shape nFeature and nDimention for storing model parameters
            mean = np.empty( ( nFeature, nDim ) )
            cov = np.empty( ( nFeature, nDim, nDim ) )

            #   Loop for nFeature time to calculate mean and covariance
            for featureIdx in range( nFeature ):

                #   Get one feature, with array shape ( nSample, nDim )
                feature = classData[ :, featureIdx, : ]

                #   Calculate model parameters of feature. Store into empty array. The fist dimension is the feautureIdx
                    #   axis = 0 is the nSample axis, find mean along the nSample axis
                mean[ featureIdx ] = np.mean( feature, axis = 0 )

                    #   Find covariance matrix. feature.T give the array shape ( nDim, nSample )
                        #   For compatible to the np.cov function
                cov[ featureIdx ] = np.cov( feature.T )

            #   Store in dictionary keys is the class, value store in list [ mean, cov ]
            modelParamDict.update( { label: [ mean, cov ] } )

        return MultivaraiteGaussianBayesian( logPrior, modelParamDict )

    def calculateLogPdf( self, x: np.ndarray ):
        '''Pass all variable x for calculate multivariate Gaussian pdf in log space and sum with log prior

        Parameters
        ----------
        x : ndarray with shape ( nSample, nFeature, nDim )
            The feature or the data to calculate pdf

        Return
        -------

        jll : ndarray with shape ( nClass, nFeature, nSample )
            The array of joint log-likelihood (jll) in each feature

        '''
        #   Swap input data from ( nSample, nFeature, nDim ) into shape ( nFeature, nSample, nDim )
            #   For easilier loop each feature
        x = x.swapaxes( 0, 1 )

        #   Declare list for store joint log-likelihood terms each feature
        jll = []

        #   Loop for all in class/label to get param for calculate pdf
        for label, modelParams in self.modelParamDict.items():
            
            #   The param is the Gaussian parameters, involve mu and sigma
            mu, sigma = modelParams

            #   Loop for all feature to calculate each the feature pdf with shape ( nFeature, nSample )
            pdf = np.array( [ multivariate_normal.pdf( *stat ) for stat in zip( x, mu, sigma ) ] )

            #   Clip the pdf, before take log function
            clipPDF = np.clip( pdf, a_min = EPSILON, a_max = np.inf )

            #   Take logarithm function to pdf values
            logPDF = np.log( clipPDF )

            #   Store in jll list
            jll.append( logPDF )

        #   After append convert list to array with shape ( nClass, nFeature, nSample )
        jll = np.array( jll )
        
        '''
        #   Sum along features axis ( sum all feature ) and add logPrior, resulting in array shape ( nClass, nSample )
        sumJll = np.sum( jll, axis = 1 ) + self.logPrior.reshape( -1, 1 )

        #   Swapaxes into ( nSample, nClass )
        sumJll = sumJll.swapaxes( 0, 1 )
        '''

        return jll

    def getProb( self, x: np.ndarray, returnJll: bool = False ):
        '''Utilize the Bayesian formula for calculate the probability of binary class of each sample, 
        aplly the multivariate Guassian to calculate the density from each feature and each class called joint log-likelihood (jll).
        Each feature was assumed to be independently, thus the join jog-likelihood was in log-space, 
        the multiply terms will be the additional terms ( `sumJll` ), then calculate the probability of [ non-homo, homo ] class. 

        Parameters
        -----------
        x : ndarray with shape ( nSample, nFeature, nDim )
            The feature or the data to calculate the probability

        returnJll : bool, default = False
            If returnJll == True the function will yeild the join log-likelihood (jll) of each feature.
            Otherwise, return only probability

        Return
        --------
        jll : ndarray with shape ( nClass, nFeature, nSample )
            The array of joint log-likelihood in each feature

        prob : ndarray with shape ( nSample, 2 )
            The probability of each class [ non-homo, homo ]

        Notes
        -----
        Currently, this function only support 2 classes [ non-homo, homo ].
        '''

        #   Get the array of joint log-likelihood (jll) in each feature
            #   jll with shape ( nClass, nFeature, nSample )
        jll = self.calculateLogPdf( x )

        #   Calculate the sum of joint log-likelihood terms
            #   Sum along features axis ( sum all feature ) and add logPrior, resulting in array shape ( nClass, nSample )
        sumJll = np.sum( jll, axis = 1 ) + self.logPrior.reshape( -1, 1 )

        #   Swapaxes into ( nSample, nClass )
        sumJll = sumJll.swapaxes( 0, 1 )

        #   Calculate the probability of each class from sum of log-likelihood probability all feature
        prob0 =  1 / ( 1 + np.exp( sumJll[ :, 1 ] - sumJll[ :, 0 ] ) )
        prob1 = 1 / ( 1 + np.exp( sumJll[ :, 0 ] - sumJll[ :, 1 ] ) )

        #   Swap axis into shape ( nSample, 2 )
        prob = np.array( [ prob0, prob1 ] ).swapaxes( 0, 1 )

        #   If returnJll is True, yield the joint log-likelihood (jll) array
        if returnJll:
            return jll, prob

        return prob

    def exportModel( self, savePath:str ):
        '''Export the model parameters into json file, the keys include, 1) logpriors, 2) mean 3) cov

        Parameters
        ----------
        savePath : str
            The specific path for saving model

        Notes
        -----
        Currently, this function only support 2 classes ( non-homo, homo ).
        '''
        #   The same structure with `self.modelParamDict` but loop for all items for convert ndarray into list
        outputDict = { 'logPrior': self.logPrior.tolist() }

        #   Loop for all label
        for label, modelParam in self.modelParamDict.items():
            mean, sigma = modelParam

            #   Label 0 is the nonhomo class, using 'nonhomo_class' as the keys of dictionary
            if label == 0:

                #   Convert mean and sigma array in to list and strorage in dictionary
                outputDict.update( { f'nonhomo_class': { 'mean': mean.tolist(), 'sigma': sigma.tolist() }  } )
            
            #   Label 1 is the homo class, using 'homo_class' as the keys of dictionary
            elif label == 1:

                #   Convert mean and sigma array in to list and strorage in dictionary
                outputDict.update( { f'homo_class': { 'mean': mean.tolist(), 'sigma': sigma.tolist() }  } )

        #   Export .json file
        with open( savePath, 'w' ) as outFile:
            json.dump( outputDict, outFile, indent = 4 )

    @staticmethod
    def loadParams( modelPath: str ):
        '''Import model parameters from specific .json file path
        
        Parameters
        -----------
        modelPath : str
            Path of model

        Return
        --------
            The object of this class by initial with the model parameters loaded.

        Notes
        -----
        Currently, this function only support 2 classes ( non-homo, homo ).
        '''

        #   The dictionary for storage model parameters
        modelParamDict = dict()

        #   The model paths with .json file
        with open( modelPath, 'r' ) as f:
            
            #   Load data
            data = json.load( f )

            #   Get LogPrior values
            logPrior = np.asarray( data[ 'logPrior' ] )

            #   Loop to get only xx_class keys in dictionary
            for labels, classData in data.items():

                #   Skip the keys without 'class'
                if 'class' not in labels:
                    continue
                
                #   Convert labels = 'nonhomo_class' into label = 0
                if labels == 'nonhomo_class':
                    label = 0

                #   Convert labels = 'homo_class' into label = 1
                elif labels == 'homo_class':
                    label = 1

                #   The dictionary in label_xx is include mean, sigma keys
                mean, sigma = classData.values()

                #   Update into the model structure, with ndarray value
                modelParamDict[ int( label ) ] = [ np.array( mean ), np.array( sigma ) ]

        return MultivaraiteGaussianBayesian( logPrior, modelParamDict )
    