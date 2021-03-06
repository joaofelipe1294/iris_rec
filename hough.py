from base_loader import BaseLoader
from utils.segmentation import Segmentation
import cv2
import numpy as np
import math	
import PIL


def threshold(image , val=255):
	height , width = image.shape
	for line in range(0 , height):
		for column in range(0 , width):
			if image.item(line , column) != val:
				image.itemset((line , column), 0)
			else:
				image.itemset((line , column) , 255)
	#cv2.imshow('mask' , image)
	#cv2.waitKey(0)




base = BaseLoader('CASIA-Iris-Lamp-100')
subject = base.subjects[0]
image_path = subject.left_image_paths[1]
segmentation = Segmentation(image_path=image_path)
segmentation.houghs_transform(min_ray = 47 , max_ray = 47)
pre_processed_image = segmentation.pre_processed_image
equalized_image = cv2.equalizeHist(pre_processed_image)
centroid = segmentation.pupil_centroid
pupil_ray = segmentation.pupil_ray
print(centroid)
#print(centroid)
#print(ray)
line_init = centroid[0] - pupil_ray
line_end = centroid[0] + pupil_ray
column_init = centroid[1] - pupil_ray
column_end = centroid[1] + pupil_ray
cut_image = equalized_image[line_init:line_end , column_init:column_end ]
#print(cut_image)
cut_image = np.array(cut_image , np.uint8)
#cv2.imshow('sub_image' , cut_image)
#cv2.waitKey(0)
sum_values = []
for increment_size in range(0,80):
	new_line_init = line_init - increment_size
	new_line_end = line_end + increment_size
	new_column_init = column_init - increment_size
	new_column_end = column_end + increment_size
	cut_image = equalized_image[new_line_init:new_line_end , new_column_init:new_column_end]
	cut_image = np.array(cut_image , np.uint8)
	copy_image = cut_image.copy()
	height , width = copy_image.shape
	#print(centroid)
	cv2.circle(copy_image , tuple([height / 2 , width / 2]) , pupil_ray + increment_size , 255 , -1)
	#print('line : ' + str(new_line_init) + ' - ' + str(new_line_end) + ' | column : ' + str(new_column_init) + ' - ' + str(new_column_end) + ' | count : ' + str(increment_size))
	threshold(copy_image)
	#cv2.imshow('mask_init' , copy_image)
	#cv2.imshow('sub_image' , cut_image)
	masked_image = cut_image & copy_image
	sum_values.append(np.sum(masked_image))
	#cv2.imshow('comparing' , masked_image)
	#cv2.waitKey(200)


diferences = []
for index in range(1 , len(sum_values)):
	diferences.append(sum_values[index] - sum_values[index - 1])

print(diferences)

bigger_diference = 0
index_diference = 0
for index in range(0 , len(diferences)):
	if diferences[index] >= bigger_diference:
		bigger_diference = diferences[index]
		index_diference = index

lower_diference = 0
index = 0


print('bigger diference : ' + str(bigger_diference) + ' | index : ' + str(index_diference))


rgb_image = cv2.imread(image_path)
cv2.circle(rgb_image , tuple([centroid[1] , centroid[0]]) , index_diference + pupil_ray, (0,0,255))
cv2.imshow('result' , rgb_image)
cv2.waitKey(0)