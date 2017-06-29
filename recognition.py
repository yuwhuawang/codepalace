#coding:utf-8
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import input_data
import model


def get_one_image(img):

    img = Image.open(img)
    img.show()
    img = img.resize([208,208])
    img = np.array(img)
    return img

img_dir = '/Users/yuwhuawang/tensorflow/catsordogs/test/{}.jpg'.format(np.random.randint(1,12500))


def evaluate_one_image(img_dir):
    img_array = get_one_image(img_dir)

    with tf.Graph().as_default():
        batch_size = 1
        n_classes = 2

        img = tf.cast(img_array, tf.float32)
        img = tf.reshape(img, [1,208,208,3])
        logit = model.inference(img, batch_size, n_classes)
        logit = tf.nn.softmax(logit)
        x = tf.placeholder(tf.float32, shape=[208,208,3])

        logs_train_dir = '/Users/yuwhuawang/tensorflow/catsordogs/logs/train/'
        saver = tf.train.Saver()

        with tf.Session() as sess:
            ckpt = tf.train.get_checkpoint_state(logs_train_dir)
            if ckpt and ckpt.model_checkpoint_path:
                global_step = ckpt.model_checkpoint_path.split("/")[-1].split('-')[-1]
                saver.restore(sess, ckpt.model_checkpoint_path)
                print 'Loading success, global_step is {}'.format(global_step)
            else:
                print 'No checkpoint file found'

            prediction = sess.run(logit, feed_dict={x:img_array})
            max_index = np.argmax(prediction)
            if max_index == 0:
                print("This is a cat with possibility {:.6f}".format(float(prediction[:,0])))
            else:
                print("This is a dog with possibility {:.6f}".format(float(prediction[:,1])))


if __name__ == '__main__':
    evaluate_one_image(img_dir)



