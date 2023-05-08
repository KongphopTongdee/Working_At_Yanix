import cv2 
import numpy as np
import math
import matplotlib.pyplot as plt

# Store all value
# class statistical_analysis:
#     def __init__(self, num_of_pixels, mean_value, std_value):
#         self.num_of_pixels = num_of_pixels
#         self.mean_value_R,self.mean_value_G,self.mean_value_B = mean_value[0],mean_value[1],mean_value[2]
#         self.std_value_R,self.std_value_G,self.std_value_B = std_value[0],std_value[1],std_value[2]
        
class statistical_analysis:
    def __init__(self):
        self.num_of_pixels = 0
        self.mean_value_R = 0
        self.mean_value_G = 0
        self.mean_value_B = 0
        self.std_value_R = 0
        self.std_value_G = 0
        self.std_value_B = 0
        self.Bayesian_plus_value_R = 0
        self.Bayesian_plus_value_G = 0
        self.Bayesian_plus_value_B = 0
        self.Bayesian_times_value_R = 0
        self.Bayesian_times_value_G = 0
        self.Bayesian_times_value_B = 0
    def update_num_of_pixels(self, num_pixels):
        self.num_of_pixels = num_pixels
    def update_mean_RGB(self, mean_value):
        self.mean_value_R,self.mean_value_G,self.mean_value_B = mean_value[0],mean_value[1],mean_value[2]
    def update_std_RGB(self, std_value):
        self.std_value_R,self.std_value_G,self.std_value_B = std_value[0],std_value[1],std_value[2]
    def update_plus_Bayesian(self, Baye_plus_value):
        self.Bayesian_plus_value_R,self.Bayesian_plus_value_G,self.Bayesian_plus_value_B = Baye_plus_value[0],Baye_plus_value[1],Baye_plus_value[2]
    def update_times_Bayesian(self, Baye_times_value):
        self.Bayesian_times_value_R,self.Bayesian_times_value_G,self.Bayesian_times_value_B = Baye_times_value[0],Baye_times_value[1],Baye_times_value[2]
    def get_num_of_pixels(self):
        return self.num_of_pixels
    def get_mean_value(self):
        return self.mean_value_R,self.mean_value_G,self.mean_value_B
    def get_std_value(self):
        return self.std_value_R,self.std_value_G,self.std_value_B
    def get_plus_Bayesian_value(self):
        return self.Bayesian_plus_value_R,self.Bayesian_plus_value_G,self.Bayesian_plus_value_B
    def get_times_Bayesian_value(self):
        return self.Bayesian_times_value_R,self.Bayesian_times_value_G,self.Bayesian_times_value_B
    

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

# print(all_mean_leaf)
# print(all_mean_notleaf)

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

# print(all_std_leaf)
# print(all_std_notleaf)

# step 4. นำค่าที่คำนวนออกมาไปเก็บใน class เพื่อดึงมาใช้งานที่ง่ายขึ้น

StoreROIleaf = statistical_analysis()
StoreNotROIleaf = statistical_analysis()

# update value in class
StoreROIleaf.update_num_of_pixels(interestpixels)
StoreROIleaf.update_mean_RGB(all_mean_leaf)
StoreROIleaf.update_std_RGB(all_std_leaf)
StoreNotROIleaf.update_num_of_pixels(not_interestpixels)
StoreNotROIleaf.update_mean_RGB(all_mean_notleaf)
StoreNotROIleaf.update_std_RGB(all_std_notleaf)

# print(StoreROIleaf.num_of_pixels)
# print(StoreROIleaf.mean_value_R)
# print(StoreROIleaf.mean_value_G)
# print(StoreROIleaf.mean_value_B)
# print(StoreROIleaf.std_value_R)
# print(StoreROIleaf.std_value_G)
# print(StoreROIleaf.std_value_B)
# print(StoreROIleaf.get_num_of_pixels())
# print(StoreROIleaf.get_mean_value())
# print(StoreROIleaf.get_std_value())


