import numpy as np
from pycocotools.coco import COCO
import json
import os
import matplotlib.pyplot as plt
from skimage import io
import cv2

#使用json头文件读入coco数据集
import json
with open("G:/xiao/dataset_molcreate/create_ann/source/create_18162/annotations/instances_val2017.json",'r') as load_f:
    f = json.load(load_f)

print(f.keys())# dict_keys(['info', 'licenses', 'categories', 'images', 'annotations'])




dataset_dir = 'G:/xiao/dataset_molcreateV2/data/create_ann1/image/'
coco = COCO("G:/xiao/dataset_molcreateV2/data/create_ann1/instances_train2017.json") # 初始化生成COCO对象

categories = coco.loadCats(coco.getCatIds())
#print(categories)

imgIds = coco.getImgIds(catIds=1)
print(len(imgIds))


img_info = coco.loadImgs(imgIds[np.random.randint(0, len(imgIds))])
print(img_info)


imgIds = coco.getImgIds(catIds=1)

for i in range(len(imgIds)):
    img = coco.loadImgs(imgIds[i])[0]
    #print(img['file_name'])
    image = cv2.imread(dataset_dir + img['file_name'])
    #plt.imshow(image)

    annIds = coco.getAnnIds(imgIds=img['id'], catIds=1, iscrowd=0)
    anns = coco.loadAnns(annIds)

    for n in range(len(anns)):
        x, y, w, h = anns[n]['bbox']
        x, y, w, h = int(x), int(y), int(w), int(h)
        # print(x, y, w, h)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255))

    cv2.imwrite('G:/xiao/dataset_molcreateV2/data/create_ann1/check/' + img['file_name'].split('/')[1], image)
    # coco.showAnns(anns)
    # plt.show()
