# pinjie image with erode

from os import listdir
from PIL import Image
import os
import math
import random
import matplotlib.pyplot as plt
import numpy as np
from skimage import data,color,morphology
import cv2
import colorsys
from skimage.morphology import binary_erosion


def random_colors(N, bright=True):
    """
    Generate random colors.
    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    """
    brightness = 1.0 if bright else 0.7
    hsv = [(i / N, 1, brightness) for i in range(N)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.shuffle(colors)
    return colors

def apply_mask(image, mask, color, alpha=0.5):
    """Apply the given mask to the image.
    """
    for c in range(3):
        image[:, :, c] = np.where(mask == 1, image[:, :, c] * (1 - alpha) + alpha * color[c] * 255, image[:, :, c])
    return image

def extract_bboxes(mask):
    """Compute bounding boxes from masks.
    mask: [height, width, num_instances]. Mask pixels are either 1 or 0.

    Returns: bbox array [num_instances, (y1, x1, y2, x2)].
    """
    boxes = np.zeros([mask.shape[-1], 4], dtype=np.int32)
    for i in range(mask.shape[-1]):
        m = mask[:, :, i]
        # Bounding box.
        horizontal_indicies = np.where(np.any(m, axis=0))[0]
        vertical_indicies = np.where(np.any(m, axis=1))[0]
        if horizontal_indicies.shape[0]:
            x1, x2 = horizontal_indicies[[0, -1]]
            y1, y2 = vertical_indicies[[0, -1]]
            # x2 and y2 should not be part of the box. Increment by 1.
            x2 += 1
            y2 += 1
        else:
            # No mask for this instance. Might happen due to
            # resizing or cropping. Set bbox to zeros
            x1, x2, y1, y2 = 0, 0, 0, 0
        x1 = 0 if x1 < 0 else x1
        y1 = 0 if y1 < 0 else y1
        y2 = mask.shape[0] - 1 if y2 >= mask.shape[0] else y2
        x2 = mask.shape[1] - 1 if x2 >= mask.shape[1] else x2
        boxes[i] = np.array([y1, x1, y2, x2])
    return boxes.astype(np.int32)


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

            img_array = np.array(im)
            #img_array = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)
            image_np = np.where(np.array(im.convert('L')) <= 150, 0, 1)

            # cols_status = np.any(image_np, axis=0)
            # x_index = np.where(cols_status)[0]
            #
            # rows_status = np.any(image_np, axis=1)
            # y_index = np.where(rows_status)[0]
            # print(x_index[0], x_index[-1], y_index[0], y_index[-1])
            #
            # top_left = (x_index[0], y_index[0])
            # right_bottom = (x_index[-1], y_index[-1])

            #image_np = image_np.reshape((image_np.shape[0], image_np.shape[1], 1))
            # bbox = extract_bboxes(image_np)

            image_np = np.asarray(image_np).astype(np.float32)
            # img = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)
            # contours, hierarchy = cv2.findContours(np.array(image_np, np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            # print(len(contours))
            # for i in range(len(contours)):
            #     cv2.drawContours(img, contours, i, (255, 255, 0), 5)
            #     cv2.imshow('contour-%d' % i, img)
            #     cv2.waitKey()
            #
            # cv2.destroyAllWindows()
            # plt.subplot(1, 2, 1)
            # plt.imshow(image_np)
            #plt.show()


            blur_factor = 12
            kernel = np.ones((blur_factor, blur_factor))
            blurred_image_array = binary_erosion(image_np, selem=kernel)
            blurred_image_array = np.where(blurred_image_array == 0, 1, 0)
            #blurred_image_array = image_np
            # plt.imshow(blurred_image_array)
            # plt.show()

            # chull = morphology.convex_hull_image(image_np)
            # chull = np.where(chull == True, 1, 0)
            # chull = chull.reshape((chull.shape[0], chull.shape[1], 1))


            # colors = random_colors(50)
            # color = colors[random.randint(0, 50)]
            # masked_image = apply_mask(img_array, blurred_image_array, color)
            #
            # masked_image_save = Image.fromarray(masked_image.astype(np.uint8))
            # masked_image_save.save('G:/xiao/workspace/image_seg/create_dataset/1.png')

            gt_masks = blurred_image_array
            gt_masks = np.asarray(gt_masks).astype(np.float32)
            gt_masks = cv2.cvtColor(gt_masks, cv2.COLOR_GRAY2RGB)

            image_np = np.where(np.array(gt_masks) == 1, [p + i for p in pixel], 255)
            im = Image.fromarray(image_np.astype('uint8')).convert('RGB')
            result.paste(im, box=(all_length, im_list[0].size[1] * math.floor(i/num)))
            all_length = all_length + im.size[0]
            if (i+1) % num == 0:
                all_length = 0

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
            img_array = np.array(im)
            image_np = np.where(np.array(im.convert('L')) <= 150, 0, 1)

            image_np = np.asarray(image_np).astype(np.float32)

            blur_factor = 12
            kernel = np.ones((blur_factor, blur_factor))
            blurred_image_array = binary_erosion(image_np, selem=kernel)
            blurred_image_array = np.where(blurred_image_array == 0, 1, 0)
            #blurred_image_array = image_np
            gt_masks = blurred_image_array
            gt_masks = np.asarray(gt_masks).astype(np.float32)
            gt_masks = cv2.cvtColor(gt_masks, cv2.COLOR_GRAY2RGB)

            image_np = np.where(np.array(gt_masks) == 1, [p + i for p in pixel], 255)
            im = Image.fromarray(image_np.astype('uint8')).convert('RGB')
            result.paste(im, box=(im_list[0].size[0] * math.floor(i/num), all_length))
            all_length = all_length + im.size[1]
            if (i+1) % num == 0:
                all_length = 0

        # 保存图片
        result.save('G:/xiao/dataset_molcreateV2/code/' + save_path)
        result_source.save('G:/xiao/dataset_molcreateV2/code/src_image/' + save_path)
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

# style = 0#random.randint(0, 1)
# if style == 0:
#     folders = getSubfolder(preimage_path + '/h/')
# else:
#     folders = getSubfolder(preimage_path + '/w/')

# sequence = random.randint(1, len(folders)-1)
# pinjie_path = folders[sequence] + '/'
# files = getFiles(folders[sequence])
#
# if len(files) > 6:
#     num = random.randint(1, 6)
# else:
#     num = random.randint(1, len(files))
# print(folders[sequence], num, len(files))

#img = pinjie(pinjie_path, style=style, num=1, image_num=1, save_path='22.png', pixel=[10, 70, 130])

'''
import cv2 as cv
img = cv.imread('1.png')
cv.imshow('img', img)
cv.waitKey(0)
cv.destroyAllWindows()

#需要调试下列函数的参数，将图像二值化，网址见https://www.cnblogs.com/yinliang-liang/p/9293310.html
_,img=cv.threshold(img,127,255,cv.THRESH_BINARY)
cv.imshow('img', img)
cv.waitKey(0)
cv.destroyAllWindows()
#需要调试kernel参数
kernel = np.ones((3, 3), np.uint8)
#需要调试iteration参数
erosion_1 = cv.erode(img, kernel, iterations=1)
kernel_1 = np.ones((6, 6), np.uint8)
erosion_2 = cv.erode(img, kernel_1, iterations=1)
erosion_3 = cv.erode(img, kernel_1, iterations=2)
erosion_4 = cv.erode(img, kernel_1, iterations=5)
#可以将多组参数合并一起查看
cv.imshow('erosion', np.hstack((erosion_1, erosion_2,erosion_3,erosion_4)))
cv.waitKey(0)
cv.destroyAllWindows()
'''