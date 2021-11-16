#this is first step.Classify images by width and height

import os
from tqdm import tqdm
from PIL import Image
import numpy as np
import random
from collections import Counter
from os import listdir
from PIL import Image
import cv2
import matplotlib.pyplot as plt

images_path = 'G:/xiao/dataset_molcreateV2/data/'
preimage_path = 'G:/xiao/dataset_molcreateV2/data/pre_image/'

def resize_image(image, length):
    w, h = image.size

    if h >= w:
        width = length * w / h
        height = length
    else:
        height = length * h / w
        width = length
    width = int(width)
    height = int(height)

    image = image.resize((width, height), Image.ANTIALIAS)
    return image

def getFiles(path):
    Filelist = []
    for home, dirs, files in os.walk(path):
        for file in files:
            # 文件名列表，包含完整路径
            Filelist.append(os.path.join(home, file))
            #Filelist.append(file)
    return Filelist

images_all = getFiles(images_path)
print('图像的总数量:', len(images_all))

w_list = []
h_list = []
for img in tqdm(images_all):
    name = os.path.split(img)[1]
    image = Image.open(img).convert('RGB')
    w, h = image.size
    image_np = np.array(image)
    image_np = Image.fromarray(image_np.astype('uint8')).convert('RGB')
    h_list.append(h)
    w_list.append(w)

# print(len(Counter(w_list)), Counter(w_list))
# print(len(Counter(h_list)), Counter(h_list))

    # N = random.randint(0, 59)
    #
    # image_np = np.where(image_np <= 150, 1, 255)
    #image_np = Image.fromarray(image_np.astype('uint8')).convert('RGB')
    # plt.imshow(image_np)
    # plt.show()

    if not os.path.exists(preimage_path + '/w/'):
        os.makedirs(preimage_path + '/w/')
    if not os.path.exists(preimage_path + '/h/'):
        os.makedirs(preimage_path + '/h/')

    if not os.path.exists(preimage_path + '/w/' + str(w) + '/'):
        os.makedirs(preimage_path + '/w/' + str(w) + '/')
    if not os.path.exists(preimage_path + '/h/' + str(h) + '/'):
        os.makedirs(preimage_path + '/h/' + str(h) + '/')

    image_np.save(preimage_path + '/h/' + str(h) + '/' + name)
    image_np.save(preimage_path + '/w/' + str(w) + '/' + name)




