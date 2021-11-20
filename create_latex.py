# -*-coding:utf-8-*-
# create new pdf, pdf2png, save png

import os
from random_words import LoremIpsum, RandomWords
import random
import cv2
from merge_image_erode import pinjie
import time
from pdf_2_img_Convert import convert

current_dir = os.path.dirname(__file__)

preimage_path = 'G:/xiao/dataset_molcreateV2/data/pre_image/'

head = r"""
\documentclass[a4paper]{article}

\usepackage{graphicx}
\usepackage{multicol}
\usepackage{float}
\usepackage{caption}
\usepackage{geometry}
\usepackage{color}
%\geometry{a4paper,left=2cm,right=2cm,top=1cm,bottom=1cm}
\geometry{a4paper,scale=0.8}
\setlength{\columnsep}{22pt}  
\begin{document}
\begin{multicols}{2}
"""

end = r"""
\end{multicols}
\end{document}
"""

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

# 创建一个txt文件，文件名为mytxtfile,并向文件写入msg
def text_create(name, msg):
    full_path = current_dir + '/' + name + '.tex'
    file = open(full_path, 'a+')

    if os.path.getsize(full_path) == 0:
        file.write(head)
    file.write(msg)
    # file.close()

def add_text(num):
    li = LoremIpsum()
    text = li.get_sentences(num)
    text = text + r"""

\noindent {\color{%s}\rule[-2pt]{%dcm}{%fem}}    

"""%(random.choice(['red', 'black', 'green', 'blue', 'yellow', 'cyan', 'magenta']), random.randint(3, 8), random.uniform(0.05, 0.3))
    return text

def add_onecolumn_image(save_path, pixel):
    style = random.randint(0, 1)
    if style == 0:
        folders = getSubfolder(preimage_path + '/h/')
    else:
        folders = getSubfolder(preimage_path + '/w/')

    sequence = random.randint(1, len(folders) - 1)
    pinjie_path = folders[sequence] + '/'
    files = getFiles(folders[sequence])

    if len(files) > 10:
        image_num = random.randint(6, 10)
    elif len(files) > 5:
        image_num = random.randint(3, len(files))
    else:
        image_num = random.randint(1, len(files))

    if image_num > 5:
        num = random.randint(3, 5)
    else:
        num = random.randint(1, image_num)

    img = pinjie(pinjie_path, style=style, num=num, image_num=image_num, save_path=save_path, pixel=pixel)
    w, h = img.size
    while((h / w >= 2) or w > 4000):
        sequence = random.randint(1, len(folders) - 1)
        pinjie_path = folders[sequence] + '/'
        files = getFiles(folders[sequence])

        if len(files) > 10:
            image_num = random.randint(1, 10)
        else:
            image_num = random.randint(1, len(files))

        if image_num > 5:
            num = random.randint(1, 5)
        else:
            num = random.randint(1, image_num)
        img = pinjie(pinjie_path, style=style, num=num, image_num=image_num, save_path=save_path, pixel=pixel)
        w, h = img.size
    head = r"""
\begin{figure*}[htbp]
\centering
"""
    end = r"""
\end{figure*}
"""
    content = (r"""\includegraphics[width= 0.8\linewidth, keepaspectratio]{%s}""") % (save_path)
    li = LoremIpsum()
    content = content + (r"""
\caption{%s}
""") % (li.get_sentences(1))

    text = head + content + end
    return text