# step 5. สุดท้ายนำไปใส่ในสมการ calculate bayesian probability ที่หา class(leaf)|score(mean,std of Y,Cr,Cb)
# Value
Bayes_prob_classleaf_given_scoreR = 0.0
Bayes_prob_classleaf_given_scoreG = 0.0
Bayes_prob_classleaf_given_scoreB = 0.0
all_bayes_prob_classleaf_given_scoreRGB = (0.0, 0.0, 0.0)

prob_scoreR_given_classleaf = 0.0
prob_scoreG_given_classleaf = 0.0
prob_scoreB_given_classleaf = 0.0
all_prob_scoreRGB_given_classleaf = (0.0, 0.0, 0.0)
prob_scoreR_given_not_classleaf = 0.0
prob_scoreG_given_not_classleaf = 0.0
prob_scoreB_given_not_classleaf = 0.0
all_prob_scoreRGB_given_not_classleaf = (0.0, 0.0, 0.0)

# ในขั้นตอนนี้เราจะทำการคำนวน prob scoreRGB given class leaf ด้วยการ +(บวก) กันทั้งหมดบนพิกัด i,j ก่อนแล้วค่อยนำมาคำนวนตัว bayesian

for row in range(position_of_start[1], position_of_end[1]):       # y axis
    for coloumn in range(position_of_start[0], position_of_end[0]):       # x axis
        if (calculate_mean_of_postion(row,coloumn,Red,Green,Blue) == 0):
            prob_scoreR_given_classleaf += cal_prob_of_score_and_class(original_Red, row, coloumn, StoreROIleaf.mean_value_R, StoreROIleaf.std_value_R)
            prob_scoreG_given_classleaf += cal_prob_of_score_and_class(original_Green, row, coloumn, StoreROIleaf.mean_value_G, StoreROIleaf.std_value_G) 
            prob_scoreB_given_classleaf += cal_prob_of_score_and_class(original_Blue, row, coloumn, StoreROIleaf.mean_value_B, StoreROIleaf.std_value_B)
        else :
            prob_scoreR_given_not_classleaf += cal_prob_of_score_and_class(original_Red, row, coloumn, StoreNotROIleaf.mean_value_R, StoreNotROIleaf.std_value_R)
            prob_scoreG_given_not_classleaf += cal_prob_of_score_and_class(original_Green, row, coloumn, StoreNotROIleaf.mean_value_G, StoreNotROIleaf.std_value_G)
            prob_scoreB_given_not_classleaf += cal_prob_of_score_and_class(original_Green, row, coloumn, StoreNotROIleaf.mean_value_B, StoreNotROIleaf.std_value_B)
 
#print(prob_scoreR_given_classleaf)
#print(prob_scoreG_given_classleaf)
#print(prob_scoreB_given_classleaf)
       
Bayes_prob_classleaf_given_scoreR = cal_prob_roi(StoreROIleaf.get_num_of_pixels(), StoreNotROIleaf.get_num_of_pixels(), prob_scoreR_given_classleaf, prob_scoreR_given_not_classleaf)
Bayes_prob_classleaf_given_scoreG = cal_prob_roi(StoreROIleaf.get_num_of_pixels(), StoreNotROIleaf.get_num_of_pixels(), prob_scoreG_given_classleaf, prob_scoreG_given_not_classleaf)
Bayes_prob_classleaf_given_scoreB = cal_prob_roi(StoreROIleaf.get_num_of_pixels(), StoreNotROIleaf.get_num_of_pixels(), prob_scoreB_given_classleaf, prob_scoreB_given_not_classleaf)
all_bayes_prob_classleaf_given_scoreRGB = (Bayes_prob_classleaf_given_scoreR, Bayes_prob_classleaf_given_scoreG, Bayes_prob_classleaf_given_scoreB)
StoreROIleaf.update_plus_Bayesian(all_bayes_prob_classleaf_given_scoreRGB)
#print(StoreROIleaf.get_plus_Bayesian_value())

