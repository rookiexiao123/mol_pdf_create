# pinjie image with no erode

from os import listdir
from PIL import Image
import os
import math
import random
import matplotlib.pyplot as plt
import numpy as np


# style == 0, height is the same, add the width; style == 1, widht is the same, add the height;
# num: image number per column
# image_num: totol image number
def pinjie(list_path, style, num, image_num, save_path, pixel=60):
    # 获取当前文件夹中所有JPG图像
    im_list = [Image.open(list_path+fn) for fn in listdir(list_path) if fn.endswith('.jpg') or fn.endswith('.png')]
    files_numbers = len(im_list)

    if files_numbers > image_num:
        files_numbers = image_num

    im_list = random.sample(im_list, files_numbers)

    # 高一样，宽相加
    if style == 0:
        # 图片转化为相同的尺寸
        all_width = 0
        width_list = []
        # columns 一行有几个化学式，有几行
        columns = math.ceil(files_numbers / num)

        for i, img in enumerate(im_list):
            # print(img.size)
            # w, h = img.size
            # length = 256
            # if h >= w:
            #     width = int(length * w / h)
            #     height = length
            #
            # else:
            #     height = int(length * h / w)
            #     width = length
            # img = img.resize((width, height), Image.BICUBIC)
            # img = np.where(np.array(img) <= 240, 0, 255)
            # img = Image.fromarray(img.astype('uint8')).convert('RGB')
            # print(img.size)
            # plt.imshow(img)
            # plt.show()
            all_width = all_width + img.size[0]#width, height = ims[0].size
            if (i+1) % num == 0 or i == (len(im_list) - 1):
                width_list.append(all_width)
                all_width = 0

        # 创建空白长图
        result = Image.new(im_list[0].mode, (max(width_list), im_list[0].size[1] * columns), (255, 255, 255))
        # 创建原图
        result_source = Image.new(im_list[0].mode, (max(width_list), im_list[0].size[1] * columns), (255, 255, 255))
        # 拼接图片
        all_length = 0
        for i, im in enumerate(im_list):
            result_source.paste(im, box=(all_length, im_list[0].size[1] * math.floor(i/num)))

            image_np = np.where(np.array(im) <= 150, [p + i for p in pixel], 255)
            im = Image.fromarray(image_np.astype('uint8')).convert('RGB')
            result.paste(im, box=(all_length, im_list[0].size[1] * math.floor(i/num)))
            all_length = all_length + im.size[0]
            if (i+1) % num == 0:
                all_length = 0
        # plt.imshow(result)
        # plt.show()
        # 保存图片
        result.save('G:/xiao/dataset_molcreateV2/code/' + save_path)
        result_source.save('G:/xiao/dataset_molcreateV2/code/src_image/' + save_path)
    else:
        # 宽一样，高相加
        # 图片转化为相同的尺寸
        all_width = 0
        width_list = []

        for i, img in enumerate(im_list):
            #resize_image(i, 256)#i.resize((1280, 1280), Image.ANTIALIAS)
            all_width = all_width + img.size[1]#width, height = ims[0].size
            if (i+1) % num == 0 or i == (len(im_list) - 1):
                width_list.append(all_width)
                all_width = 0

        # columns 一行有几个化学式，有几行
        columns = num
        # 创建空白长图
        result = Image.new(im_list[0].mode, (im_list[0].size[0] * columns, max(width_list)), (255, 255, 255))
        # 创建原图
        result_source = Image.new(im_list[0].mode, (im_list[0].size[0] * columns, max(width_list)), (255, 255, 255))
        # 拼接图片
        all_length = 0
        for i, im in enumerate(im_list):
            result_source.paste(im, box=(im_list[0].size[0] * math.floor(i / num), all_length))

            image_np = np.where(np.array(im) <= 150, [p + i for p in pixel], 255)
            im = Image.fromarray(image_np.astype('uint8')).convert('RGB')
            result.paste(im, box=(im_list[0].size[0] * math.floor(i/num), all_length))
            all_length = all_length + im.size[1]
            if (i+1) % num == 0:
                all_length = 0

        # 保存图片
        result.save('G:/xiao/dataset_molcreateV2/code/' + save_path)
        result_source.save('G:/xiao/dataset_molcreateV2/code/src_image/' + save_path)
        # plt.imshow(result)
        # plt.show()
    return result

# images_path = 'G:/xiao/dataset_molcreate/image/'
# source_path = 'G:/xiao/dataset_molcreate/source/'
# preimage_path = 'G:/xiao/dataset_molcreate/pro_image/'
#
# def getFiles(path):
#     Filelist = []
#     for home, dirs, files in os.walk(path):
#         for file in files:
#             # 文件名列表，包含完整路径
#             Filelist.append(os.path.join(home, file))
#             #Filelist.append(file)
#     return Filelist
#
# def getSubfolder(path):
#     Filelist = []
#     for dirpath, dirnames, filenames in os.walk(path):
#         file_count = 0
#         for file in filenames:
#             file_count = file_count + 1
#         Filelist.append(dirpath)
#         #print(dirpath,file_count)
#     return Filelist

# style = random.randint(0, 1)
# if style == 0:
#     folders = getSubfolder(preimage_path + '/h/')
# else:
#     folders = getSubfolder(preimage_path + '/w/')
#
# sequence = random.randint(1, len(folders)-1)
# pinjie_path = folders[sequence] + '/'
# files = getFiles(folders[sequence])
#
# if len(files) > 6:
#     num = random.randint(1, 6)
# else:
#     num = random.randint(1, len(files))
# print(folders[sequence], num, len(files))
#
# img = pinjie(pinjie_path, style=style, num=num, image_num=10, save_path='22.png', pixel=[1, 2, 3])
