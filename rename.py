import os
from PIL import Image

def myrename(path):
    file_list=os.listdir(path)
    for i,fi in enumerate(file_list):
        old_dir=os.path.join(path,fi)
        filename=str(i+1)+"."+str(fi.split(".")[-1])
        new_dir=os.path.join(path,filename)
        try:
            os.rename(old_dir,new_dir)
        except Exception as e:
            print(e)
            print("Failed!")
        else:
            print("SUcess!")

if __name__=="__main__":
    path="G:/xiao/dataset_molcreateV2/code/other_elements/arrow/"
    myrename(path)

