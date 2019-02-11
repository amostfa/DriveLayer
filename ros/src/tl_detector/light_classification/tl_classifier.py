from styx_msgs.msg import TrafficLight

import numpy as numpy
import tensorflow as tf

import os
import sys


class TLClassifier(object):
    def __init__(self):
        self.model = None
        self.tf_session = None
        self.model_path = None
        self.sim = True
        
        cwd = os.path.dirname(os.path.realpath(__file__))

        if self.sim is True:
            self.model_path = cwd + '/frozen_models/sim/'
        else:
            self.model_path = cwd + '/frozen_models/real/'

        self.config = tf.ConfigProto(log_device_placement=True)
        self.config.gpu_options.allow_growth = True
        self.config.gpu_options.per_process_gpu_memory_fraction = 0.3
        self.config.operation_timeout_in_ms = 50000
        self.tf_session = tf.Session(config=self.config)
        self.saver = tf.train.import_meta_graph(
            self.model_path + '/generator.ckpt.meta')
        self.saver.restore(
            self.tf_session, tf.train.latest_checkpoint(self.model_path))

        self.tf_graph = tf.get_default_graph()
        self.input_real = self.tf_graph.get_tensor_by_name("input_real:0")
        self.drop_rate = self.tf_graph.get_tensor_by_name("drop_rate:0")
        self.model = self.tf_graph.get_tensor_by_name("predict:0")

    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        re_scaled_image = self.scale(image.reshape(-1, 600, 800, 3))

        predict = [TrafficLight.UNKNOWN]
        if self.model is not None:
            predict = self.tf_session.run(self.model, feed_dict={
                self.input_real: re_scaled_image,
                self.drop_rate: 0.})

        return predict[0]

    def scale(self, x):
        x = ((x - x.min())/(255 - x.min()))
        min = -1
        max = 1
        x = x * (max - min) + min
        return x
