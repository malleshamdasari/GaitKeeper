import os
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from utils import *

def Layer(X, num_output, initializer, keep_prob, W_name, b_name, activation = True):

    _, num_feature = X.shape

    W = tf.get_variable(W_name, shape = [num_feature, num_output], dtype = tf.float32, initializer = initializer)
    b = tf.Variable(tf.random_normal([num_output]), name = b_name)
    L = tf.matmul(X, W) + b

    if activation:
        L = tf.nn.relu(L)
        L = tf.nn.dropout(L, keep_prob = keep_prob)

    return L, W, b

class model():

    def __init__(self, initial_learning_rate, num_steps, model_save_path, num_col):
        self.initial_learning_rate = initial_learning_rate
        self.num_steps = num_steps
        self.model_save_path = model_save_path
        self.num_col = num_col
    def build(self):

        self.keep_prob = tf.placeholder(tf.float32, name = 'keep_prob')
        self.initializer = tf.contrib.layers.xavier_initializer()

        self.X = tf.placeholder(tf.float32, shape = [None, self.num_col], name = 'X')
        self.Y = tf.placeholder(tf.float32, shape = [None, 1], name = 'Y')

        l1_dim = 2000
        l2_dim = 2000
        l3_dim = 500
        output_dim = 1

        with tf.variable_scope('Layer1') as scope:
            self.L1, _, _ = Layer(self.X, l1_dim, self.initializer, self.keep_prob, 'W1', 'b1')

        with tf.variable_scope('Layer2') as scope:
            self.L2, _, _ = Layer(self.L1, l2_dim, self.initializer, self.keep_prob, 'W2', 'b2')

        with tf.variable_scope('Layer3') as scope:
            self.L3, _, _ = Layer(self.L2, l3_dim, self.initializer, self.keep_prob, 'W3', 'b3')

        with tf.variable_scope('Output') as scope:
            self.logits, _, _ = Layer(self.L3, output_dim, self.initializer, self.keep_prob, 'W', 'b', activation = False)

        self.cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels = self.Y, logits= self.logits))
        self.global_step = tf.Variable(0)
        self.learning_rate = tf.train.exponential_decay(self.initial_learning_rate, self.global_step, 100, 0.9)

        self.optimizer = tf.train.AdamOptimizer(learning_rate = self.learning_rate).minimize(self.cost)
        self.confidence = tf.nn.sigmoid(self.logits, name = 'sigmoid')
        self.prediction = tf.round(self.confidence, name = 'prediction')
        self.correct_pred = tf.equal(self.prediction, self.Y)

        self.accuracy = tf.reduce_mean(tf.cast(self.correct_pred, tf.float32), name = 'accuracy')

    def train(self, train_x_data, train_y_data, keep_prob):

        saver = tf.train.Saver()
        if not os.path.exists(self.model_save_path):
            os.makedirs(self.model_save_path)

        self.sess = tf.Session()

        self.sess.run(tf.global_variables_initializer())

        for step in range(self.num_steps):

            c, a, _ = self.sess.run([self.cost, self.accuracy, self.optimizer], feed_dict = {self.X: train_x_data, self.Y: train_y_data, self.keep_prob: keep_prob})

            if step % 100 == 0:
                print('Num Iteration: {}, Cost: {}, Accuracy: {}'.format(step, c, a))

        saver.save(self.sess, save_path = os.path.join(self.model_save_path, 'nn'))

    def predict(self, test_x_data):

        sess = tf.Session()
        saver = tf.train.import_meta_graph('model/nn.meta')
        saver.restore(sess,tf.train.latest_checkpoint('model/./'))

        graph = tf.get_default_graph()
        X = graph.get_tensor_by_name("X:0")
        keep_prob = graph.get_tensor_by_name("keep_prob:0")

        feed_dict ={X: test_x_data, keep_prob: 1.0}

        op_to_restore = graph.get_tensor_by_name("sigmoid:0")

        return sess.run(op_to_restore, feed_dict)


    def acc(self, test_x_data, test_y_data):

        sess = tf.Session()
        saver = tf.train.import_meta_graph('model/nn.meta')
        saver.restore(sess, tf.train.latest_checkpoint('model/./'))

        graph = tf.get_default_graph()
        X = graph.get_tensor_by_name("X:0")
        Y = graph.get_tensor_by_name("Y:0")
        keep_prob = graph.get_tensor_by_name("keep_prob:0")

        feed_dict ={X:test_x_data, Y:test_y_data, keep_prob: 1.0}

        #Now, access the op that you want to run.
        op_to_restore = graph.get_tensor_by_name("accuracy:0")

        return sess.run(op_to_restore, feed_dict)


















'''
        ## import the graph from the file
        #imported_graph = tf.train.import_meta_graph('model/nn.meta')

        ## list all the tensors in the graph
        #for tensor in tf.get_default_graph().get_operations():
        #   print (tensor.name)

        with tf.Session() as sess:

            latest_checkpoint = tf.train.latest_checkpoint('model')
            meta_path = '%s.meta' % latest_checkpoint

            saver = tf.train.import_meta_graph(meta_path)
            saver.restore(sess, latest_checkpoint)

            X = tf.get_collection("X")[0]
            Y = tf.get_collection("Y")[0]
            keep_prob = tf.get_collection("keep_prob")[0]
            prediction = tf.get_collection("accuracy")[0]
            acc = sess.run(accuracy, feed_dict = {X: test_x_data, Y: test_y_data, keep_prob: 1.0})
        return acc
'''




'''
        X = graph.get_tensor_by_name("X:0")
        Y = graph.get_tensor_by_name("Y:0")
        keep_prob = graph.get_tensor_by_name("keep_prob:0")

        feed_dict ={X: test_x_data, Y: test_y_data, keep_prob: 1.0}

        #Now, access the op that you want to run.
        op_to_restore = graph.get_tensor_by_name("accuracy:0")
        return sess.run(op_to_restore, feed_dict)
        #acc = self.sess.run(self.accuracy, feed_dict = {self.X: test_x_data, self.Y: test_y_data, self.keep_prob: 1.0})
        #return acc
'''
























































#end.
