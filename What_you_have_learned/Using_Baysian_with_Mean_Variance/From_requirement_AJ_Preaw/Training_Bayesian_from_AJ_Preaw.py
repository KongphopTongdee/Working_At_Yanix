import cv2 
import csv
import collections
import numpy as np
import math
import matplotlib.pyplot as plt

def show_img(img):
    cv2.imshow("test",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# img_Leaf_tilted = cv2.imread("Leaf_tilted.png")
img_Leaf_straight_line = cv2.imread("Leaf_straight_line.png")

height, width, channels = img_Leaf_straight_line.shape
print("height and width of this picture " + "(" + str(height) +","+str(width) +","+str(channels) +")")

img_convert_YCRCB = cv2.cvtColor(img_Leaf_straight_line, cv2.COLOR_BGR2YCR_CB)

# cv2.rectangle(img_Leaf_straight_line, (445,470), (712,23), (0,0,255), 2)
# show_img(img_Leaf_straight_line)
# cv2.rectangle(img_Leaf_tilted, (445,470), (712,23), (0,0,255), 2)
# show_img(img_Leaf_tilted)

# พรุ่งนี้ตต้องทำมาลองสร้างค่าที่เก็บสี leaf ที่อยู่ใน position ที่เลือกแล้วทำการหา threshold บ้างค่าที่สามารถตีได้ว่าสีเขียวคือ threshold อะไร 
# ก่อนที่จะนำไปเขียน probability


# storing_color_value_list_row = []
# storing_color_value_list_all = []

# with open('color_value_rectangle_area.csv', 'w', encoding='UTF8', newline='') as f:
#     writer = csv.writer(f)
#     for height_of_picture in range(23,470):   # y position
#         for width_of_picture in range(445,712):     # x position
#             storing_color_value_list_row.append(img_Leaf_straight_line[height_of_picture][width_of_picture])
#         # print(storing_color_value_list_row)
#         storing_color_value_list_all.append(storing_color_value_list_row)
#         storing_color_value_list_row = []

#     print(storing_color_value_list_all)

#     writer.writerows(storing_color_value_list_all)  
#     storing_color_value_list_all = []  


# cv2.rectangle(img_Leaf_straight_line, (445,470), (712,23), (0,0,255), 2)
# show_img(img_Leaf_straight_line)

set_leaf = []
set_background = []


# test code for know scale of pixel

# Creating region selecting by rectangle
position_start = (0,0)      #(width,hight)
position_end = (0,0)        #(width,hight)
count_click = 0
seed_positon = (0,0)
value_of_YCrCb = (0,0,0)
Y,Cr,Cb = Y,Cr,Cb = cv2.split(img_convert_YCRCB)
# Y,Cr,Cb = Y,Cr,Cb = cv2.split(img_Leaf_straight_line)

#use only matplotlib to plot the scale 
plt.imshow(img_convert_YCRCB)
plt.show()
# plt.imshow(Y)
# plt.show()
# plt.imshow(Cr)
# plt.show()
# plt.imshow(Cb)
# plt.show()


# not use
# def Position_of_value(event,x,y,flags,param):
#     global img_Leaf_straight_line,count_click, position_start, position_end, seed_positon, value_of_YCrCb
    
#     if (event == cv2.EVENT_LBUTTONDOWN):
#         # if (count_click %2 == 0):
#         #     position_start = (x,y)
#         #     count_click += 1
#         #     print("position_start" +"("+ str(x) +","+ str(y)+")")
#         # else:
#         #     position_end = (x,y)
#         #     count_click += 1
#         #     print("position_end" +"("+ str(x) +","+ str(y)+")")
#         seed_positon = (x,y)
#         value_of_YCrCb = (Y[x][y], Cr[x][y], Cb[x][y])
#         print("seed_position " +"("+ str(x) +","+ str(y)+")")
#         print(value_of_YCrCb)
        
            
#     # elif(event == cv2.EVENT_RBUTTONDOWN):
#     #     cv2.rectangle(img_Leaf_straight_line, position_start, position_end, (0,0,255), 2)
 
 
# cv2.namedWindow('Leaf_straight_line')
# cv2.setMouseCallback('Leaf_straight_line',Position_of_value) 
 

# # การคำนวนรูปภาพกับตัว show รูปภาพใช้คนละตัวกัน คำนวนใช้ color model = Y,Cr,Cb แต่ output รูปภาพใช้ R,G,B

# while(1):
#     cv2.imshow('Leaf_straight_line', img_Leaf_straight_line)
#     k = cv2.waitKey(1) & 0xFF
    
#     if k == 27:
#         break

# cv2.destroyAllWindows()

