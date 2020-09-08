# 目标检测/图像分割数据集工具包



## How to use?

将PASCAL  VOC标记文件`xml`转化为COCO的`json`文件格式：

1. 安装所需要的包

```python
pip install lxml
```

2. 将VOC数据集预先分成训练集，验证集和测试集

```
python data_split.py
```

3. 运行命令

```python
python voc2coco.py xmllist.txt Annotations output.json
```

`xmllist.txt`是`xml`文件夹的目录文件，使用`gtxt.py`生成

```python
python gtxt.py
```

`Annotations`为`xml`文件夹路径

`output.json`是转换的COCO格式的数据集标记文件



## 参考链接

> 如何将VOC XML文件转化成COCO数据格式 https://www.cnblogs.com/marsggbo/p/11152462.html

> Tony607voc2coco https://github.com/Tony607/voc2coco