# ในขั้นตอนนี้เราจะทำการคำนวน prob scoreRGB given class leaf ด้วยการ x(คูณ) กันทั้งหมดบนพิกัด i,j ก่อนแล้วค่อยนำมาคำนวนตัว bayesian (เนื่องจากพอนำค่ามาคูณกันจะทำให้ค่าเข้าใกล้ 0 จนไม่สามารถคำนวน bayesian ได้เลย)

# # reset value
# prob_scoreR_given_classleaf = 0.0
# prob_scoreG_given_classleaf = 0.0 
# prob_scoreB_given_classleaf = 0.0 
# prob_scoreR_given_not_classleaf = 0.0
# prob_scoreG_given_not_classleaf = 0.0 
# prob_scoreB_given_not_classleaf = 0.0

# for row in range(position_of_start[1], position_of_end[1]):       # y axis
#     for coloumn in range(position_of_start[0], position_of_end[0]):       # x axis
#         if (calculate_mean_of_postion(row,coloumn,Red,Green,Blue) == 0):
#             prob_scoreR_given_classleaf *= cal_prob_of_score_and_class(original_Red, row, coloumn, StoreROIleaf.mean_value_R, StoreROIleaf.std_value_R)
#             prob_scoreG_given_classleaf *= cal_prob_of_score_and_class(original_Green, row, coloumn, StoreROIleaf.mean_value_G, StoreROIleaf.std_value_G) 
#             prob_scoreB_given_classleaf *= cal_prob_of_score_and_class(original_Blue, row, coloumn, StoreROIleaf.mean_value_B, StoreROIleaf.std_value_B)
#         else :
#             prob_scoreR_given_not_classleaf *= cal_prob_of_score_and_class(original_Red, row, coloumn, StoreNotROIleaf.mean_value_R, StoreNotROIleaf.std_value_R)
#             prob_scoreG_given_not_classleaf *= cal_prob_of_score_and_class(original_Green, row, coloumn, StoreNotROIleaf.mean_value_G, StoreNotROIleaf.std_value_G)
#             prob_scoreB_given_not_classleaf *= cal_prob_of_score_and_class(original_Green, row, coloumn, StoreNotROIleaf.mean_value_B, StoreNotROIleaf.std_value_B)
   
# Bayes_prob_classleaf_given_scoreR = cal_prob_roi(StoreROIleaf.get_num_of_pixels(), StoreNotROIleaf.get_num_of_pixels(), prob_scoreR_given_classleaf, prob_scoreR_given_not_classleaf)
# Bayes_prob_classleaf_given_scoreG = cal_prob_roi(StoreROIleaf.get_num_of_pixels(), StoreNotROIleaf.get_num_of_pixels(), prob_scoreG_given_classleaf, prob_scoreG_given_not_classleaf)
# Bayes_prob_classleaf_given_scoreB = cal_prob_roi(StoreROIleaf.get_num_of_pixels(), StoreNotROIleaf.get_num_of_pixels(), prob_scoreB_given_classleaf, prob_scoreB_given_not_classleaf)
# all_bayes_prob_classleaf_given_scoreRGB = (Bayes_prob_classleaf_given_scoreR, Bayes_prob_classleaf_given_scoreG, Bayes_prob_classleaf_given_scoreB)
# StoreROIleaf.update_times_Bayesian(all_bayes_prob_classleaf_given_scoreRGB)
# print(StoreROIleaf.get_times_Bayesian_value())

print(StoreROIleaf.get_num_of_pixels())
print(StoreROIleaf.get_mean_value())
print(StoreROIleaf.get_std_value())
print(StoreROIleaf.get_plus_Bayesian_value())
print(StoreNotROIleaf.get_num_of_pixels())