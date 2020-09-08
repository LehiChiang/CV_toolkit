import os

# 生成testset，trainset，valset文件夹的文件目录
# 目录文件格式为txt，每个目录文件的一行对应着文件夹中的一个文件

ftest = open('D:\\yolo\\coco\\annotations\\testset.txt', 'w')
ftrain = open('D:\\yolo\\coco\\annotations\\trainset.txt', 'w')
fval = open('D:\\yolo\\coco\\annotations\\valset.txt', 'w')

testset = os.listdir('D:\\yolo\\coco\\annotations\\testset')
for name in testset:
    name = name + '\n'
    ftest.write(name)
ftest.close()

trainset = os.listdir('D:\\yolo\\coco\\annotations\\trainset')
for name in trainset:
    name = name + '\n'
    ftrain.write(name)
ftrain.close()

valset = os.listdir('D:\\yolo\\coco\\annotations\\valset')
for name in valset:
    name = name + '\n'
    fval.write(name)
fval.close()