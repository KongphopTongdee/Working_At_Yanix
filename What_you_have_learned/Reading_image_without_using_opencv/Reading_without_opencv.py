# Necessary library used for this tutorial
import numpy as np
     
# For example a particular image in this case would contain (512*512) rows and columns meaning 262,144 pixels
ROWS = 919     # hight
COLS =  879    # width
# Different images have different dimensions. Change it accordingly
   
# Opening the input image (RAW)
fin = open('Idea_leaf_white_background.png')     
print(fin)

# Loading the input image
print("... Load input image")
img = np.fromfile(fin, dtype = np.uint8, count = ROWS * COLS)
print("Dimension of the old image array: ", img.ndim)
print("Size of the old image array: ", img.size)
new_img = np.delete(img, [i for i in range(len(img)-142,len(img)-1)])
print("Size of the old image array: ", new_img.size)

# Conversion from 1D to 2D array    
new_img.shape = (379,379)
# new_img.shape = np.reshape(new_img, (2, 2), )
print("New dimension of the array:", new_img.ndim)
print("----------------------------------------------------")
print(" The 2D array of the original image is: \n", new_img)
print("----------------------------------------------------")
print("The shape of the original image array is: ", new_img.shape)

# Save the output image
print("... Save the output image")
img.astype('int8').tofile('NewImage.raw')
print("... File successfully saved")
# Closing the file
fin.close()
