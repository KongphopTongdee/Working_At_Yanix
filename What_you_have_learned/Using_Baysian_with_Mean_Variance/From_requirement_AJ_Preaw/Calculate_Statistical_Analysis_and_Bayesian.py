import cv2 
import csv
import collections
import numpy as np
import math

def show_picture(img):
    cv2.imshow("test",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img_test = cv2.imread('Cup_of_coffee.png')
# img_convert_YCRCB = cv2.cvtColor(img_test, cv2.COLOR_BGR2YCR_CB)
# img_convert_YCRCB = cv2.cvtColor(img_test, cv2.COLOR_BGR2RGB)
img_convert_YCRCB = img_test

original_picture = img_convert_YCRCB.copy()

height_grayscale, width_grayscale, channels = img_convert_YCRCB.shape
print("height and width and channels of this picture " + "(" + str(height_grayscale) +","+str(width_grayscale)+","+str(channels) + ")")

#split into Y and Cr and Cb
Y,Cr,Cb = cv2.split(img_convert_YCRCB)

# Variable
# Keep the 10 statistical analysis
store_swatch = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
count_idx_store_swatch = 0

# list of split data
color_channels = [Y,Cr,Cb]

# for creating the area of rectangle
seed_positon = (0,0)
color_of_seed = 0
calculate_seed_bottom_left = (0,0)
calculate_seed_top_right = (0,0)
kernel_input = 0

# for calculate mean
color_of_pixels = 0
number_of_pixels = 0
mean_pixel = 0

# for calculate variance
variance_pixel = 0
power_pixel = 0

# for calculate standard deviation
std_pixel = 0
standard_pixel = 0

# rectangle param
color_of_rectangle = (0,0,255)
thickness = 1

# Step calculate 
# 1.calculate each Y,Cr and Cb mean
# 2.Calculate all Y,Cr and Cb mean
# 3.Do it same with variance and mean


def calculate_mean_variance(event,x,y,flags,param):
    global count_idx_store_swatch, standard_pixel, power_pixel, std_pixel, variance_pixel , mean_pixel, color_of_pixels, number_of_pixels, kernel_input, calculate_seed_bottom_left, calculate_seed_top_right, seed_positon
    
    if (event == cv2.EVENT_LBUTTONDOWN):
        seed_positon = (x,y)
        calculate_seed_bottom_left = (x-kernel_input,y-kernel_input)
        calculate_seed_top_right = (x+kernel_input,y+kernel_input)
        print("seed_position " +"("+ str(x) +","+ str(y)+")")
        print("position_bottom_right " +"("+ str(calculate_seed_top_right[0]) +","+ str(calculate_seed_top_right[1])+")")
        print("position_top_left " +"("+ str(calculate_seed_bottom_left[0]) +","+ str(calculate_seed_bottom_left[1])+")")

    elif (event == cv2.EVENT_RBUTTONDOWN):
        cv2.rectangle(img_convert_YCRCB, calculate_seed_bottom_left, calculate_seed_top_right, color_of_rectangle, thickness)
        # Calculate Mean each Y,Cr and Cb
        for each_channels in color_channels:
            for height_of_picture in range(calculate_seed_bottom_left[1]+1,calculate_seed_top_right[1]):
                for width_of_picture in range(calculate_seed_bottom_left[0]+1,calculate_seed_top_right[0]):
                    color_of_pixels += each_channels[height_of_picture][width_of_picture]
                    power_pixel += pow((each_channels[height_of_picture][width_of_picture] - mean_pixel),2)
                    # standard_pixel += (each_channels[height_of_picture][width_of_picture] - mean_pixel)
                    number_of_pixels += 1
        mean_pixel = (color_of_pixels/number_of_pixels)
        variance_pixel = (power_pixel/number_of_pixels)
        std_pixel = math.sqrt((variance_pixel))
        
        # ยังติดปัญหาที่ว่าวนมาอีกรอบแล้วค่ายัง append ไปข้างหลัง
        print('Mean,Variance,Standard deviation')
        print(mean_pixel,variance_pixel,std_pixel)
        store_swatch[count_idx_store_swatch][0] = mean_pixel
        store_swatch[count_idx_store_swatch][1] = variance_pixel
        store_swatch[count_idx_store_swatch][2] = std_pixel
        count_idx_store_swatch += 1
        count_idx_store_swatch = count_idx_store_swatch % 10
        
        # after_save_need_to_reset
        color_of_pixels = 0
        power_pixel = 0
        # standard_pixel = 0
        number_of_pixels = 0
    
        print('save finish idx : ',count_idx_store_swatch)
        print(store_swatch)


# Run code 

cv2.namedWindow("Calculate_Statistical_Analysis")
cv2.setMouseCallback("Calculate_Statistical_Analysis", calculate_mean_variance)

input_of_enter_kernel = input("Pls enter the kernel expand : ")
print("Kernel expand : " + input_of_enter_kernel)
kernel_input = int(input_of_enter_kernel)

while(1):
    cv2.imshow("Calculate_Statistical_Analysis", img_convert_YCRCB)
    k = cv2.waitKey(1) & 0xFF
    
    if(k == ord('i')):
        input_of_enter_kernel = input("Pls enter the kernel expand : ")
        print("Kernel expand : " + input_of_enter_kernel)
        kernel_input = int(input_of_enter_kernel)
        
    elif (k == ord('x')):
        img_convert_YCRCB = original_picture
    
    elif(k == 27):
        break

cv2.destroyAllWindows()










