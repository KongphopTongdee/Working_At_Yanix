import cv2 

image = cv2.imread("Lenna.png")

original_image = image.copy()

print(image[50][50])


# x = input("Pls insert the kernel expand : ")
# print("kernel expand : " + x)
# print(type(x))
# y = int(x)
# print(type(y))

# cv2.imshow("test",image)
# cv2.waitKey()
# cv2.destroyAllWindows()

# cv2.imshow("test",original_image)
# cv2.waitKey()
# cv2.destroyAllWindows()