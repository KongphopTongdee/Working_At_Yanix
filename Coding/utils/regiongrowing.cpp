//
// Copyright (C) 2023 Yannix Technologies
//			Written by Thanachart (Ultra) Satianjarukarn
//
//#######################################################
//
//	STANDARD IMPORTS
//

#include <iostream>
#include <vector>
#include <deque>

//#######################################################
//
//	GLOBALS
//

//  The neighbor grid using for finding neighbor position
const int NEIGHBORGRID[ 8 ][ 2 ] = { { 1, 0 }, { -1, 0 }, { 0, 1 }, { 0, -1 }, 
                                     { 1, 1 }, { -1, -1 }, { 1, -1 }, { -1, 1 } };

//#######################################################
//
//	FUNCTIONS DEFINITIONS
//

extern "C"
{
    uint32_t *performRegionGrowing( const double *probImage, 
                                    const int imageHeight, 
                                    const int imageWidth, 
                                    const double criteriaThreshold, 
                                    const double initialSeedThresh ) 
    {
    /*Perform region growing on the probability image or seach on the probability image

    Parameters
    -----------
    probImage : 1D array with shape ( imageHeight, imageWidth )
        The probability image or the flatten image contain the probability at each pixel

    imageHeight : int
        The length of image in y-axis

    imageWidth : int
        The length of image in x-axis

    criteriaThreshold : double
        The threshold for terminate condition, while seraching if the neighbor
        probability is less than `criteriaThreshold` this mean not the same region

    initSeedThresh : double
        The threshold value for getting initial seed position on probability image.
        The pixel that have the higher probability tange iniSeedThresh will be the initial seed position.
    
    Return
    --------
    segmentImage : 1D uint32_t array with shape ( imageHeight, imageWidth )
        The 1D array represent the label values of each pixel in image
    */

        //  Visited array, declare a 2D boolean array to check if a pixel has been already searched or not
        std::vector< std::vector< bool > > visited( imageHeight, std::vector< bool >( imageWidth, false ) );
  
        //  1D array, with range ( imageHeight * imageWidth ), each values define the region labels.
        uint32_t *segmentImage = new uint32_t[ imageHeight * imageWidth ];

        //  Get the position of initial seed from the probability where more than `initialSeedThresh`
        std::deque< std::pair< int, int > > initSeedQueue;

        //  Loop for all pixel in image, to get the initial seed
    // #pragma omp parallel for
        for ( int i = 0; i < imageHeight; i++ ) 
        {
            for (int j = 0; j < imageWidth; j++ ) 
            {
                //  Assign the pixel with 0
                segmentImage[ ( i * imageWidth ) + j ] = 0;

                //  Check if the probImage of pixel more than initSeedThresh
                if ( probImage[ ( i * imageWidth ) + j ] >= initialSeedThresh ) 
                {
                    //  Push back the pair of index
                    initSeedQueue.push_back( std::make_pair( i, j ) );
                }
            }
        }

        //  The region label, additional 1 after end the initSeedQueqe while loop
        uint32_t regionLabel = 1;

        //  Loop until the initial seed queqe is empty
        while ( !initSeedQueue.empty() ) 
        {
            
            //  Get first element of `initSeedQueqe`
            std::pair< int, int > initRegionPos = initSeedQueue.front();
            
            //  Remove first element of initSeedQueqe
            initSeedQueue.pop_front();

            //  Check if the initial region position has been visited, skip this initRegionPos
            if( visited[ initRegionPos.first ][ initRegionPos.second ] )
            {
                continue;
            }

            //  Mark the regionLabel in the initial seed position
            segmentImage[ ( initRegionPos.first * imageWidth ) + initRegionPos.second ] = regionLabel;

            //  Number of pixels in the region
            int nPixel = 1;

            //  Queue the initial region position
            std::deque<std::pair< int, int >> currentQueue;
            currentQueue.push_back( initRegionPos );

            //  Do this region and position until it can't grow anymore
            while ( !currentQueue.empty() ) 
            {
                //  Get the position from queqe
                std::pair< int, int > currentPos = currentQueue.front();
                currentQueue.pop_front();

                //  Mark currentPosition as visited
                visited[ currentPos.first ][ currentPos.second ] = true;

                //  Loop for 8-neighbors of current pos
                for ( int i = 0; i < 8; i++ ) 
                {

                    int neighborY = currentPos.first + NEIGHBORGRID[ i ][ 0 ];
                    int neighborX = currentPos.second + NEIGHBORGRID[ i ][ 1 ];

                    //  Check if the neighbor is within bounds and meets the criteria
                        //  1) The neighborX,Y was in image boundary
                        //  2) This neighbor position was not visitted
                        //  3) probImage on neighbor pixel more than criteriaThreshold
                    if( neighborX >= 0 && neighborY >= 0 && neighborY < imageHeight && neighborX < imageWidth && 
                        segmentImage[ ( neighborY * imageWidth ) + neighborX ] == 0 &&
                        probImage[ ( neighborY * imageWidth ) + neighborX ] > criteriaThreshold )
                        {
                            //  Fill the segmentImage with regionLabel and add this neighbor to the currentQueue
                            segmentImage[ ( neighborY * imageWidth ) + neighborX ] = regionLabel;
                            currentQueue.push_back( std::make_pair( neighborY, neighborX ) );
                            nPixel++;
                        }
                }
            }

            regionLabel++;
        }

        return segmentImage;

    }
}
