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

def cal_prob_of_score_and_class(color_space, x, y, mean_of_class, std_of_class):
    # equation 
    # P(S|C) = (1/(standard_deviation*squareroot(2*pi)))(exp((-1/2)((current_pixel-mean)^2/standard_deviation)))
    Ans = 0.0
    
    Ans = (1/(std_of_class*math.sqrt(2*math.pi)))*(math.exp((-1/2)*(math.pow((color_space[x][y]-mean_of_class),2)/math.pow((std_of_class),2))))
    
    return Ans

# Calculate_Probability_Region_of_interesting
def cal_prob_roi(interestsample,notinterestsample,prob_of_score_and_class,prob_of_score_and_notclass):
    # equation 
    # P(C|S) = 1/(1+((P(~C)*P(S|~C))/(P(C)*P(S|C))))
    # เมื่อ P(C|S) = class ที่เราสนใจใน score นั้นๆ เช่น probability ของใบไม้(class)ใน mean(score)
    # P(~C) = จำนวน sample ทั้งหมดที่ไม่ใช่ใบไม้(class)
    # P(C) = จำนวน sample ทั้งหมดที่เป็นใบไม้(class)
    # P(S|C) = likelihood เป็นค่า prob ที่เลือกใน distribution เช่น plot histogram ออกมาแล้วทำการหาว่าสีเขียวหรือสีที่เราต้องการใน dishapestribution นั้นๆมีค่าเท่ากับเท่าไรแล้วนำมาหารด้วยทั้งหมด
        #    = distribution class in mean Y, mean Cr, mean Cb and std Y, std Cr, Std Cb
    # P(S|~C) = likelihood เป็นค่า prob ที่ไม่เลือกใน distribution เช่น plot histogram ออกมาแล้วทำการหาว่าสีเขียวหรือสีที่เราต้องการใน distribution นั้นๆมีค่าเท่ากับเท่าไรแล้วนำมาหารด้วยทั้งหมด
        #    = distribution not class in mean Y, mean Cr, mean Cb and std Y, std Cr, Std Cb
    Ans = 0.0
    All_sample = interestsample + notinterestsample
    Ans = 1/(1+(((notinterestsample/All_sample)*prob_of_score_and_notclass)/((interestsample/All_sample)*prob_of_score_and_class)))
    
    return Ans

img_Idea_ROI_white_background = cv2.imread("Idea_ROI_white_background.png")

height, width, channels = img_Idea_ROI_white_background.shape
print("height and width of this picture " + "(" + str(height) +","+str(width) +","+str(channels) +")")

img_convert_YCRCB = cv2.cvtColor(img_Idea_ROI_white_background, cv2.COLOR_BGR2YCR_CB)
img_convert_RGB = cv2.cvtColor(img_Idea_ROI_white_background, cv2.COLOR_BGR2RGB)
# Y,Cr,Cb = cv2.split(img_convert_YCRCB)
Red,Green,Blue = cv2.split(img_convert_RGB)
original_Red,original_Green,original_Blue = np.copy(Red),np.copy(Green),np.copy(Blue)

# rectangle of meanandvariance
rectangle_position = [(333,177),(736,307),(668,917),(264,515),(578,549),(805,271),(888,269),(808,331),(821,408),(798,457),(797,535),(733,432),(737,375),(650,372),(645,316)]
for i in range(len(rectangle_position)):
    if i <= 4:
        # mean kernel colour = black
        rectangle_kernel = calculate_expand_kernel(rectangle_position[i][0],rectangle_position[i][1],25)
        cv2.rectangle(img_convert_RGB, rectangle_kernel[0], rectangle_kernel[1], (0,0,0), 1)
    elif i > 4:
        # variance kernel colour = red
        rectangle_kernel = calculate_expand_kernel(rectangle_position[i][0],rectangle_position[i][1],25)
        cv2.rectangle(img_convert_RGB, rectangle_kernel[0], rectangle_kernel[1], (255,0,0), 1)

# rectangle of probabilityandBayesian
# bayesian kernel colour = green        
cv2.rectangle(img_convert_RGB, (840,20), (629,629), (0,255,0), 1)

show_img_matplotlib(img_convert_RGB)

# cv2.rectangle(img_convert_RGB, (328,177), (610,750), (0,0,255), 1)        # ขนาด pixel ที่จะนำมาใช้
# seed_post = (364,278)
# cv2.circle(img_convert_RGB, seed_post, radius=0, color=(0, 0, 0), thickness=10)


# Step of working
# step 1. ทำการหา region growing เพื่อทำการตั้ง threshold ที่เอาเฉพาะค่าใบไม้มาใช้ โดยถ้าเป็นใบไม้จะให้เป็นสีขาวแต่ถ้าเป็นสิ่งที่ไม่สำคัญจะให้เป็นสีดำ(เนื่องจากว่าการ region growing ที่ง่ายที่สุดจะเป็นภาพขาวดำ)
# step 2. ทำการหา interestsample,notinterestsample จากการนับเฉพาะสีขาวจาก region growing
# step 3. ทำการหา prob_of_score_and_class, prob_of_score_and_notclass โดยการคำนวน equation ที่ผนวกค่า current position, mean, standard deviation
# step 4. นำค่าที่คำนวนออกมาไปเก็บใน class เพื่อดึงมาใช้งานที่ง่ายขึ้น
# step 5. สุดท้ายนำไปใส่ในสมการ calculate bayesian probability ที่หา class(leaf)|score(mean,std of Y,Cr,Cb)