def add_twocolumn_image(save_path, pixel):
    style = random.randint(0, 1)
    if style == 0:
        folders = getSubfolder(preimage_path + '/h/')
    else:
        folders = getSubfolder(preimage_path + '/w/')

    sequence = random.randint(1, len(folders) - 1)
    pinjie_path = folders[sequence] + '/'
    files = getFiles(folders[sequence])

    if len(files) > 10:
        image_num = random.randint(6, 10)
    elif len(files) > 5:
        image_num = random.randint(3, len(files))
    else:
        image_num = random.randint(1, len(files))

    if image_num > 3:
        num = random.randint(1, 3)
    else:
        num = random.randint(1, image_num)
    #print(folders[sequence], num, len(files))

    img = pinjie(pinjie_path, style=style, num=num, image_num=image_num, save_path=save_path, pixel=pixel)
    w, h = img.size
    while((h / w >= 2) or w > 2000):
        sequence = random.randint(1, len(folders) - 1)
        pinjie_path = folders[sequence] + '/'
        files = getFiles(folders[sequence])

        if len(files) > 10:
            image_num = random.randint(1, 10)
        else:
            image_num = random.randint(1, len(files))

        if image_num > 3:
            num = random.randint(1, 3)
        else:
            num = random.randint(1, image_num)
        img = pinjie(pinjie_path, style=style, num=num, image_num=image_num, save_path=save_path, pixel=pixel)
        w, h = img.size

    head = r"""
\begin{figure}[H]
\centering
"""
    end = r"""
\end{figure}
"""

    content = (r"""\includegraphics[width= 0.8\linewidth, keepaspectratio]{%s}""") % (save_path)
    li = LoremIpsum()
    content = content + (r"""
\caption{%s}
""") % (li.get_sentences(1))

    text = head + content + end
    return text

def add_table(columns, rows):
    rw = RandomWords()
    words = rw.random_words(count=columns*rows)

    if columns <= 3:
        head = r'''
\begin{table}[H]
\centering
\setlength{\tabcolsep}{%dmm}{        
\begin{tabular}{%s}
\hline
'''%(random.randint(3, 15), ' c ' * columns)
        content_string = ''
        for row in range(rows):
            string = ''
            for column in range(columns):
                string = string + words[column*row + column]
                if column < (columns-1):
                    string = string + ' & '
            string = string + r' \\'
            content_string = content_string + string
        content = r'''
%s
'''%(content_string)

        end = r'''
\end{tabular}}
\end{table}
                   
'''
    else:
        head = r'''
\begin{table*}[htbp]
\centering 
\setlength{\tabcolsep}{%dmm}{    
\begin{tabular}{%s}
\hline'''%(random.randint(3, 20), ' c ' * columns)

        content_string = ''
        for row in range(rows):
            string = ''
            for column in range(columns):
                string = string + words[column * row + column]
                if column < (columns - 1):
                    string = string + ' & '
            string = string + r' \\'
            if row == 0:
                string = string + ' \hline '
            content_string = content_string + string
        content = r'''
        %s
        ''' % (content_string)

        end = r'''
\end{tabular}}
\end{table*}

'''
    text = head + content + end
    return text

def add_other_image(save_path):
    files = getFiles(save_path)

    path = files[random.randint(0, len(files)-1)]
    path = path.split('G:/xiao/dataset_molcreateV2/code/')[1]

    style = random.randint(0, 1)
    if style == 1:
        head = r"""
\begin{figure}[H]
\centering
"""
        end = r"""
\end{figure}
"""
    else:
        head = r"""
\begin{figure*}[htbp]
\centering
"""
        end = r"""
\end{figure*}
"""

    content = (r"""\includegraphics[width= 0.8\linewidth, keepaspectratio]{%s}""") % (path)
    li = LoremIpsum()
    content = content + (r"""
\caption{%s}
""") % (li.get_sentences(1))

    text = head + content + end

    return text


