# From Website : https://medium.com/@dopplerz/bayesian-neural-network-%E0%B8%95%E0%B8%AD%E0%B8%99%E0%B8%97%E0%B8%B5%E0%B9%88-4-model-%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B9%80%E0%B8%A3%E0%B8%B5%E0%B8%A2%E0%B8%99%E0%B8%A3%E0%B8%B9%E0%B9%89%E0%B8%94%E0%B9%89%E0%B8%A7%E0%B8%A2-probabilistic-distribution-f7024b8dab2

import cv2
import csv
import numpy as np

def convert_str_into_float(input_list):
    Ans = []
    number_check = ['0','1','2','3','4','5','6','7','8','9','.']
    
    checking_num = input_list[0]
    for checking in checking_num[0]:
        if (checking in number_check):
            Ans.append(checking)       
    Ans = ''.join(Ans)  
    Ans = float(Ans)
    
    return Ans

def convert_list_into_numpy_array(input_list_to_numpyarray):
    Ans = []
    
    input_list_to_numpyarray = list(map(int, input_list_to_numpyarray))
    input_list_to_numpyarray = np.array(input_list_to_numpyarray)
    Ans = input_list_to_numpyarray
    
    return Ans

# value of pixels for using bayesian
picture_for_using_bayesian = []
mean_of_picture = []
variance_of_picture = []
mode_of_picture = []
media_of_picture = []
std_of_picture = []

# store value for changing into numpy array
list_after_change_into_numpy_array = np.array([])

# calculate probability
probability_more_than_means = 0.0
probability_less_than_means = 0.0
n_all_pixels = 0

# preparing data
with open("color_value_rectangle_area.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        picture_for_using_bayesian.append(row)
        
# store the mean and variance and pixel of picture
mean_of_picture.append(picture_for_using_bayesian[len(picture_for_using_bayesian)-5])
media_of_picture.append(picture_for_using_bayesian[len(picture_for_using_bayesian)-4])
mode_of_picture.append(picture_for_using_bayesian[len(picture_for_using_bayesian)-3])
variance_of_picture.append(picture_for_using_bayesian[len(picture_for_using_bayesian)-2])
std_of_picture.append(picture_for_using_bayesian[len(picture_for_using_bayesian)-1])
picture_for_using_bayesian.pop(len(picture_for_using_bayesian)-1)
picture_for_using_bayesian.pop(len(picture_for_using_bayesian)-1)
picture_for_using_bayesian.pop(len(picture_for_using_bayesian)-1)
picture_for_using_bayesian.pop(len(picture_for_using_bayesian)-1)
picture_for_using_bayesian.pop(len(picture_for_using_bayesian)-1)

# convert and scale the decimal into 4 decimal
mean_of_picture = convert_str_into_float(mean_of_picture)
media_of_picture = convert_str_into_float(media_of_picture)
mode_of_picture = convert_str_into_float(mode_of_picture)
variance_of_picture = convert_str_into_float(variance_of_picture)
std_of_picture = convert_str_into_float(std_of_picture)
mean_of_picture = format(mean_of_picture, '.4f')
variance_of_picture = format(variance_of_picture, '.4f')
std_of_picture = format(std_of_picture, '.4f')


# print(mean_of_picture)
# print(media_of_picture)
# print(mode_of_picture)
# print(variance_of_picture)
# print(std_of_picture)


# convert the outside list into numpy array
picture_for_using_bayesian = np.array(picture_for_using_bayesian)

# convert list_string into numpy array                                  (not finish next step is input into array)
for list_numpyarray in picture_for_using_bayesian:
    list_numpyarray = convert_list_into_numpy_array(list_numpyarray)
    # print(list_numpyarray)
    list_after_change_into_numpy_array = np.append(list_after_change_into_numpy_array , list_numpyarray,axis = 0)       
    

# print(list_after_change_into_numpy_array)
# print(type(list_after_change_into_numpy_array))

# print(picture_for_using_bayesian)