# step 1. ทำการหา region growing เพื่อทำการตั้ง threshold ที่เอาเฉพาะค่าใบไม้มาใช้ โดยถ้าเป็นใบไม้จะให้เป็นสีขาวแต่ถ้าเป็นสิ่งที่ไม่สำคัญจะให้เป็นสีดำ
# เนื่องจากว่าการ region growing ที่ง่ายที่สุดจะเป็นภาพขาวดำ
# Valiable
# coordinates (x,y)
position_of_seed = (364,278)
# threshold_seed_position = calculate_mean_of_postion(position_of_seed,Red,Green,Blue)
threshold_seed_position = calculate_mean_of_postion(position_of_seed[0],position_of_seed[1],Red,Green,Blue)
position_of_start= (328,177)
position_of_end = (610,750)


for row in range(position_of_start[1], position_of_end[1]):       # y axis
    for coloumn in range(position_of_start[0], position_of_end[0]):       # x axis
        if (calculate_mean_of_postion(row,coloumn,Red,Green,Blue) < threshold_seed_position) :
            Red[row][coloumn] = 0
            Green[row][coloumn] = 0
            Blue[row][coloumn] = 0

# step 2. ทำการหา interestsample,notinterestsample จากการนับเฉพาะสีขาวจาก region growing
# Valiable
interestpixels = 0
not_interestpixels = 0

for row in range(position_of_start[1], position_of_end[1]):       # y axis
    for coloumn in range(position_of_start[0], position_of_end[0]):       # x axis
        if (calculate_mean_of_postion(row,coloumn,Red,Green,Blue) == 0) :
            interestpixels += 1
        else :
            not_interestpixels += 1

# step 3. ทำการหา prob_of_score_and_class, prob_of_score_and_notclass โดยการคำนวน equation ที่ผนวกค่า current position, mean, standard deviation
# Valiable
all_mean_leaf = (0,0,0)
mean_R_leaf = 0
mean_G_leaf = 0
mean_B_leaf = 0
all_std_leaf = (0,0,0)
std_R_leaf = 0
std_G_leaf = 0
std_B_leaf = 0
all_mean_notleaf = (0,0,0)

mean_R_notleaf = 0
mean_G_notleaf = 0
mean_B_notleaf = 0
all_std_notleaf = (0,0,0)
std_R_notleaf = 0
std_G_notleaf = 0
std_B_notleaf = 0

for row in range(position_of_start[1], position_of_end[1]):       # y axis
    for coloumn in range(position_of_start[0], position_of_end[0]):       # x axis
        if (calculate_mean_of_postion(row,coloumn,Red,Green,Blue) == 0):
            mean_R_leaf += original_Red[row][coloumn]
            mean_G_leaf += original_Green[row][coloumn]
            mean_B_leaf += original_Blue[row][coloumn]
        else :
            mean_R_notleaf += original_Red[row][coloumn]
            mean_G_notleaf += original_Green[row][coloumn]
            mean_B_notleaf += original_Blue[row][coloumn]

mean_R_leaf = (mean_R_leaf/interestpixels)
mean_G_leaf = (mean_G_leaf/interestpixels)
mean_B_leaf = (mean_B_leaf/interestpixels)
all_mean_leaf = (mean_R_leaf, mean_G_leaf, mean_B_leaf)
mean_R_notleaf = (mean_R_notleaf/not_interestpixels)
mean_G_notleaf = (mean_G_notleaf/not_interestpixels)
mean_B_notleaf = (mean_B_notleaf/not_interestpixels)
all_mean_notleaf = (mean_R_notleaf, mean_G_notleaf, mean_B_notleaf)

for row in range(position_of_start[1], position_of_end[1]):       # y axis
    for coloumn in range(position_of_start[0], position_of_end[0]):       # x axis
        if (calculate_mean_of_postion(row,coloumn,Red,Green,Blue) == 0):
            std_R_leaf += pow((original_Red[row][coloumn] - mean_R_leaf),2)
            std_G_leaf += pow((original_Green[row][coloumn] - mean_G_leaf),2)
            std_B_leaf += pow((original_Blue[row][coloumn] - mean_B_leaf),2)
        else :
            std_R_notleaf += pow((original_Red[row][coloumn] - mean_R_leaf),2)
            std_G_notleaf += pow((original_Green[row][coloumn] - mean_G_leaf),2)
            std_B_notleaf += pow((original_Blue[row][coloumn] - mean_B_leaf),2)

