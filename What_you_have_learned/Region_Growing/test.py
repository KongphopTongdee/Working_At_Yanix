import cv2
import numpy as np
# test = [[1,2,3],
#         [4,5,6],
#         [7,8,9]]

# for i in range(len(test)):
#     for j in range(len(test)):
#         print(test[i][j])

picture_for_region_growing = cv2.imread('Lenna.png', 0)

# สีที่ได้จะเป็นสีที่อยู่ในช่วงของ 0-255 ที่เป็น 1 channels เท่านั้น
# print(picture_for_region_growing)

height ,width = picture_for_region_growing.shape
new_list_for_image = picture_for_region_growing

cv2.imshow('test_image', new_list_for_image)
cv2.waitKey()
cv2.destroyAllWindows()