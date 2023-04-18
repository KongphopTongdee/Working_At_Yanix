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

# value of pixels for using bayesian
picture_for_using_bayesian = []
mean_of_picture = []
variance_of_picture = []

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
mean_of_picture.append(picture_for_using_bayesian[len(picture_for_using_bayesian)-2])
variance_of_picture.append(picture_for_using_bayesian[len(picture_for_using_bayesian)-1])
picture_for_using_bayesian.pop(len(picture_for_using_bayesian)-1)
picture_for_using_bayesian.pop(len(picture_for_using_bayesian)-1)

# convert and scale the decimal into 4 decimal
mean_of_picture = convert_str_into_float(mean_of_picture)
variance_of_picture = convert_str_into_float(variance_of_picture)
mean_of_picture = format(mean_of_picture, '.4f')
variance_of_picture = format(variance_of_picture, '.4f')

