import xml.etree.ElementTree as ET
from os import listdir, getcwd, makedirs, path

from tqdm import tqdm

'''
    将labelImg工具生成的VOC格式标签转化成YOLO格式标签
        XML文件的默认路径在Annotations文件夹下
        TXT文件会在生成的yolo_format文件夹下
'''

classes = ['0B', '1B', '2B']

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    in_file = open('VOCdevkit/VOC2007/Annotations/%s.xml'%(image_id))
    out_file = open('yolo_format/%s.txt'%(image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes :
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

if __name__ == '__main__':
    if not path.exists('yolo_format'):
        makedirs('yolo_format')

    wd = getcwd()
    b=0 #文件计数
    list_file = listdir('VOCdevkit/VOC2007/Annotations')
    for file in tqdm(list_file):
        f=file.replace('.xml','')
        convert_annotation(f)
        b=b+1