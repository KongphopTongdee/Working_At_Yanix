# # Python program to explain cv2.ellipse() method
	
# # importing cv2
# import cv2
	
	
# # Reading an image in default mode
# image = cv2.imread('wallpaper_neon_valley.jpg')

# image = cv2.resize(image, (1280,720))
	
# # Window name in which image is displayed
# window_name = 'Image'

# center_coordinates = (500, 500)

# axesLength = (100*2, 50*2)

# angle = 30

# startAngle = 0

# endAngle = 360

# # Blue color in BGR
# color = (255, 0, 0)

# # Line thickness of -1 px
# thickness = -1

# # Using cv2.ellipse() method
# # Draw a ellipse with blue line borders of thickness of -1 px
# image = cv2.ellipse(image, center_coordinates, axesLength, angle,
# 						startAngle, endAngle, color, thickness)

# # Displaying the image
# cv2.imshow(window_name, image)
# cv2.waitKey()
# cv2.destroyAllWindows() 





# # import numpy as np

# # position_start = (255,266)
# # position_end = (500,900)

# # centorx = int((position_start[0]+position_end[0])/2)
# # centory = int((position_start[1]+position_end[1])/2)

# # center = (centorx,centory)

# # print(center)

# x = pow(7,2)

# print(x)

# y = 36.885
# y = int(y)
# print(y)

import numpy as np
import math

x1,y1 = 5,1

x2,y2 = 1,4

print(x1,y1,x2,y2)
    
angle = int(abs((math.atan((y2-y1)/(x2-x1)))*(180/3.14)))

print(angle)

# angle2 = ((y2-y1)/(x2-x1))

# print(angle2)