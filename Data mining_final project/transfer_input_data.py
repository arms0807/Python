import numpy as np
import os
import matplotlib.pyplot as plt
import skimage.io as io
import random
from skimage.transform import resize
from PIL import Image

def get_file(file_dir):
    '''
    Args:
        file_dir: file directory
    Returns:
        images: image directories, list, string
        lables: label, list, int
    '''

    if(os.path.exists(".DS_Store")):
        print("remove .DS_Store")
        os.remove(".DS_Store")

    images = []
    temp = []
    for root, sub_folders, files in os.walk(file_dir):
        #image directories
        for name in files:
            images.append(os.path.join(root, name))
        #get 10 sub-folder names
        for name in sub_folders:
            temp.append(os.path.join(root, name))

    # print("image ", images[:3])
    # print("temp ", temp[:3])
    labels = []
    for one_folder in temp:
        n_img = len(os.listdir(one_folder))
        letter = one_folder.split('/')[-1]

        if letter == 'A':
            labels = np.append(labels, n_img*[0])
        elif letter == 'B':
            labels = np.append(labels, n_img*[1])
        elif letter == 'C':
            labels = np.append(labels, n_img*[2])
        elif letter == 'D':
            labels = np.append(labels, n_img*[3])
        elif letter == 'E':
            labels = np.append(labels, n_img*[4])
        elif letter == 'F':
            labels = np.append(labels, n_img*[5])
        elif letter == 'G':
            labels = np.append(labels, n_img*[6])
        elif letter == 'H':
            labels = np.append(labels, n_img*[7])
        elif letter == 'I':
            labels = np.append(labels, n_img*[8])
        elif letter == 'J':
            labels = np.append(labels, n_img*[9])
        # print(len(labels))
        # print(labels)

    #shuffle for randomize
    temp = np.array([images, labels])
    temp = temp.transpose()
    np.random.shuffle(temp)
    # print(temp[:3])
    image_list = list(temp[:, 0])
    labels = list(temp[:, 1])
    labels = [int(float(i)) for i in labels]
    # print("label")
    # print(labels)
    #image_list.pop(0)
    #print(image_list[0])

    return image_list, labels

def convert_to_nparray(images, labels):
    '''
    Args:
        images: list of image directories, string type
        labels: list of labels, int type
        save_dir: the directory to save tfrecord file, e.g.: '/home/folder1/'
        name: the name of tfrecord file, string type, e.g.: 'train'

    Return:
        no return
    '''

    if len(images) != len(labels):
        print("NOT MATCH")
        print(len(images))
        print("\n")
        print(len(labels))

    print('\nTransform start......')
    i = 0
    j = 0
    data = []
    drop = []
    for i in np.arange(0, len(images)):
        try:
            image = io.imread(images[i], as_grey=True)
            image = resize(image, (28, 28))
            image = np.array(image)[:, :, np.newaxis]
            # print(image.shape)
            # print(image)
            data.append(image)
            labels[i] = int(labels[i])
        except IOError as e:
            drop.append(i)
            print('Could not read:', images[i])
            print('error: %s' %e)
            print('Skip it\n')
    print('Transform done!\n')

    return data, labels, drop

train_dir = '/Users/wengshiquan/Desktop/cs634/notMNIST_large/'

images_train, labels_train = get_file(train_dir)

train_image, train_label, drop = convert_to_nparray(images_train, labels_train)
# for i in drop:
#     train_label.pop(i)
# print(len(train_image), len(train_label)) 
# np.save("/Users/wengshiquan/Desktop/cs634/train/train_image.npy", train_image)
# np.save("/Users/wengshiquan/Desktop/cs634/train/train_label.npy", train_label)

# test_dir = '/Users/wengshiquan/Desktop/cs634/notMNIST_small/'
# images_test, labels_test = get_file(test_dir)
# test_image, test_label, drop = convert_to_nparray(images_test, labels_test)
# print(drop)
# for i in drop:
#     test_label.pop(i)
# print(len(test_image), len(test_label)) 

# np.save("/Users/wengshiquan/Desktop/cs634/test/test_image.npy", test_image)
# np.save("/Users/wengshiquan/Desktop/cs634/test/test_label.npy", test_label)
