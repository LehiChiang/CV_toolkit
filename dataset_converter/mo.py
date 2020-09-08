import xml.etree.ElementTree as ET
import os

# 检测xml格式的文件中是否有缺失的属性
xml_dir = 'D:\\yolo\\coco\\annotations\\valset'
list_fp = os.listdir(xml_dir)
for line in list_fp:
    line = line.strip()
    xml_f = os.path.join(xml_dir, line)
    tree = ET.parse(xml_f)
    root = tree.getroot()
    path = root.findall('filename') # 这里缺失的属性是filename
    if not path:
        print(line, '文件信息不全！')
        filename = line.split('.')[0] + '.jpg'
        node = ET.Element('filename')
        node.text = filename
        root.append(node)
        tree.write(xml_f, encoding='utf-8', xml_declaration=True)

