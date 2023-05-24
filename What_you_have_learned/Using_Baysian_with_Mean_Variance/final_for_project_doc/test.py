import cv2 
import numpy as np
import math
import matplotlib.pyplot as plt
from Store_analysis_class_ROI import statistical_analysis

def calculate_expand_kernel(seed_position_x,seed_position_y,expand_kernel):
    Top_Right_position = (seed_position_x+expand_kernel,seed_position_y-expand_kernel)
    Bottom_Left_position = (seed_position_x-expand_kernel,seed_position_y+expand_kernel)
    return Top_Right_position,Bottom_Left_position

def show_img_cv2(img):
    cv2.imshow("test",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def show_img_matplotlib(img):
    #use only matplotlib to plot the scale 
    plt.imshow(img)
    plt.show()
    
def merge_picture(colorRarray,colorGarray,colorBarray):
    Ans = cv2.merge((colorRarray,colorGarray,colorBarray))
    return Ans
    
def calculate_mean_of_postion(x,y,colorRarray,colorGarray,colorBarray):
    Ans = 0
    mean = 0
    # x,y = position[0],position[1]
    R,G,B = colorRarray[x][y],colorGarray[x][y],colorBarray[x][y]
    mean = np.sum([R,G,B])
    mean = np.divide(mean,3)
    Ans = mean
    return Ans

img_Idea_ROI_white_background = cv2.imread("Idea_ROI_white_background_little_movement.png")

height, width, channels = img_Idea_ROI_white_background.shape
print("height and width of this picture " + "(" + str(height) +","+str(width) +","+str(channels) +")")

img_convert_RGB = cv2.cvtColor(img_Idea_ROI_white_background, cv2.COLOR_BGR2RGB)
Red,Green,Blue = cv2.split(img_convert_RGB)
original_Red,original_Green,original_Blue = np.copy(Red),np.copy(Green),np.copy(Blue)

# # rectangle of meanandvariance
# rectangle_position = [(333,177),(736,307),(668,917),(264,515),(578,549),(805,271),(888,269),(808,331),(821,408),(798,457),(797,535),(733,432),(737,375),(650,372),(645,316)]
# for i in range(len(rectangle_position)):
#     if i <= 4:
#         # mean kernel colour = black
#         rectangle_kernel = calculate_expand_kernel(rectangle_position[i][0],rectangle_position[i][1],25)
#         cv2.rectangle(img_convert_RGB, rectangle_kernel[0], rectangle_kernel[1], (0,0,0), 1)
#     elif i > 4:
#         # variance kernel colour = red
#         rectangle_kernel = calculate_expand_kernel(rectangle_position[i][0],rectangle_position[i][1],25)
#         cv2.rectangle(img_convert_RGB, rectangle_kernel[0], rectangle_kernel[1], (255,0,0), 1)

# rectangle of probabilityandBayesian
# # bayesian kernel colour = green     
# cv2.rectangle(img_convert_RGB, (840,20), (629,629), (0,255,0), 1)
rectangle_position = [(888,269),(805,271),(808,331),(821,408),(798,457),(797,535),(737,375),(733,432),(645,316),(650,372)]

for i in rectangle_position:
    rectangle_kernel = calculate_expand_kernel(i[0],i[1],25)

    position_of_start= rectangle_kernel[0]
    position_of_end = rectangle_kernel[1]

    cv2.rectangle(img_convert_RGB, rectangle_kernel[0], rectangle_kernel[1], (0,0,0), 1)

    show_img_matplotlib(img_convert_RGB)

    all_mean = (0,0,0)
    mean_R = 0
    mean_G = 0
    mean_B = 0
    pixelscount = 0

    for row in range(position_of_start[1], position_of_end[1]):       # y axis
        for coloumn in range(position_of_end[0], position_of_start[0]):       # x axis
            mean_R += original_Red[row][coloumn]
            mean_G += original_Green[row][coloumn]
            mean_B += original_Blue[row][coloumn]
            pixelscount += 1

    mean_R = (mean_R/pixelscount)
    mean_G = (mean_G/pixelscount)
    mean_B = (mean_B/pixelscount)
    all_mean = (mean_R, mean_G, mean_B)
    print("Mean_of_picture")
    print(all_mean)


    all_std = (0,0,0)
    std_R = 0
    std_G = 0
    std_B = 0
    for row in range(position_of_start[1], position_of_end[1]):       # y axis
        for coloumn in range(position_of_end[0], position_of_start[0]):       # x axis
            std_R += pow((original_Red[row][coloumn] - mean_R),2)
            std_G += pow((original_Green[row][coloumn] - mean_G),2)
            std_B += pow((original_Blue[row][coloumn] - mean_B),2)

    std_R = math.sqrt(std_R/pixelscount)
    std_G = math.sqrt(std_G/pixelscount)
    std_B = math.sqrt(std_B/pixelscount)
    all_std = (std_R, std_G, std_B)
    print("Standard_deviation_of_picture")
    print(all_std)
