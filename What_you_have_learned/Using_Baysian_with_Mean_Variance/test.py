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