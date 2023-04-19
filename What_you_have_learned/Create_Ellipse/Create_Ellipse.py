import numpy as np
import cv2
import matplotlib.pyplot as plt
import math


# Don't finish
# def draw_circle(event,x,y,flags,param):
#     global mouseX,mouseY
#     if event == cv2.EVENT_LBUTTONDBLCLK:
#         cv2.circle(img,(x,y),100,(255,0,0),-1)
#         mouseX,mouseY = x,y
        
# img = np.zeros((512,512,3), np.uint8)
# cv2.namedWindow('image')
# cv2.setMouseCallback('image',draw_circle)

# while(1):
#     cv2.imshow('image',img)
#     k = cv2.waitKey(20) & 0xFF
#     if k == 27:
#         break
#     elif k == ord('a'):
#         print(mouseX)
#         print(mouseY)
   

# Import Picture     
picture_for_creating_ellipse = cv2.imread('Lenna.png',0)
picture_for_creating_ellipse_after_resize = cv2.resize(picture_for_creating_ellipse, (600,480))

# Create function for mouse tracking
ix, iy = -1,-1 # the valiable to print out from def function to checking output
count_click = 0
position_major_start = (0,0)
position_major_end = (0,0)
position_minor_start = (0,0)
position_minor_end = (0,0)
mode_line_ellipse = True
mode_major_minor = True

# Parameter
color = (0,0,255)
thickness = 9
startAngle = 0
endAngle = 360

def create_ellipse(event,x,y,flags,param):
    global ix, iy, count_click, position_major_start, position_major_end, mode_line_ellipse, startAngle, endAngle, position_minor_end, position_minor_start
    
    if event == cv2.EVENT_LBUTTONDOWN:
        ix,iy = x,y
        # print(ix,iy)
        if mode_major_minor == True:
            if (count_click %2 == 0):
                position_major_start = (ix,iy)
                count_click += 1
                print("position_major_start" +"("+ str(ix) +","+ str(iy)+")")
            else:
                position_major_end = (ix,iy)
                count_click += 1
                print("position_major_end" +"("+ str(ix) +","+ str(iy)+")")
        
        else :
            if (count_click %2 == 0):
                position_minor_start = (ix,iy)
                count_click += 1
                print("position_minor_start" +"("+ str(ix) +","+ str(iy)+")")
            else:
                position_minor_end = (ix,iy)
                count_click += 1
                print("position_minor_end" +"("+ str(ix) +","+ str(iy)+")")
    
    elif event == cv2.EVENT_RBUTTONDOWN:
        # Calculate center_coordinates
        centorx = int((position_major_start[0]+position_major_end[0])/2)
        centory = int((position_major_start[1]+position_major_end[1])/2)
        center_coordinates = (centorx,centory)
        
        # Calculate angle
        # angle = int(abs((math.atan((position_major_end[1]-position_major_start[1])/(position_major_end[0]-position_major_start[0])))*(180/3.14)))
        angle = int((math.atan((position_major_end[1]-position_major_start[1])/(position_major_end[0]-position_major_start[0])))*(180/3.14))
        print(angle)
        
        # Calculate axesLength
        major_axes = int(math.sqrt((pow(position_major_start[0]-position_major_end[0],2))+(pow(position_major_start[1]-position_major_end[1],2))))
        miner_axes = int(math.sqrt((pow(position_minor_start[0]-position_minor_end[0],2))+(pow(position_minor_start[1]-position_minor_end[1],2))))
        axesLength = (major_axes ,miner_axes)
        
        if mode_line_ellipse == True:
            cv2.line(picture_for_creating_ellipse_after_resize, position_major_start, position_major_end, color, thickness)
        else:
            cv2.ellipse(picture_for_creating_ellipse_after_resize, center_coordinates, axesLength, angle, startAngle, endAngle, color, thickness)
    
    
# Setup using function mouse tracking
cv2.namedWindow('image_test')
cv2.setMouseCallback('image_test',create_ellipse)


# Show Picture on window
while(1):
    cv2.imshow('image_test',picture_for_creating_ellipse_after_resize)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        if(mode_line_ellipse == True):
            print("mode Create ellipse")
        else:
            print("mode Create Line")
        mode_line_ellipse = not mode_line_ellipse
    elif k == ord('n'):
        if(mode_major_minor == True):
            print("mode miner position")
        else:
            print("mode major position")
        mode_major_minor = not mode_major_minor
    elif k == 27:
        break

cv2.destroyAllWindows() 


# import numpy as np
# import cv2 as cv
# drawing = False # true if mouse is pressed
# mode_line_ellipse = True # if True, draw rectangle. Press 'm' to toggle to curve
# ix,iy = -1,-1
# # mouse callback function
# def draw_circle(event,x,y,flags,param):
#     global ix,iy,drawing,mode_line_ellipse
#     if event == cv.EVENT_LBUTTONDOWN:
#         drawing = True
#         ix,iy = x,y
#     elif event == cv.EVENT_MOUSEMOVE:
#         if drawing == True:
#             if mode_line_ellipse == True:
#                 cv.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
#             else:
#                 cv.circle(img,(x,y),5,(0,0,255),-1)
#     elif event == cv.EVENT_LBUTTONUP:
#         drawing = False
#         if mode_line_ellipse == True:
#             cv.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
#         else:
#             cv.circle(img,(x,y),5,(0,0,255),-1)
            
# img = np.zeros((512,512,3), np.uint8)
# cv.namedWindow('image')
# cv.setMouseCallback('image',draw_circle)
# while(1):
#     cv.imshow('image',img)
#     k = cv.waitKey(1) & 0xFF
#     if k == ord('m'):
#         mode_line_ellipse = not mode_line_ellipse
#     elif k == 27:
#         break
# cv.destroyAllWindows()