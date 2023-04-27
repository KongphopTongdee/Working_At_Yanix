import cv2 
import numpy as np
import math
import matplotlib.pyplot as plt

def show_img_cv2(img):
    cv2.imshow("test",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def show_img_matplotlib(img):
    #use only matplotlib to plot the scale 
    plt.imshow(img)
    plt.show()

def cal_prob_of_score_and_class(current_pixel, mean_of_class, std_of_class):
    # equation 
    # P(S|C) = (1/(standard_deviation*squareroot(2*pi)))(exp((-1/2)((current_pixel-mean)^2/standard_deviation)))
    Ans = 0.0
    
    Ans = (1/(std_of_class*math.sqrt(2*math.pi)))*(math.exp((-1/2)*((math.pow((current_pixel-mean_of_class),2))/std_of_class)))
    
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


# img_Leaf_tilted = cv2.imread("Leaf_tilted.png")
img_Leaf_straight_line = cv2.imread("Leaf_straight_line.png")

height, width, channels = img_Leaf_straight_line.shape
print("height and width of this picture " + "(" + str(height) +","+str(width) +","+str(channels) +")")

img_convert_YCRCB = cv2.cvtColor(img_Leaf_straight_line, cv2.COLOR_BGR2YCR_CB)
img_convert_RGB = cv2.cvtColor(img_Leaf_straight_line, cv2.COLOR_BGR2RGB)
Y,Cr,Cb = cv2.split(img_convert_YCRCB)

# cv2.rectangle(img_Leaf_straight_line, (445,470), (712,23), (0,0,255), 2)
# show_img(img_Leaf_straight_line)
# cv2.rectangle(img_Leaf_tilted, (445,470), (712,23), (0,0,255), 2)
# show_img(img_Leaf_tilted)

# Step of working
# 1. ทำการหา region growing เพื่อทำการตั้ง threshold ที่เอาเฉพาะค่าใบไม้มาใช้ โดยถ้าเป็นใบไม้จะให้เป็นสีขาวแต่ถ้าเป็นสิ่งที่ไม่สำคัญจะให้เป็นสีดำ
# 2. ทำการหา interestsample,notinterestsample จากการนับเฉพาะสีขาวจาก region growing
# 3. ทำการหา prob_of_score_and_class, prob_of_score_and_notclass โดยการคำนวน equation ที่ผนวกค่า current position, mean, standard deviation
# 4. สุดท้ายนำไปใส่ในสมการ calculate bayesian probability ที่หา class(leaf)|score(mean,std of Y,Cr,Cb)

# step 1. ทำการหา region growing เพื่อทำการตั้ง threshold ที่เอาเฉพาะค่าใบไม้มาใช้ โดยถ้าเป็นใบไม้จะให้เป็นสีขาวแต่ถ้าเป็นสิ่งที่ไม่สำคัญจะให้เป็นสีดำ
# เนื่องจากว่าการ region growing ที่ง่ายที่สุดจะเป็นภาพขาวดำ
region_growing_only = cv2.imread("Leaf_straight_line.png")
region_growing_only_convert_RGB = cv2.cvtColor(region_growing_only, cv2.COLOR_BGR2RGB)
# region_growing_only_convert_YCrCb = cv2.cvtColor(region_growing_only, cv2.COLOR_BGR2YCrCb)
# region_growing_only_convert_YCr_Cb = cv2.cvtColor(region_growing_only, cv2.COLOR_BGR2YCR_CB)
# region_growing_only = cv2.imread("Leaf_straight_line.png")

cv2.rectangle(region_growing_only_convert_RGB, (445,470), (712,23), (0,0,255), 1)
# position that is green is (x,y) = (530,300)
# position outside leaf on the left = 490,280
# position outside leaf on the right = 706,294
# position outside leaf on the top = 582,96
# position outside leaf on the bottom = 620,441

# calculate mean leaf(YCrCb) = 166 105 100 = 123.67
# calculate mean outside leaf on the left(YCrCb) = 167 132 120 = 139.67
# calculate mean outside leaf on the right(YCrCb) = 234 139 114 = 162.34
# calculate mean outside leaf on the top(YCrCb) = 115 134 120 = 123
# calculate mean leaf on the bottom(YCrCb) = 139 155 107 = 133.67

# calculate mean leaf(RGB) = 128 185 111 = 141.34
# calculate mean outside leaf on the left(RGB) = 168 163 151 = 160.67
# calculate mean outside leaf on the right(RGB) = 237 208 184 = 209.67
# calculate mean outside leaf on the top(RGB) = 129 119 107 = 118.33
# calculate mean leaf on the bottom(RGB) = 185 140 114 = 146.34

# ดูจากการที่เราประมาณค่าสังเกตุได้ว่ามีบางค่า mean ที่ใกล้เคียงกันคือ mean leaf กับ mean bottom ทำให้ถ้าเลือกตัดค่า threshold นี้อาจจะมีปัญหาได้เพราะ ฉนั้นจะลองใช้ค่า
# บางตัวจาก R หรือ G หรือ B เพื่อเป็นตัวมาตัด threshold ดั้งนั้นผลสรุปค่าที่ได้เลือกนำมาใช้ คือ ค่า

show_img_matplotlib(region_growing_only_convert_RGB)













# step 2. ทำการหา interestsample,notinterestsample จากการนับเฉพาะสีขาวจาก region growing












# step 3. ทำการหา prob_of_score_and_class, prob_of_score_and_notclass โดยการคำนวน equation ที่ผนวกค่า current position, mean, standard deviation















# step 4. สุดท้ายนำไปใส่ในสมการ calculate bayesian probability ที่หา class(leaf)|score(mean,std of Y,Cr,Cb)





















