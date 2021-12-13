from PIL import Image
import os
import datetime
import json
import os
import re
import fnmatch
from PIL import Image
import numpy as np
from pycococreatortools import pycococreatortools
import matplotlib.pyplot as plt
from tqdm import tqdm
import colorsys
import random
import pickle
import h5py
import SimpleITK
from skimage import data,color,morphology
import time
import cv2
import numpy as np
from skimage.morphology import binary_erosion


def getFiles(path):
    Filelist = []
    for home, dirs, files in os.walk(path):
        for file in files:
            # 文件名列表，包含完整路径
            file_path = os.path.join(home, file).replace('\\', '/')
            Filelist.append(file_path)
            #Filelist.append(file)
    return Filelist

def getSubfolder(path):
    Filelist = []
    for dirpath, dirnames, filenames in os.walk(path):
        file_count = 0
        for file in filenames:
            file_count = file_count + 1
        Filelist.append(dirpath)
        #print(dirpath,file_count)
    return Filelist

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

def mat_inter(box1,box2):
    y01, x01, y02, x02 = box1
    y11, x11, y12, x12 = box2
    lx = abs((x01 + x02) / 2 - (x11 + x12) / 2)
    ly = abs((y01 + y02) / 2 - (y11 + y12) / 2)
    sax = abs(x01 - x02)
    sbx = abs(x11 - x12)
    say = abs(y01 - y02)
    sby = abs(y11 - y12)
    if lx <= (sax + sbx) / 2 and ly <= (say + sby) / 2:
        return True
    else:
        return False


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print(path + "---OK---")
    else:
        print(path + "---There is this folder!---")

INFO = {
    "description": "Chemical Dataset",
    "url": "https://github.com/waspinator/pycococreator",
    "version": "0.1.0",
    "year": 2021,
    "contributor": "xiao",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]

# 根据自己的需要添加种类
CATEGORIES = [
    {
        'id': 1,
        'name': 'formula',
        'supercategory': 'Chemical',
    }
]

coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

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

def mask_annjson(path):
    files = getFiles(path+'image')
    image_id = 1
    segmentation_id = 1
    print(len(files))
    for i, file in enumerate(tqdm(files)):
        img = Image.open(file)
        masked_image = np.array(img).copy()
        mask_label = False
        # 1634709941
        name = os.path.split(file)[1].split('_')[0]
        # 1.png
        num = os.path.split(file)[1].split('_')[2]
        # 1635312645.pdf/1635312645.pdf_1.png
        #image_name = name + '.pdf/' + name + '.pdf_' + num

        img_ann = Image.open(path + 'ann/' + name + '.pdf/' + name + '.pdf_' + num)
        image_np = np.array(img_ann)

        # # Load image
        # im = cv2.imread(path + 'ann/' + name + '.pdf/' + name + '.pdf_' + num)[:300,:1000]
        # print(im.shape)
        # # Define the blue colour we want to find - remember OpenCV uses BGR ordering
        # blue = [210, 110, 10]
        # #img = np.array([[[1,2,3],[4,5,6]],[[3,2,1],[1,2,3]],[[4,5,6],[6,5,4]]])


        # # tt=im.reshape(-1,3)
        # # ttt=set([str(i) for i in tt])
        # # print(ttt)
        # # Get X and Y coordinates of all blue pixels
        # X, Y = np.where(np.all(im == blue, axis=2))
        #
        # print(X, Y)


        # zipped = np.column_stack((X, Y))
        # print(zipped.size)

        # 记录每一张图像的masks 维度是[n, h, w] n是每张图mask的数量
        mask_array = []
        mask_array_color = []
        values = [[10, 110, 210], [20, 120, 220], [30, 130, 230]]#[[10, 70, 130], [20, 80, 140], [30, 90, 150], [40, 100, 160], [50, 110, 170], [60, 120, 180], [70, 130, 190], [80, 140, 200]]
        for value in values:
            # 判断第一个有没有，没有就跳过
            arr = image_np.reshape(-1, 3)
            #print(arr.shape)
            labels = (arr == [value[0], value[1], value[2]]).all(1)
            #print(len(set(labels)), value)
            if len(set(labels)) == 1:
                continue

            for j in range(10):
                labels = (arr == [value[0] + j, value[1] + j, value[2] + j]).all(1)

                if len(set(labels)) == 1:
                    continue
                if len(labels.astype(np.int8)[labels == True]) < 200:
                    continue
                '''
                null_arr = np.ones(arr.shape) * 255
                null_arr[labels] = [value[0] + j, value[1] + j, value[2] + j]
                new_arr = null_arr.reshape(image_np.shape)
                image_alone = Image.fromarray(new_arr.astype('uint8')).convert('RGB')
                '''
                # value = True or False
                labels_arr = labels.reshape(image_np[:, :, 0].shape)
                # value = 1 or 0
                labels_arr = np.asarray(labels_arr).astype(np.uint8)
                '''
                labels_arr = morphology.convex_hull_image(labels_arr)
                labels_arr = np.where(labels_arr == True, 1, 0)
                mask_array1 = labels_arr.reshape((labels_arr.shape[0], labels_arr.shape[1], 1))
                '''
                mask_array_color.append(labels_arr)

                labels_arr = np.where(labels_arr == 0, 1, 0)
                blur_factor = 12
                kernel = np.ones((blur_factor, blur_factor))
                blurred_image_array = binary_erosion(labels_arr, selem=kernel)
                blurred_image_array = np.where(blurred_image_array == 0, 1, 0)
                labels_arr = blurred_image_array

                mask_array.append(labels_arr)

                mask_label = True

                class_id = 1
                category_info = {'id': class_id, 'is_crowd': 0}

                if len(set(labels)) == 2:
                    annotation_info = pycococreatortools.create_annotation_info(segmentation_id, image_id, category_info, labels_arr, tolerance=2)

                    if annotation_info is not None:
                        mask_label = True
                        coco_output["annotations"].append(annotation_info)

                        segmentation_id = segmentation_id + 1

        if mask_label == True:
            image_info = pycococreatortools.create_image_info(image_id, name + '.pdf_' + num, img.size)
            coco_output["images"].append(image_info)
            image_id = image_id + 1

            mask_array = np.array(mask_array)
            colors = random_colors(50)
            for i in range(mask_array.shape[0]):
                # plt.imshow(mask_array[i])
                # plt.show()
                # 把img和mask合并
                color = colors[i]

                masked_image = apply_mask(masked_image, mask_array_color[i], color)

            masked_image_save = Image.fromarray(masked_image.astype(np.uint8))
            masked_image_save.save(path + 'mask/' + name + '.pdf_' + num)

            out = SimpleITK.GetImageFromArray(np.array(mask_array))
            SimpleITK.WriteImage(out, path + '/nii/' + str(name) + '_' + str(num).split('.')[0] + '.nii.gz')
        else:
            os.remove(file)
            os.remove(path + 'ann/' + name + '.pdf/' + name + '.pdf_' + num)
    with open(path + 'instances_train2017.json', 'w') as output_json_file:
        json.dump(coco_output, output_json_file, cls=NpEncoder)
    print('it is ok!')

import concurrent.futures
if __name__ == "__main__":
    path = 'G:/xiao/dataset_molcreateV2/data/create_ann/'
    mask_annjson(path)
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     executor.submit(mask_annjson, path)