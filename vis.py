import matplotlib.pyplot as plt
import os
import cv2
import numpy as np
from PIL import Image


def getFiles(path):
    Filelist = []
    for home, dirs, files in os.walk(path):
        for file in files:
            # 文件名列表，包含完整路径
            Filelist.append(os.path.join(home, file))
            #Filelist.append(file)
    return Filelist

# 按比例resize Image
def resize_image(path, length):
    img = cv2.imread(path)
    h, w, _ = img.shape

    if h >= w:
        width = length * w / h
        height = length

    else:
        height = length * h / w
        width = length

    return height, width

if __name__ == "__main__":
    values = [[10, 70, 130], [20 , 80, 140], [30, 90, 150], [40, 100, 160], [50, 110, 170], [60, 120, 180], [70, 120, 190], [80, 130, 200]]
    for value in values:
        for i in range(10):
            image = Image.open('G:/xiao/dataset_molcreateV2/data/vis_show/2.png')

            image_np = np.array(image)
            arr = image_np.reshape(-1,3)

            null_arr = np.ones(arr.shape) * 255
            labels = (arr==[value[0]+i, value[1]+i, value[2]+i]).all(1)
            #print(labels.shape)

            null_arr[labels]=[value[0]+i, value[1]+i, value[2]+i]
            new_arr=null_arr.reshape(image_np.shape)

            #labels_arr = labels.reshape(image_np[:,:,0].shape)
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



            if len(set(labels)) == 1:
                pass
            else:
                print(value[0] + i, labels.shape, len(labels.astype(np.int8)[labels == True]), len(set(labels)), set(labels))
                image_np = Image.fromarray(new_arr.astype('uint8')).convert('RGB')

                new_arr = np.where(new_arr==[255, 255, 255], 255, 0)
                plt.imshow(image_np)
                plt.show()

                # image_np = image_np.resize((image_np.size[0]//4, image_np.size[1]//4), Image.ANTIALIAS)
                # plt.imshow(image_np)
                # plt.show()
                #
                # image_np = image_np.resize((image_np.size[0]*4, image_np.size[1]*4), Image.ANTIALIAS)
                # plt.imshow(image_np)
                # plt.show()
