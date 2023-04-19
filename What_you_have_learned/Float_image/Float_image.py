import cv2

picture_for_float_image = cv2.imread('Lenna.png')

# print(picture_for_float_image)

blue,green,red = cv2.split(picture_for_float_image)

new_Blue = blue/255
new_Green = green/255
new_Red = red/255

# print(ne_Blue)
# print(new_Green)
# print(new_Red)

picture_for_new_float_image = cv2.merge((new_Blue, new_Green, new_Red))

print(picture_for_new_float_image)

cv2.imshow("Picture for float image",picture_for_float_image)
cv2.waitKey(0)
cv2.destroyAllWindows()