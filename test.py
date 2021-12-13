import cv2
import os
import numpy as np
def gen_random_backgroud(w,h):
    one_arr = np.ones((w,h,3),dtype=np.uint8)*255
    return one_arr

def random_gen(min=100,max=300):
    tmp=np.random.randint(min,max)
    return tmp


w=100
h=300
random_w=random_gen()
a=gen_random_backgroud(random_w,300)
cv2.imshow("Image", a)
cv2.waitKey(0)
cv2.destroyAllWindows()


# img = cv2.imread('G:/xiao/dataset_molcreateV2/code/other_elements/negative_sample1/white.png')
#
# img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
# print(type(img), img.shape)
# img_re = cv2.resize(img, (330, 160))
# print(type(img), img_re.shape)
# #img = cv2.resize(img_re, (4344, 5684))
# cv2.imwrite('G:/xiao/dataset_molcreateV2/code/other_elements/negative_sample1/white.png', img_re)
#
#
# def getFiles(path):
#     Filelist = []
#     for home, dirs, files in os.walk(path):
#         for file in files:
#             # 文件名列表，包含完整路径
#             file_path = os.path.join(home, file).replace('\\', '/')
#             Filelist.append(file_path)
#             #Filelist.append(file)
#     return Filelist
#
#
# files = getFiles('G:/xiao/dataset_molcreateV2/code/other_elements/negative_sample1/')
# print(len(files))
# for file in files:
#     img = cv2.imread(file)
#     img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
#     img_re = cv2.resize(img, (330, 160))
#     cv2.imwrite(file, img_re)
