
import json
import os

path = 'G:/xiao/dataset_molcreateV2/data/json/'
entries = os.listdir(path)
entries.sort()

main = open(path + entries[0])
main = json.load(main)

# 第一个json文件 image的数量
main_image_number = len(main['images'])
main_annotation_number = len(main['annotations'])

for entry in entries[1:]:
    file = open(path + entry)
    file = json.load(file)

    for i in file['images']:
        main['images'].append(i)

    for i in file['annotations']:
        main['annotations'].append(i)

for i in range(len(main['images'])):
    main['images'][i]['id'] = i+1
for i in range(len(main['annotations'])):
    main['annotations'][i]['id'] = i+1
    if main['annotations'][i]['id'] > main_annotation_number:
        main['annotations'][i]['image_id'] = main['annotations'][i]['image_id'] + main_image_number

with open('G:/xiao/dataset_molcreateV2/data/json/data.json', 'w') as outfile:
    json.dump(main, outfile)
