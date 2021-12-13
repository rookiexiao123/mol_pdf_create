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


def mask_annjson(path):
    files = getFiles(path + 'image/')
    image_id = 1
    segmentation_id = 1
    print(len(files))
    for i, file in enumerate(tqdm(files)):
        img = Image.open(file)
        mask_label = False
        # 1634709941
        name = os.path.split(file)[1].split('_')[0]
        # 1
        num = os.path.split(file)[1].split('_')[2].split('.')[0]
        # 1635312645.pdf/1635312645.pdf_1.png

        mask = SimpleITK.ReadImage(path + 'nii/' + str(name) + '_' + str(num) + '.nii.gz')
        mask_array = SimpleITK.GetArrayFromImage(mask)

        if mask_array.shape[0] > 1:
            bboxes = []
            for i in range(mask_array.shape[0]):
                image_np = mask_array[i]
                image_np = image_np.reshape((image_np.shape[0], image_np.shape[1], 1))

                bbox = extract_bboxes(image_np)
                bboxes.append(bbox)
            result_flag = False
            for m in range(len(bboxes)):
                for n in range(m+1, len(bboxes)):
                    result = mat_inter((bboxes[m][0][0], bboxes[m][0][1], bboxes[m][0][2], bboxes[m][0][3]), (bboxes[n][0][0], bboxes[n][0][1], bboxes[n][0][2], bboxes[n][0][3]))
                    if result == True:
                        result_flag = True
                        print('true', file, len(bboxes))
                        break
                if result_flag == True:
                    break
            if result_flag == False:
                class_id = 1
                category_info = {'id': class_id, 'is_crowd': 0}

                for num in range(mask_array.shape[0]):
                    annotation_info = pycococreatortools.create_annotation_info(segmentation_id, image_id, category_info, mask_array[num], tolerance=2)
                    if annotation_info is not None:
                        mask_label = True
                        coco_output["annotations"].append(annotation_info)

                        segmentation_id = segmentation_id + 1
        else:
            class_id = 1
            category_info = {'id': class_id, 'is_crowd': 0}

            annotation_info = pycococreatortools.create_annotation_info(segmentation_id, image_id, category_info, mask_array[0], tolerance=2)

            if annotation_info is not None:
                mask_label = True
                coco_output["annotations"].append(annotation_info)

                segmentation_id = segmentation_id + 1

        if mask_label == True:
            image_info = pycococreatortools.create_image_info(image_id, file.split('/image/'), img.size)
            coco_output["images"].append(image_info)
            image_id = image_id + 1



    with open(path + '2.json', 'w') as output_json_file:
        json.dump(coco_output, output_json_file, cls=NpEncoder)
    print('it is ok!')




import concurrent.futures
if __name__ == "__main__":
    path = 'G:/xiao/dataset_molcreateV2/data/create_ann1/'
    mask_annjson(path)
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     executor.submit(mask_annjson, path)