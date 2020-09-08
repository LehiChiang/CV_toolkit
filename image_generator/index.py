from keras.preprocessing.image import ImageDataGenerator
import os

path = os.getcwd()+'/imgsrc/'
dis_path = os.getcwd()+'/output/'

data_generator = ImageDataGenerator(
    rotation_range=20,
    rescale=1./255,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

gen = data_generator.flow_from_directory(
    path,
    batch_size=1,
    target_size=(534, 800),
    save_to_dir=dis_path,
    save_prefix='convert',
    save_format='jpg')

if __name__ == '__main__':
    if not os.path.exists(path):
        os.makedirs(path)

    if not os.path.exists(dis_path):
        os.makedirs(dis_path)

    num = input('Input the number of pics you want to generate : ')
    for i in range(int(num)):
        gen.next()
        print('Processing the %d th picture....' % (i+1))
    print('All pictures processed!')
