#coding:utf-8

import os
import numpy as np
import tensorflow as tf
import input_data
import model

N_CLASSES = 2
IMG_W = 208
IMG_H = 208
BATCH_SIZE = 16
CAPACITY = 2000
MAX_STEP = 4000
LEARNING_RATE = 0.0001


def run_training():
    train_dir = "/Users/yuwhuawang/tensorflow/catsordogs/train/"
    logs_train_dir = "/Users/yuwhuawang/tensorflow/catsordogs/logs/train/"

    train, train_label = input_data.get_files(train_dir)

    train_batch, train_label_batch = input_data.get_batch(train,
                                                          train_label,
                                                          IMG_W,
                                                          IMG_H,
                                                          BATCH_SIZE,
                                                          CAPACITY)

    train_logits = model.inference(train_batch, BATCH_SIZE, N_CLASSES)
    train_loss = model.losses(train_logits, train_label_batch)
    train_op = model.training(train_loss, LEARNING_RATE)
    train_acc = model.evaluation(train_logits, train_label_batch)

    summary_op = tf.summary.merge_all()
    sess = tf.Session()
    train_writer = tf.summary.FileWriter(logs_train_dir, sess.graph)
    saver = tf.train.Saver()

    sess.run(tf.global_variables_initializer())
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess,coord)

    try:
        for step in np.arange(MAX_STEP):
            if coord.should_stop():
                break
            _, trn_loss, trn_acc = sess.run([train_op, train_loss, train_acc])

            if step % 50 == 0:
                print ("Step {}, train loss = {:.2f}, train accuracy = {:.2f}".format(step,trn_loss, trn_acc))
                summary_str = sess.run(summary_op)
                train_writer.add_summary(summary_str, step)

            if step % 2000 == 0 or (step + 1) == MAX_STEP:
                checkpoint_path = os.path.join(logs_train_dir, 'model.ckpt')
                saver.save(sess, checkpoint_path, global_step=step)

    except tf.errors.OutOfRangeError:
        print ('Done training --epoch limit reached')
    finally:
        coord.request_stop()

    coord.join(threads)
    sess.close()

if __name__ == '__main__':
    run_training()
