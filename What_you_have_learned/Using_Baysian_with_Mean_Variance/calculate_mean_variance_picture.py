# From website (write csv file) : https://www.pythontutorial.net/python-basics/python-write-csv-file/

import cv2 
import csv

# picture_for_calculate_mean_variance_color = cv2.imread('Lenna.png')
# height_color, width_color, channels_color = picture_for_calculate_mean_variance_color.shape

picture_for_calculate_mean_variance_grayscale = cv2.imread('Lenna.png', 0)

original_picture_for_calculate_mean_variance_grayscale = picture_for_calculate_mean_variance_grayscale.copy()

height_grayscale, width_grayscale = picture_for_calculate_mean_variance_grayscale.shape
print("height and width of this picture " + "(" + str(height_grayscale) +","+str(width_grayscale) + ")")

# for creating the area of rectangle
seed_positon = (0,0)
color_of_seed = 0
calculate_seed_bottom_left = (0,0)
calculate_seed_top_right = (0,0)
kernel_input = 0

# value calculate
mean_pixel = 0
color_of_pixels = 0
number_of_pixels = 0

variance_pixel = 0
sqrt_pixel = 0

# list to csv file
storing_color_value_list_row = []
storing_color_value_list_all = []


# rectangle param
color_of_rectangle = (0,0,255)
thickness = 1
# thickness = 2

# mode selection
mode_selection = 0

def calculate_mean_variance(event,x,y,flags,param):
    global seed_positon, color_of_seed, calculate_seed_bottom_left, calculate_seed_top_right, kernel_input, color_of_rectangle, thickness, mean_pixel, number_of_pixels, color_of_pixels, variance_pixel,sqrt_pixel, storing_color_value_list_row, storing_color_value_list_all
    
    if (event == cv2.EVENT_LBUTTONDOWN):
        seed_positon = (x,y)
        calculate_seed_bottom_left = (x-kernel_input,y-kernel_input)
        calculate_seed_top_right = (x+kernel_input,y+kernel_input)
        print("seed_position " +"("+ str(x) +","+ str(y)+")")
        print("position_bottom_right " +"("+ str(calculate_seed_top_right[0]) +","+ str(calculate_seed_top_right[1])+")")
        print("position_top_left " +"("+ str(calculate_seed_bottom_left[0]) +","+ str(calculate_seed_bottom_left[1])+")")

    elif (event == cv2.EVENT_RBUTTONDOWN):
        cv2.rectangle(picture_for_calculate_mean_variance_grayscale, calculate_seed_bottom_left, calculate_seed_top_right, color_of_rectangle, thickness)
        if (mode_selection == 0):
            for height_of_picture in range(calculate_seed_bottom_left[1],calculate_seed_top_right[1]):
                for width_of_picture in range(calculate_seed_bottom_left[0],calculate_seed_top_right[0]):
                    color_of_pixels += picture_for_calculate_mean_variance_grayscale[height_of_picture][width_of_picture]
                    number_of_pixels += 1
            # print(color_of_pixels)
            # print(number_of_pixels)
            mean_pixel = (color_of_pixels/number_of_pixels)
            print("Mean : " + str(mean_pixel))
            color_of_pixels = 0
            number_of_pixels = 0
            
        elif (mode_selection == 1) :
            for height_of_picture in range(calculate_seed_bottom_left[1],calculate_seed_top_right[1]):
                for width_of_picture in range(calculate_seed_bottom_left[0],calculate_seed_top_right[0]):
                    number_of_pixels += 1
                    sqrt_pixel += pow((picture_for_calculate_mean_variance_grayscale[height_of_picture][width_of_picture] - mean_pixel),2)
            # print(sqrt_pixel)
            # print(number_of_pixels)
            variance_pixel = (sqrt_pixel/number_of_pixels)
            print("Variance : " + str(variance_pixel))
            sqrt_pixel = 0
            number_of_pixels = 0
            
        elif (mode_selection == 2):           
            with open('color_value_rectangle_area.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)

                for height_of_picture in range(calculate_seed_bottom_left[1]+1,calculate_seed_top_right[1]):
                    for width_of_picture in range(calculate_seed_bottom_left[0]+1,calculate_seed_top_right[0]):
                        storing_color_value_list_row.append(picture_for_calculate_mean_variance_grayscale[height_of_picture][width_of_picture])
                    # print(storing_color_value_list_row)
                    storing_color_value_list_all.append(storing_color_value_list_row)
                    storing_color_value_list_row = []
                # print(storing_color_value_list_all)   
                # write the data of color value
                writer.writerows(storing_color_value_list_all)  
                storing_color_value_list_all = []         
                
                # write the data of mean and variance of color value
                mean_info = ["Mean : " + str(mean_pixel)]
                variance_info = ["Variance : " + str(variance_pixel)]
                writer.writerow(mean_info) 
                writer.writerow(variance_info) 
                
            print("Finish save data")

# Run code 

cv2.namedWindow("Test_calculate_mean_variance_picture_with_Lenna")
cv2.setMouseCallback("Test_calculate_mean_variance_picture_with_Lenna", calculate_mean_variance)


input_of_enter_kernel = input("Pls enter the kernel expand : ")
print("Kernel expand : " + input_of_enter_kernel)
kernel_input = int(input_of_enter_kernel)

while(1):
    cv2.imshow("Test_calculate_mean_variance_picture_with_Lenna", picture_for_calculate_mean_variance_grayscale)
    k = cv2.waitKey(1) & 0xFF
    
    if(k == ord('i')):
        input_of_enter_kernel = input("Pls enter the kernel expand : ")
        print("Kernel expand : " + input_of_enter_kernel)
        kernel_input = int(input_of_enter_kernel)
        
    elif (k == ord('x')):
        picture_for_calculate_mean_variance_grayscale = original_picture_for_calculate_mean_variance_grayscale
        
    elif (k == ord('m')):
        mode_selection += 1
        mode_selection = mode_selection % 3
        if (mode_selection == 0):
            print("Calculate mean")   
        elif (mode_selection == 1):
            print("Calculate variance")
        elif (mode_selection == 2):
            print("Save data to csv file")
    
    elif(k == 27):
        break

cv2.destroyAllWindows()