std_R_leaf = math.sqrt(std_R_leaf/interestpixels)
std_G_leaf = math.sqrt(std_G_leaf/interestpixels)
std_B_leaf = math.sqrt(std_B_leaf/interestpixels)
all_std_leaf = (std_R_leaf, std_G_leaf, std_B_leaf)
std_R_notleaf = math.sqrt(std_R_notleaf/not_interestpixels)
std_G_notleaf = math.sqrt(std_G_notleaf/not_interestpixels)
std_B_notleaf = math.sqrt(std_B_notleaf/not_interestpixels)
all_std_notleaf = (std_R_notleaf, std_G_notleaf, std_B_notleaf)

# step 4. นำค่าที่คำนวนออกมาไปเก็บใน class เพื่อดึงมาใช้งานที่ง่ายขึ้น
# Create class storage varialble
StoreROIleaf = statistical_analysis()
StoreNotROIleaf = statistical_analysis()

# update value in class
StoreROIleaf.update_num_of_pixels(interestpixels)
StoreROIleaf.update_mean_RGB(all_mean_leaf)
StoreROIleaf.update_std_RGB(all_std_leaf)
StoreNotROIleaf.update_num_of_pixels(not_interestpixels)
StoreNotROIleaf.update_mean_RGB(all_mean_notleaf)
StoreNotROIleaf.update_std_RGB(all_std_notleaf)

print("Mean_R_interest,Mean_G_interest,Mean_B_interest")
print(StoreROIleaf.get_mean_value())
print("Mean_R_Not_interest,Mean_G_Not_interest,Mean_B_Not_interest")
print(StoreNotROIleaf.get_mean_value())
print("Std_R_interest,Std_G_interest,Std_B_interest")
print(StoreROIleaf.get_std_value())
print("Std_R_Not_interest,Std_G_Not_interest,Std_B_Not_interest")
print(StoreNotROIleaf.get_std_value())



# step 5. สุดท้ายนำไปใส่ในสมการ calculate bayesian probability ที่หา class(leaf)|score(mean,std of R,G,B)
# Value
Bayes_prob_classleaf_given_scoreR = 0.0
Bayes_prob_classleaf_given_scoreG = 0.0
Bayes_prob_classleaf_given_scoreB = 0.0

prob_scoreR_given_classleaf = 0.0
prob_scoreG_given_classleaf = 0.0
prob_scoreB_given_classleaf = 0.0

prob_scoreR_given_not_classleaf = 0.0
prob_scoreG_given_not_classleaf = 0.0
prob_scoreB_given_not_classleaf = 0.0

# ทำการคำนวน bayesian ของแต่ละ pixels แล้วทำการแทนเข้าไปในภาพ
# Valiable
store_the_bayesian_channel_R = np.zeros((height,width))
store_the_bayesian_channel_G = np.zeros((height,width))
store_the_bayesian_channel_B = np.zeros((height,width))

for row in range(position_of_start[1], position_of_end[1]):       # y axis
    for coloumn in range(position_of_start[0], position_of_end[0]):       # x axis
        prob_scoreR_given_classleaf = cal_prob_of_score_and_class(original_Red, row, coloumn, StoreROIleaf.mean_value_R, StoreROIleaf.std_value_R)
        prob_scoreR_given_not_classleaf = cal_prob_of_score_and_class(original_Red, row, coloumn, StoreNotROIleaf.mean_value_R, StoreNotROIleaf.std_value_R)
        store_the_bayesian_channel_R[row][coloumn] = cal_prob_roi(StoreROIleaf.get_num_of_pixels(), StoreNotROIleaf.get_num_of_pixels(), prob_scoreR_given_classleaf, prob_scoreR_given_not_classleaf)
        
        prob_scoreG_given_classleaf = cal_prob_of_score_and_class(original_Green, row, coloumn, StoreROIleaf.mean_value_G, StoreROIleaf.std_value_G)
        prob_scoreG_given_not_classleaf = cal_prob_of_score_and_class(original_Green, row, coloumn, StoreNotROIleaf.mean_value_G, StoreNotROIleaf.std_value_G)
        store_the_bayesian_channel_G[row][coloumn] = cal_prob_roi(StoreROIleaf.get_num_of_pixels(), StoreNotROIleaf.get_num_of_pixels(), prob_scoreG_given_classleaf, prob_scoreG_given_not_classleaf)
        
        prob_scoreB_given_classleaf = cal_prob_of_score_and_class(original_Green, row, coloumn, StoreROIleaf.mean_value_B, StoreROIleaf.std_value_B)
        prob_scoreB_given_not_classleaf = cal_prob_of_score_and_class(original_Green, row, coloumn, StoreNotROIleaf.mean_value_B, StoreNotROIleaf.std_value_B)
        store_the_bayesian_channel_B[row][coloumn] = cal_prob_roi(StoreROIleaf.get_num_of_pixels(), StoreNotROIleaf.get_num_of_pixels(), prob_scoreB_given_classleaf, prob_scoreB_given_not_classleaf)

image_bayesian = merge_picture(store_the_bayesian_channel_R, store_the_bayesian_channel_G, store_the_bayesian_channel_B)
show_img_cv2(image_bayesian)
