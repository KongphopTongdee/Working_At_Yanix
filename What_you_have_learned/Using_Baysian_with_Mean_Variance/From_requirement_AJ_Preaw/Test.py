import cv2 
import numpy as np
import math
import matplotlib.pyplot as plt

def show_img_matplotlib(img):
    #use only matplotlib to plot the scale 
    plt.imshow(img)
    plt.show()

# class Person:
#   def __init__(self, name, age):
#     self.name = name
#     self.age = age

#   def myfunc(self):
#     print("Hello my name is " + self.name)

# p1 = Person("John", 36)
# p1.myfunc()

# store_swatch = [[],[],[],[],[],[],[],[],[],[]]

# store_swatch[5].append(10)

# print(store_swatch)

# y = [5,10,15]
# cr = [2,4,6]
# cb = [3,6,9]

# calculate_num = 0

# test_call_out = [y,cr,cb]

# for test in test_call_out:
#     for i in range(len(y)):
#         calculate_num += test[i]
        
# print(calculate_num)

# ans = 45.5646813218
# ans = format(ans, '.4f')

# print(ans)

# test = 111

# for i in range(15):
#     test += 1
#     test = test%10
#     print(test)

# print(math.pi)

# print(math.exp(1))

# print('Hello world')

# calculate_mean_leaf = [128,185,111] 
# calculate_mean_outside_leaf_on_the_left= [168,163,151]
# calculate_mean_outside_leaf_on_the_right = [237,208,184]
# calculate_mean_outside_leaf_on_the_top = [129,119,107]
# calculate_mean_leaf_on_the_bottom = [185,140,114]

# calculate mean leaf(RGB) = 128 185 111 = 141.34
# calculate mean outside leaf on the left(RGB) = 168 163 151 = 160.67
# calculate mean outside leaf on the right(RGB) = 237 208 184 = 209.67
# calculate mean outside leaf on the top(RGB) = 129 119 107 = 118.33
# calculate mean leaf on the bottom(RGB) = 185 140 114 = 146.34


# def calculate_mean(input):
#     Ans = 0.0
#     for i in input:
#         Ans += i
#     Ans = Ans / len(input)
#     return Ans

# print(calculate_mean(calculate_mean_leaf))
# print(calculate_mean(calculate_mean_outside_leaf_on_the_left))
# print(calculate_mean(calculate_mean_outside_leaf_on_the_right))
# print(calculate_mean(calculate_mean_outside_leaf_on_the_top))
# print(calculate_mean(calculate_mean_leaf_on_the_bottom))


# Ans = math.exp(math.pow((50-25),2)/math.pow((9),2))

# print(Ans)

# x1 = np.ones(9).reshape((3, 3))
# x2 = np.arange(9.0).reshape((3, 3))

# print(x1)
# print(x2)

# test = [1,2,3,4,5,6,7,8,9]
# showtest = test.copy()
# test.pop(0)
# print(test)
# print(showtest)

# class Person:
#   def __init__(self, name, age):
#     self.name = name
#     self.age = age

# p1 = Person("John", 36)

# print(p1.name)
# print(p1.age)


# # Illustration of creating a class
# # in Python with input from the user
# class Student:
# 	'A student class'
# 	stuCount = 0

# 	# initialization or constructor method of
# 	def __init__(self):
		
# 		# class Student
# 		self.name = input('enter student name:')
# 		self.rollno = input('enter student rollno:')
# 		Student.stuCount += 1

# 	# displayStudent method of class Student
# 	def displayStudent(self):
# 		print("Name:", self.name, "Rollno:", self.rollno)


# stu1 = Student()
# stu2 = Student()
# stu3 = Student()
# stu1.displayStudent()
# stu2.displayStudent()
# stu3.displayStudent()
# print('total no. of students:', Student.stuCount)

# std_R_leaf = math.sqrt(81/9)

# print(std_R_leaf)

# class Person:
#     def __init__(self):
#         self.name = ""
#         self.age = 0
#     def update_name(self, name):
#         self.name = name
#     def update_age(self, age):
#         self.age = age
#     def get_name(self):
#         return self.name
#     def get_age(self):
#         return self.age


# p1 = Person()

# # same meaning but different code
# print(p1.name)
# print(p1.age)
# print(p1.get_name())
# print(p1.get_age())

# p1.update_name("Kongphop")
# p1.update_age(21)

# print(p1.get_name())
# print(p1.get_age())

# test = cv2.imread("Idea_leaf_white_background.png")
# position_of_seed = (364,278)
# cv2.circle(test, position_of_seed, radius=0, color=(0, 0, 0), thickness=100)
# show_img_matplotlib(test)

store_the_bayesian_pic = np.zeros((5,3))
print(store_the_bayesian_pic)