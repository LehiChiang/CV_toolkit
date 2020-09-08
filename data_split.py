import os
import shutil
import random

# 将一个大的VOC格式的数据集分割成COCO格式的训练集，验证集和测试集
# 其中VOC格式中的标记文件夹Annotations和JPEGImages被分割成三部分:
# trainset, valset, testset
# 三部分分割完毕后，将VOC格式的数据集转换成COCO格式的数据集

def move_path(name, folder):
    old_img_path = os.path.join(img_path, name + '.jpg')
    old_anno_path = os.path.join(anno_path, name + '.xml')
    new_img_path = os.path.join(img_folder, folder)
    new_anno_path = os.path.join(anno_folder, folder)
    shutil.move(old_img_path, new_img_path)
    shutil.move(old_anno_path, new_anno_path)


if __name__ == '__main__':
    trainval_percent = 0.2
    train_percent = 0.8
    # path of img
    img_path = 'D:\\yolo\\coco\\VOC2007\\JPEGImages'
    # path of annotations
    anno_path = 'D:\\yolo\\coco\\VOC2007\\Annotations'
    # path of the annotation folder
    anno_folder = 'D:\\yolo\\coco\\annotations'
    # path of the images folder
    img_folder = 'D:\\yolo\\coco\\data'

    folder_name = ['trainset', 'valset', 'testset']

    for name in folder_name:
        img_folder_path = os.path.join(img_folder, '%s' % name)

        if not os.path.exists(img_folder_path):
            os.makedirs(img_folder_path)
            print("new a folder named " + str(name) + 'at the path of ' + img_folder_path)

        anno_folder_path = os.path.join(anno_folder, '%s' % name)

        if not os.path.exists(anno_folder_path):
            os.makedirs(anno_folder_path)
            print("new a folder named " + str(name) + 'at the path of ' + anno_folder_path)

    # give the img list
    total_imgs = os.listdir(img_path)

    num = len(total_imgs)
    list = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)

    for i in list:
        name = total_imgs[i][:-4]
        if i in trainval:
            if i in train:
                move_path(name, 'testset')
            else:
                move_path(name, 'valset')
        else:
            move_path(name, 'trainset')
