import csv
import numpy as np
import cv2
import collections
import matplotlib.pyplot as plt
import math

# test = True

# def change_boolen():
#     global test
#     test = not test
    
# print(test)
# change_boolen()
# print(test)
# change_boolen()
# print(test)

# test = 0
# key_from_key_board_input = ""

# def change_boolen():
#     global test, key_from_key_board_input
#     if (key_from_key_board_input == 'm'):
#         test += 1
#         test = test % 3
#         if (test == 0):
#             print("Calculate mean")   
#         elif (test == 1):
#             print("Calculate variance")
#         elif (test == 2):
#             print("Save data to csv file")
#         print(test)
#     else:
#         print(False)
    
# print(test)
# change_boolen()
# print(test)
# change_boolen()
# print(test)
# change_boolen()
# print(test)

# def input_the_key_value():
#     global key_from_key_board_input
#     input_key = input()
#     key_from_key_board_input = str(input_key)
#     change_boolen()


# for i in range(10):
#     input_the_key_value()
    
    

# input_of_enter_kernel = input("Pls enter the kernel expand : ")
# print("Kernel expand : " + input_of_enter_kernel)
# kernel_input = int(input_of_enter_kernel)

# for i in range(15):
#     test = i % 3
#     print(test)














# import csv

# header = ['name', 'area', 'country_code2', 'country_code3']
# data = [
#     ['Albania', 28748, 'AL', 'ALB'],
#     ['Algeria', 2381741, 'DZ', 'DZA'],
#     ['American Samoa', 199, 'AS', 'ASM'],
#     ['Andorra', 468, 'AD', 'AND'],
#     ['Angola', 1246700, 'AO', 'AGO']
# ]

# 'w' คือการ write ข้อมูลใหม่ลงไป 

# with open('countries.csv', 'w', encoding='UTF8', newline='') as f:
#     writer = csv.writer(f)

#     # write the header
#     writer.writerow(header)

#     # write multiple rows
#     writer.writerows(data)


# import csv

# # 'r' คือการ read ข้อมูล  

# with open("countries.csv", 'r') as file:
#   csvreader = csv.reader(file)
# #   for row in csvreader:
# #     print(row)
# print(csvreader)

# import pandas as pd
# data = pd.read_csv("countries.csv")
# print(data)





# picture_for_using_bayesian = []

# with open("color_value_rectangle_area.csv", 'r') as file:
#     csvreader = csv.reader(file)
#     for row in csvreader:
#         picture_for_using_bayesian.append(row)
      
# picture_for_using_bayesian.pop(len(picture_for_using_bayesian)-1)
# picture_for_using_bayesian.pop(len(picture_for_using_bayesian)-1)
  
  
  
  
  
  
  
  
# Test

# img = cv2.imread('Lenna.png',0)

# print(img)
# print(type(img))

# cv2.imshow('sample image',img)

# cv2.waitKey(0) # waits until a key is pressed
# cv2.destroyAllWindows() # destroys the window showing image

# print(picture_for_using_bayesian)
# print(type(picture_for_using_bayesian))



# test = np.array(picture_for_using_bayesian)



# print(test)

# for i in test:
#     print(i)
#     i = list(map(int, i))
#     print(i)
#     i = np.array(i)
#     print(i)

# print(test)





# # Attempt to display using cv2 (doesn't work)
# cv2.namedWindow("Picture_of_using_baysian")
# cv2.imshow("Picture_of_using_baysian", picture_for_using_bayesian)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

























# import csv  

# header = ['name', 'area', 'country_code2', 'country_code3']
# data = ['Afghanistan', 652090, 'AF', 'AFG']

# with open('countries.csv', 'w', encoding='UTF8') as f:
#     writer = csv.writer(f)

#     # write the header
#     writer.writerow(header)

#     # write the data
#     writer.writerow(data)

# import csv

# header = ['name', 'area', 'country_code2', 'country_code3']
# data = ['Afghanistan', 652090, 'AF', 'AFG']


# with open('countries.csv', 'w', encoding='UTF8', newline='') as f:
#     writer = csv.writer(f)

#     # write the header
#     writer.writerow(header)

#     # write the data
#     writer.writerow(data)



# # Example 1: Use numpy.append() function
# arr = np.array([[0,2,4],[6,8,10]]) 
# app_arr = np.append(arr, [13,15,17])
# print(app_arr)
# print(type(app_arr)) 

