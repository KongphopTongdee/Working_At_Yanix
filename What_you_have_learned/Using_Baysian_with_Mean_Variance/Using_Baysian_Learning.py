# From Website : https://medium.com/@dopplerz/bayesian-neural-network-%E0%B8%95%E0%B8%AD%E0%B8%99%E0%B8%97%E0%B8%B5%E0%B9%88-4-model-%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B9%80%E0%B8%A3%E0%B8%B5%E0%B8%A2%E0%B8%99%E0%B8%A3%E0%B8%B9%E0%B9%89%E0%B8%94%E0%B9%89%E0%B8%A7%E0%B8%A2-probabilistic-distribution-f7024b8dab2

import cv2
import csv

picture_for_using_bayesian = []

with open("color_value_rectangle_area.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        picture_for_using_bayesian.append(row)

