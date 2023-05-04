import cv2 
import numpy as np
import math
import matplotlib.pyplot as plt

# Store all value
class statistical_analysis:
    def __init__(self, num_of_pixels, mean_value, std_value):
        self.num_of_pixels = num_of_pixels
        self.mean_value_R,self.mean_value_G,self.mean_value_B = mean_value[0],mean_value[1],mean_value[2]
        self.std_value_R,self.std_value_G,self.std_value_B = std_value[0],std_value[1],std_value[2]

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

def cal_prob_of_score_and_class(current_pixel, mean_of_class, std_of_class):
    # equation 
    # P(S|C) = (1/(standard_deviation*squareroot(2*pi)))(exp((-1/2)((current_pixel-mean)^2/standard_deviation)))
    Ans = 0.0
    
    Ans = (1/(std_of_class*math.sqrt(2*math.pi)))*(math.exp((-1/2)*(math.pow((current_pixel-mean_of_class),2)/math.pow((std_of_class),2))))
    
    return Ans

# Calculate_Probability_Region_of_interesting
def cal_prob_roi(interestsample,notinterestsample,prob_of_score_and_class,prob_of_score_and_notclass):
    # equation 
    # P(C|S) = 1/(1+((P(~C)*P(S|~C))/(P(C)*P(S|C))))
    # เมื่อ P(C|S) = class ที่เราสนใจใน score นั้นๆ เช่น probability ของใบไม้(class)ใน mean(score)
    # P(~C) = จำนวน sample ทั้งหมดที่ไม่ใช่ใบไม้(class)
    # P(C) = จำนวน sample ทั้งหมดที่เป็นใบไม้(class)
    # P(S|C) = likelihood เป็นค่า prob ที่เลือกใน distribution เช่น plot histogram ออกมาแล้วทำการหาว่าสีเขียวหรือสีที่เราต้องการใน distribution นั้นๆมีค่าเท่ากับเท่าไรแล้วนำมาหารด้วยทั้งหมด
        #    = distribution class in mean Y, mean Cr, mean Cb and std Y, std Cr, Std Cb
    # P(S|~C) = likelihood เป็นค่า prob ที่ไม่เลือกใน distribution เช่น plot histogram ออกมาแล้วทำการหาว่าสีเขียวหรือสีที่เราต้องการใน distribution นั้นๆมีค่าเท่ากับเท่าไรแล้วนำมาหารด้วยทั้งหมด
        #    = distribution not class in mean Y, mean Cr, mean Cb and std Y, std Cr, Std Cb
    Ans = 0.0
    
    Ans = 1/(1+((notinterestsample*prob_of_score_and_notclass)/(interestsample*prob_of_score_and_class)))
    
    return Ans

img_Idea_leaf_white_background = cv2.imread("Idea_leaf_white_background.png")

height, width, channels = img_Idea_leaf_white_background.shape
print("height and width of this picture " + "(" + str(height) +","+str(width) +","+str(channels) +")")

img_convert_YCRCB = cv2.cvtColor(img_Idea_leaf_white_background, cv2.COLOR_BGR2YCR_CB)
img_convert_RGB = cv2.cvtColor(img_Idea_leaf_white_background, cv2.COLOR_BGR2RGB)
# Y,Cr,Cb = cv2.split(img_convert_YCRCB)
Red,Green,Blue = cv2.split(img_convert_RGB)
original_Red,original_Green,original_Blue = np.copy(Red),np.copy(Green),np.copy(Blue)

# cv2.rectangle(img_convert_RGB, (328,177), (547,750), (0,0,255), 1)        # ขนาด pixel ที่จะนำมาใช้
# seed_post = (364,278)

# Step of working
# 1. ทำการหา region growing เพื่อทำการตั้ง threshold ที่เอาเฉพาะค่าใบไม้มาใช้ โดยถ้าเป็นใบไม้จะให้เป็นสีขาวแต่ถ้าเป็นสิ่งที่ไม่สำคัญจะให้เป็นสีดำ
# 2. ทำการหา interestsample,notinterestsample จากการนับเฉพาะสีขาวจาก region growing
# 3. ทำการหา prob_of_score_and_class, prob_of_score_and_notclass โดยการคำนวน equation ที่ผนวกค่า current position, mean, standard deviation
# 4. สุดท้ายนำไปใส่ในสมการ calculate bayesian probability ที่หา class(leaf)|score(mean,std of Y,Cr,Cb)

# step 1. ทำการหา region growing เพื่อทำการตั้ง threshold ที่เอาเฉพาะค่าใบไม้มาใช้ โดยถ้าเป็นใบไม้จะให้เป็นสีขาวแต่ถ้าเป็นสิ่งที่ไม่สำคัญจะให้เป็นสีดำ
# เนื่องจากว่าการ region growing ที่ง่ายที่สุดจะเป็นภาพขาวดำ
# Valiable
# coordinates (x,y)
position_of_seed = (364,278)
# threshold_seed_position = calculate_mean_of_postion(position_of_seed,Red,Green,Blue)
threshold_seed_position = calculate_mean_of_postion(position_of_seed[0],position_of_seed[1],Red,Green,Blue)
position_of_start= (328,177)
position_of_end = (547,750)


for row in range(position_of_start[1], position_of_end[1]):       # y axis
    for coloumn in range(position_of_start[0], position_of_end[0]):       # x axis
        if calculate_mean_of_postion(row,coloumn,Red,Green,Blue) < threshold_seed_position :
            Red[row][coloumn] = 0
            Green[row][coloumn] = 0
            Blue[row][coloumn] = 0

# step 2. ทำการหา interestsample,notinterestsample จากการนับเฉพาะสีขาวจาก region growing
# Valiable
set_leaf = 0
set_notleaf = 0

for row in range(position_of_start[1], position_of_end[1]):       # y axis
    for coloumn in range(position_of_start[0], position_of_end[0]):       # x axis
        if calculate_mean_of_postion(row,coloumn,Red,Green,Blue) == 0 :
            set_leaf += 1
        else :
            set_notleaf += 1

# step 3. ทำการหา prob_of_score_and_class, prob_of_score_and_notclass โดยการคำนวน equation ที่ผนวกค่า current position, mean, standard deviation















# step 4. สุดท้ายนำไปใส่ในสมการ calculate bayesian probability ที่หา class(leaf)|score(mean,std of Y,Cr,Cb)





















