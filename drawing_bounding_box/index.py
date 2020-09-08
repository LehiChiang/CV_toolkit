import colorsys
from os import path, listdir, makedirs, getcwd, _exit
import time
import cv2
import argparse
import xml.etree.ElementTree as ET
import numpy as np


def get_parser():
    parser = argparse.ArgumentParser(description='Input visualization parameters')
    parser.add_argument('--label', type=str, required=False, default='Annotations',
                        help='Input the labels folder')
    parser.add_argument('--image', type=str, required=False, default='JPEGImages',
                        help='Input the images folder')
    parser.add_argument('--output', type=str, required=False, default='outcome',
                        help='Input the folder of outcome images')
    return parser


def mkdir(dirpath):
    if not path.exists(dirpath):
        makedirs(dirpath)
        logshow(("Directory created successfully!"))


def logshow(message):
    logtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if isinstance(message,tuple):
        for m in message:
            print(logtime, m)
    else:
        print(logtime, message)


def get_class():
    classes_path = path.expanduser('classes.txt')
    with open(classes_path) as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names


def get_colors(length):
    # Generate colors for drawing bounding boxes.
    hsv_tuples = [(x / length, 1., 1.)
                  for x in range(length)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))
    np.random.seed(10101)  # Fixed seed for consistent colors across runs.
    np.random.shuffle(colors)  # Shuffle colors to decorrelate adjacent classes.
    np.random.seed(None)  # Reset seed to default.
    return colors

def main():
    args = get_parser().parse_args()
    label_input_dir = path.expanduser(args.label)
    images_input_dir = path.expanduser(args.image)
    outcome_dir = path.expanduser(args.output)
    if not path.exists(label_input_dir) or not path.exists(images_input_dir):
        logshow(("*"*50, 'Label folder or image folder do not exist! Please check it later.', '*'*50))
        _exit(0)
    logshow((label_input_dir, images_input_dir, outcome_dir))
    mkdir(outcome_dir)

    class_names = get_class()
    colors = get_colors(len(class_names))

    filenames =[name.split('.')[0] for name in listdir(label_input_dir)]
    for name in filenames:
        tree = ET.parse(path.join(label_input_dir, '{}.xml'.format(name)))
        root = tree.getroot()
        url = path.join(images_input_dir, name+'.jpg')
        img = cv2.imread(url, 1)
        for object in root.findall('object'):
            cls = object.find('name').text
            bndbox = object.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)
            cv2.putText(img, cls, (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[class_names.index(cls)], 1, cv2.LINE_AA, False)
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), colors[class_names.index(cls)], 2, cv2.LINE_AA)

        cv2.imshow('Image', img)
        savepath = path.join(outcome_dir, '{}.jpg'.format(name))
        cv2.imwrite(savepath,img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
        logshow('Saving image to {}'.format(savepath))
        cv2.waitKey(100)


if __name__ == '__main__':
    main()
