import cv2
import numpy as np

picture_for_region_growing = cv2.imread('Lenna.png', 0)

print(picture_for_region_growing)

cv2.imshow('test_image', picture_for_region_growing)
cv2.waitKey(0)
cv2.destroyAllWindows()