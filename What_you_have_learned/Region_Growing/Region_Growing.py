import cv2
import numpy as np

picture_for_region_growing = cv2.imread('Lenna.png', 0)

# สีที่ได้จะเป็นสีที่อยู่ในช่วงของ 0-255 ที่เป็น 1 channels เท่านั้น
# print(picture_for_region_growing)

height ,width = picture_for_region_growing.shape

seed_region = (0,0)
color_of_seed = 0
Threshold = 128 # the number at the middle of color

# Creating region selecting by rectangle
position_start = (0,0)      #(width,hight)
position_end = (0,0)        #(width,hight)
mode_rectangle_position = True
count_click = 0

def region_growing(event,x,y,flags,param):
    global seed_region, color_of_seed, Threshold, picture_for_region_growing,count_click, position_start, position_end
    
    if (event == cv2.EVENT_LBUTTONDOWN):
        if mode_rectangle_position  == True:
            if (count_click %2 == 0):
                position_start = (x,y)
                count_click += 1
                print("position_start" +"("+ str(x) +","+ str(y)+")")
            else:
                position_end = (x,y)
                count_click += 1
                print("position_end" +"("+ str(x) +","+ str(y)+")")
        else :
            seed_region = (x,y)
            print("The Position of seed : " + str(seed_region))
            color_of_seed = picture_for_region_growing[x][y]
            print("The Color of the seed position : " + str(color_of_seed))
              
    elif(event == cv2.EVENT_RBUTTONDOWN):
        if mode_rectangle_position  == True:
            cv2.rectangle(picture_for_region_growing, position_start, position_end, (0,0,255), 2)
        else :
            for height_of_picture in range(position_start[1],position_end[1]):
                for width_of_picture in range(position_start[0],position_end[0]):
                    if ((picture_for_region_growing[height_of_picture][width_of_picture] - seed_region) < Threshold).all():
                        picture_for_region_growing[height_of_picture][width_of_picture] = 255
                    else:
                        picture_for_region_growing[height_of_picture][width_of_picture] = 0
 
 
cv2.namedWindow('Lenna_test_picture')
cv2.setMouseCallback('Lenna_test_picture',region_growing) 
 

while(1):
    cv2.imshow('Lenna_test_picture', picture_for_region_growing)
    k = cv2.waitKey(1) & 0xFF
    
    if k == ord('m'):
        mode_rectangle_position = not mode_rectangle_position
    
    elif k == 27:
        break

cv2.destroyAllWindows()