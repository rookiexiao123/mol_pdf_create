import SimpleITK
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('AGG')
import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm


def getFiles(path):
    Filelist = []
    for home, dirs, files in os.walk(path):
        for file in files:
            # 文件名列表，包含完整路径
            file_path = os.path.join(home, file).replace('\\', '/')
            Filelist.append(file_path)
            #Filelist.append(file)
    return Filelist

path = 'G:/xiao/dataset_molcreateV2/data/create_ann1/nii/'
masks_path = getFiles(path)

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


for mask_path in tqdm(masks_path):
    time_name = os.path.split(mask_path)[1].split('_')[0]
    count_name = os.path.split(mask_path)[1].split('_')[1].split('.')[0]
    image_path = os.path.split(mask_path)[0].replace('nii', 'image') + '/' + str(time_name) + '.pdf/' + str(time_name) + '_src.pdf_' + str(count_name) + '.png'
    #print(image_path)
    try:
        image = Image.open(image_path)

        mask = SimpleITK.ReadImage(mask_path)
        mask_array = SimpleITK.GetArrayFromImage(mask)
        #print(mask_path, mask_array.shape)

        for i in range(mask_array.shape[0]):

            image_np = mask_array[i]
            cols_status = np.any(image_np, axis=0)
            x_index = np.where(cols_status)[0]

            rows_status = np.any(image_np, axis=1)
            y_index = np.where(rows_status)[0]
            #print(x_index[0], x_index[-1], y_index[0], y_index[-1])

            top_left = (x_index[0], y_index[0])
            right_bottom = (x_index[-1], y_index[-1])

            image_np = image_np.reshape((image_np.shape[0], image_np.shape[1], 1))
            bbox = extract_bboxes(image_np)
            #print(bbox[0][0])

            plt.gca().add_patch(plt.Rectangle(xy=(bbox[0][1], bbox[0][0]),
                                              width=bbox[0][3] - bbox[0][1],
                                              height=bbox[0][2] - bbox[0][0],
                                              edgecolor='red',
                                              fill=False, linewidth=2))

        plt.imshow(image)
        # plt.title(str(time_name) + '_src.pdf_' + str(count_name) + '.png', fontsize=10)
        # plt.show()
        plt.savefig('G:/xiao/dataset_molcreateV2/data/create_ann1/check/' + str(time_name) + '_src.pdf_' + str(count_name) + '.png')
        plt.close('all')
    except:
        print('error : ', image_path)