# Example 2: Appending array with axis=0
# arr = np.array([[0,2,4],[6,8,10]]) 
# app_arr=np.append(arr, [[5,7,9],[13,15,17]],axis = 0)
# print(app_arr)
# print(type(app_arr))

# # Example 3: Use Append elements along axis 1
# arr = np.array([[0,2,4],[6,8,10]]) 
# app_arr=np.append(arr, [[5,7,9],[13,15,17]],axis = 1) 
# print(app_arr)
# print(type(app_arr))

# # Example 4: Use appending array
# arr = np.arange(7)  
# arr1 = np.arange(9, 14)
# arr2 = np.append(arr, arr1)
# print("Appended arr2 : ", arr2)

# test = [0,1,2,3,4,5,6,0,1,0,1,2,5,3,1]
# new_tuple = []
# print(test)
# print(type(test))

# test = sorted(test)
# test = tuple(test)
# print(test)

# for i in test:
#     if i in new_tuple:
#         pass
#     else :
#         new_tuple.append((i,1))
        
# print(new_tuple)

# test = (0,1,2,3,4,5,6,0,1,0,1,2,5,3,1)
# test = [0,1,2,3,4,5,6,0,1,0,1,2,5,3,2,2,2,2]

# words = [word for word in test]
# print(words)
# word_count = list()

# #use set and len to get the number of unique words
# word_count.extend(collections.Counter(words).most_common(len(set(words))))
# #print out 10 most frequent words
# print(word_count)

# def find_max_index(lst):
#     """
#     Returns the index of the maximum value in a given list.
#     """
#     max_value = max(lst)
#     max_index = lst.index(max_value)
#     return max_index

# value_check = []
# for num,value in word_count:
#     value_check.append(value)

# print(value_check)

# max_index = find_max_index(value_check)
# print(max_index)

# print(word_count[max_index][0])

# my_list = [1, 3, 2, 5, 4]
# max_index = find_max_index(my_list)
# print(max_index)   # Output: 3



# # Generate some random data
# data = np.random.normal(size=1000)
# print(data)
# print(type(data))

# # Create a histogram of the data
# plt.hist(data, bins=30)

# # Add a title and axis labels
# plt.title('Histogram of Random Data')
# plt.xlabel('Value')
# plt.ylabel('Frequency')

# # Show the plot
# plt.show()

# Generate some random data
# data = np.random.normal(size=1000)

# # Calculate the probability density function
# density, bins = np.histogram(data, density=True)
# density /= density.sum()

# # Calculate the cumulative distribution function
# cumulative = np.cumsum(density)

# # Create a line plot of the cumulative distribution
# plt.plot(bins[:-1], cumulative)

# # Add labels and title
# plt.xlabel('Value')
# plt.ylabel('Cumulative Probability')
# plt.title('Cumulative Distribution of Random Data')

# # Show the plot
# plt.show()
   

# year = [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
# unemployment_rate = [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]
  
# plt.plot(year, unemployment_rate, color='red', marker='o')
# plt.title('unemployment rate vs year', fontsize=14)
# plt.xlabel('year', fontsize=14)
# plt.ylabel('unemployment rate', fontsize=14)
# plt.grid(True)
# plt.show()

# test = [0,1,1,12,2,15,5,6,10,8,44,8,82]

# test = sorted(test)
# print(test)

# idx_list = []
# value_list = []

# for i in range(1,len(test)):
#     if test[i-1] != test[i]:
#         value_list.append(test[i])
#     else :
#         pass

# test = (0,1,2,3,4,5,6,0,1,0,1,2,5,3,1)
# test = [0,1,2,3,4,5,6,0,1,0,1,2,5,3,2,2,2,2]

# words = [word for word in test]
# print(words)
# word_count = list()

# #use set and len to get the number of unique words
# word_count.extend(collections.Counter(words).most_common(len(set(words))))
# #print out 10 most frequent words
# print(word_count)
# print(len(word_count))

# word_count = sorted(word_count)
# print(word_count)


# Generate some random data
test = [0,1,2,3,4,5,6,0,1,0,1,2,5,3,2,2,2,2]
# data = np.random.normal(size=1000)
# print(data)
# print(type(data))

# Create a histogram of the data
# plt.hist(data, bins=30)
# test = sorted(test)
# print(test) 
# print(type(test))
plt.hist(test, bins=30)     # auto sorted by self function

# Add a title and axis labels
plt.title('Histogram of Random Data')
plt.xlabel('Value')
plt.ylabel('Frequency')

# Show the plot
plt.show()


