#coding=utf-8

import tensorflow as tf
import numpy as np
import os
import matplotlib.pyplot as plt

img_width = 208
img_height = 208


def get_files(path):
    cats =[]
    label_cats = []
    dogs = []
    label_dogs = []

    for img_file in os.listdir(path):

        name = img_file.split('.')
        if name[0]=="cat":
            cats.append(path+img_file)
            label_cats.append(0)
        else:
            dogs.append(path+img_file)
            label_dogs.append(1)

    img_list = np.hstack((cats, dogs))
    label_list = np.hstack((label_cats, label_dogs))

    temp = np.array([img_list, label_list])
    temp = temp.transpose()
    np.random.shuffle(temp)

    img_list = list(temp[:, 0])
    label_list = list(temp[:, 1])
    label_list = [int(i) for i in label_list]

    return img_list, label_list


def get_batch(image, label, image_width, image_height, batch_size, capacity):
    image = tf.cast(image, tf.string)
    label = tf.cast(label, tf.int32)

    input_queue = tf.train.slice_input_producer([image, label])

    label = input_queue[1]
    image_contents = tf.read_file(input_queue[0])
    image = tf.image.decode_jpeg(image_contents, channels=3)

    image = tf.image.resize_image_with_crop_or_pad(image, image_width, image_height)
    image = tf.image.per_image_standardization(image)
    image_batch, label_batch = tf.train.batch([image, label],
                                              batch_size,
                                              num_threads=8,
                                              capacity=capacity)

    label_batch = tf.reshape(label_batch, [batch_size])
    image_batch = tf.cast(image_batch, tf.float32)

    return image_batch, label_batch


def show_img():
    BATCH_SIZE = 10
    CAPACITY = 256

    train_dir = "/Users/yuwhuawang/tensorflow/catsordogs/train/"

    img_list, label_list = get_files(train_dir)
    img_batch, label_batch = get_batch(img_list, label_list, img_width, img_height, BATCH_SIZE, CAPACITY)

    with tf.Session() as sess:
        i = 0
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)

        try:
            while not coord.should_stop() and i < 5:
                img, label = sess.run([img_batch, label_batch])
                for j in np.arange(BATCH_SIZE):
                    print "label:{}".format(label[j])
                    plt.imshow(img[j,:,:,:])
                    plt.show()
                i+=1

        except tf.errors.OutOfRangeError:
            print ("done!")
        finally:
            coord.request_stop()
        coord.join(threads)


if __name__ == '__main__':
    show_img()