if __name__ == '__main__':
    i = 0
    while(i < 200):
        i = i + 1
        name = str(int(time.time()))

        if not os.path.exists('G:/xiao/dataset_molcreateV2/code/gen_image/'):
            os.makedirs('G:/xiao/dataset_molcreateV2/code/gen_image/')
        if not os.path.exists('G:/xiao/dataset_molcreateV2/code/src_image/'):
            os.makedirs('G:/xiao/dataset_molcreateV2/code/src_image/')
        if not os.path.exists('G:/xiao/dataset_molcreateV2/code/gen_image/' + name):
            os.makedirs('G:/xiao/dataset_molcreateV2/code/gen_image/' + name)
        if not os.path.exists('G:/xiao/dataset_molcreateV2/code/src_image/gen_image/'):
            os.makedirs('G:/xiao/dataset_molcreateV2/code/src_image/gen_image/')
        if not os.path.exists('G:/xiao/dataset_molcreateV2/code/src_image/gen_image/' + name):
            os.makedirs('G:/xiao/dataset_molcreateV2/code/src_image/gen_image/' + name)

        text_create(name, add_onecolumn_image('gen_image/' + name + '/1.png', pixel=[10, 70, 130]))
        for t in range(1, 3):
            text_create(name, add_text(random.randint(2, 8)))

        text_create(name, add_table(random.randint(2, 10), random.randint(3, 14)))
        text_create(name, add_twocolumn_image('gen_image/' + name + '/2.png', pixel=[20 , 80, 140]))
        for t in range(2, 8):
            text_create(name, add_text(random.randint(2, 8)))

        text_create(name, add_twocolumn_image('gen_image/' + name + '/3.png', pixel=[30, 90, 150]))
        for t in range(2, 8):
            text_create(name, add_text(random.randint(2, 8)))

        text_create(name, add_twocolumn_image('gen_image/' + name + '/4.png', pixel=[40, 100, 160]))
        text_create(name, add_other_image('G:/xiao/dataset_molcreateV2/code/other_elements/pymol_graphs/'))
        text_create(name, add_table(random.randint(2, 10), random.randint(3, 14)))
        for t in range(2, 8):
            text_create(name, add_text(random.randint(2, 8)))

        text_create(name, add_other_image('G:/xiao/dataset_molcreateV2/code/other_elements/pymol_graphs/'))
        text_create(name, add_twocolumn_image('gen_image/' + name + '/5.png', pixel=[50, 110, 170]))
        text_create(name, add_table(random.randint(2, 10), random.randint(3, 14)))
        for t in range(2, 8):
            text_create(name, add_text(random.randint(2, 8)))

        text_create(name, add_twocolumn_image('gen_image/' + name + '/6.png', pixel=[60, 120, 180]))
        for t in range(2, 8):
            text_create(name, add_text(random.randint(2, 8)))

        text_create(name, add_twocolumn_image('gen_image/' + name + '/7.png', pixel=[70, 120, 190]))
        text_create(name, add_other_image('G:/xiao/dataset_molcreateV2/code/other_elements/pymol_graphs/'))
        text_create(name, add_table(random.randint(2, 10), random.randint(3, 14)))
        for t in range(2, 8):
            text_create(name, add_text(random.randint(2, 8)))

        text_create(name, add_onecolumn_image('gen_image/' + name + '/8.png', pixel=[80, 130, 200]))
        text_create(name, add_table(random.randint(2, 10), random.randint(3, 14)))
        text_create(name, add_other_image('G:/xiao/dataset_molcreateV2/code/other_elements/pymol_graphs/'))
        for t in range(2, 8):
            text_create(name, add_text(random.randint(2, 8)))

        text_create(name, end)
        command = 'F:/2345Installs/texliver/2021/bin/win32/pdflatex %s.tex'%(name)
        os.system(command)
        #time.sleep(3)
        pdf_path = 'G:/xiao/dataset_molcreateV2/code/' + '%s.pdf'%(name)
        convert(pdf_path, outputpath='G:/xiao/dataset_molcreateV2/data/create_ann/ann/' + '%s.pdf'%(name))

        f = open('%s.tex'%(name), 'r', encoding='utf-8')
        f_new = open('%s.tex'%(name + '_src'), 'w', encoding='utf-8')

        for line in f:
            # 进行判断
            if "gen_image" in line:
                line = line.replace('gen_image', 'src_image/gen_image')
            # 如果不符合就正常的将文件中的内容读取并且输出到新文件中
            f_new.write(line)

        f.close()
        f_new.close()

        command = 'F:/2345Installs/texliver/2021/bin/win32/pdflatex %s.tex'%(name + '_src')
        os.system(command)
        #time.sleep(3)
        pdf_path = 'G:/xiao/dataset_molcreateV2/code/' + '%s.pdf'%(name + '_src')
        convert(pdf_path, outputpath='G:/xiao/dataset_molcreateV2/data/create_ann/image/' + '%s.pdf'%(name))

        os.remove('%s.tex'%name)
        os.remove('%s.tex' % (name + '_src'))
        os.remove('%s.pdf'%name)
        os.remove('%s.pdf' % (name + '_src'))
        os.remove('%s.log' % name)
        os.remove('%s.log' % (name + '_src'))
        os.remove('%s.aux' % name)
        os.remove('%s.aux' % (name + '_src'))
        # os.remove('%s.out' % name)
        # os.remove('%s.out' % (name + '_src'))
