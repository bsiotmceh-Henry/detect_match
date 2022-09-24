import cv2
import numpy as np

# 576*1280
img = cv2.imread('../image_ad/1.jpg')

# 尺寸大約60px
x_position_list = [
    (60, 60),
    (img.shape[1]- 90, 60),
    (img.shape[1]- 60, 40),
    (img.shape[1]- 60, 80),
]
size_list = [
    60,
    60,
    60,
    60,
]
# position_list = [
#     [(60, 60), (120, 120)],
#     [(img.shape[1]- 90, 60), (img.shape[1], 120)],
#     [(img.shape[1]- 60, 40), (img.shape[1], 100)],
#     [(img.shape[1]- 60, 80), (img.shape[1], 140)],
# ]
position_list = []
for x in x_position_list:
    y = (x[0]+60, x[1]+60)
    position_list.append([x, y])
print(img.size)

# ltop = (300, 0)
# rtbm = (600, 300)
for p in position_list:
    img_cap = img[p[0][1]:p[1][1], p[0][0]: p[1][0]]
    cv2.imshow('Image', img_cap)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# img_cap = img[ltop[1]:rtbm[1], ltop[0]: rtbm[0]]

# cv2.imshow('Image', img_cap)

# cv2.imwrite('meme2.jpg', img_cap)

# cv2.waitKey(0)
# cv2.destroyAllWindows()