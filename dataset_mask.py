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
import complete_structure
from skimage import data,color,morphology
import time


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
        #start = time.time()
        #print(start, file)
        # if file != 'G:/xiao/dataset_molcreate/create_ann/image/1635312674.pdf/1635312674_src.pdf_2.png':
        #     continue
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

        # 记录每一张图像的masks 维度是[n, h, w] n是每张图mask的数量
        mask_array = []
        values = [[10, 70, 130], [20, 80, 140], [30, 90, 150], [40, 100, 160], [50, 110, 170], [60, 120, 180], [70, 120, 190], [80, 130, 200]]
        for value in values:
            # 判断第一个有没有，没有就跳过
            arr = image_np.reshape(-1, 3)

            labels = (arr == [value[0], value[1], value[2]]).all(1)

            if len(set(labels)) == 1:
                continue

            for j in range(10):
                labels = (arr == [value[0] + j, value[1] + j, value[2] + j]).all(1)

                if len(set(labels)) == 1:
                    break
                if len(labels.astype(np.int8)[labels == True]) < 50:
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
                gt_masks = mask_array1#complete_structure.complete_structure_mask(image_array=np.array(image_alone), mask_array=np.array(mask_array1), debug=False)
                labels_arr = gt_masks.reshape(image_np[:, :, 0].shape)
                '''

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

                # 扩展周围的像素点
                #height, width = image_np[:,:,0].shape
                # for h, w in np.argwhere(labels_arr == True):
                #     for _w_ in [w - 1, w, w + 1]:
                #         for _h_ in [h - 1, h, h + 1]:
                #             if _w_ > width - 1:
                #                 continue
                #             if _h_ > height - 1:
                #                 continue
                #             if _w_ == w and _h_ == h:
                #                 continue
                #
                #             if ((image_np[_h_][_w_] == [254, 254, 254]).all()) or ((image_np[_h_][_w_] == [255, 255, 255]).all()):
                #                 print('nonono', _h_, _w_, image_np[_h_][_w_], new_arr[_h_][_w_])
                #             else:
                #                 print(_h_, _w_, image_np[_h_][_w_], new_arr[_h_][_w_])
                #                 new_arr[_h_][_w_] = image_np[h][w]
                #
                #                 print(_h_, _w_, image_np[_h_][_w_], new_arr[_h_][_w_])

        if mask_label == True:
            image_info = pycococreatortools.create_image_info(image_id, file.split('/image/')[1], img.size)
            coco_output["images"].append(image_info)
            image_id = image_id + 1

            mask_array = np.array(mask_array)
            for i in range(mask_array.shape[0]):
                # plt.imshow(mask_array[i])
                # plt.show()
                # 把img和mask合并
                colors = random_colors(50)
                color = colors[i]
                masked_image = apply_mask(masked_image, mask_array[i], color)

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
    path = 'G:/xiao/dataset_molcreate/create_ann/'
    # mask_annjson(path)
    '''
    with open(path + "16353126451_ins.pkl", 'rb') as f:
        # 反序列化解析成列表a
        a = pickle.load(f)

    print(a['image_name'])
    print(a['mask_array'].shape)

    filename = path + '1635312645_1.nii.gz'
    img = SimpleITK.ReadImage(filename)  # SimpleITK object
    data = SimpleITK.GetArrayFromImage(img)  # numpy array
    print(data.shape)
    if a['mask_array'].all() == data.all():
        print('same')
    for i in range(data.shape[0]):
        plt.imshow(data[i])
        plt.show()
    '''
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.submit(mask_annjson, path)