import cv2 
import csv
import collections
import numpy as np
import math

def show_img(img):
    cv2.imshow("test",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img_Leaf_tilted = cv2.imread("Leaf_tilted.png")
img_Leaf_straight_line = cv2.imread("Leaf_straight_line.png",0)

# cv2.rectangle(img_Leaf_straight_line, (445,470), (712,23), (0,0,255), 2)
# show_img(img_Leaf_straight_line)
# cv2.rectangle(img_Leaf_tilted, (445,470), (712,23), (0,0,255), 2)
# show_img(img_Leaf_tilted)

# พรุ่งนี้ตต้องทำมาลองสร้างค่าที่เก็บสี leaf ที่อยู่ใน position ที่เลือกแล้วทำการหา threshold บ้างค่าที่สามารถตีได้ว่าสีเขียวคือ threshold อะไร 
# ก่อนที่จะนำไปเขียน probability


set_leaf = []
set_background = []







# test code for know scale of pixel

# # Creating region selecting by rectangle
# position_start = (0,0)      #(width,hight)
# position_end = (0,0)        #(width,hight)
# count_click = 0

# def region_growing(event,x,y,flags,param):
#     global img_Leaf_straight_line,count_click, position_start, position_end
    
#     if (event == cv2.EVENT_LBUTTONDOWN):
#         if (count_click %2 == 0):
#             position_start = (x,y)
#             count_click += 1
#             print("position_start" +"("+ str(x) +","+ str(y)+")")
#         else:
#             position_end = (x,y)
#             count_click += 1
#             print("position_end" +"("+ str(x) +","+ str(y)+")")
            
#     elif(event == cv2.EVENT_RBUTTONDOWN):
#         cv2.rectangle(img_Leaf_straight_line, position_start, position_end, (0,0,255), 2)
 
 
# cv2.namedWindow('Lenna_test_picture')
# cv2.setMouseCallback('Lenna_test_picture',region_growing) 
 

# while(1):
#     cv2.imshow('Lenna_test_picture', img_Leaf_straight_line)
#     k = cv2.waitKey(1) & 0xFF
    
#     if k == 27:
#         break

# cv2.destroyAllWindows()

