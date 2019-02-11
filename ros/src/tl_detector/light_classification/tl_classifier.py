from styx_msgs.msg import TrafficLight

import numpy as numpy
import os
import sys
import tensorflow as tf


class TLClassifier(object):
    def __init__(self):
        self.img_h = 0
        self.img_w = 0
        self.img_d = 0

         

    def get_classification(self, image):
        """Determines the color of the traffic light in the image
            Using CIELUV colorspace
            REFERENCES: 
            https://ieeexplore.ieee.org/document/7960711/authors#authors
            http://cs.haifa.ac.il/hagit/courses/ist/Lectures/Demos/ColorApplet/me/infoluv.html
            https://github.com/asimonov/carla-brain/blob/master/ros/src/tl_detector/light_classification/tl_classifier.py
            
        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        self.img_h, self.img_w, self.img_d = image.shape

        # convert to LUV color space
        self.img_luv = cv2.cvtColor(image, cv2.COLOR_RGB2LUV)
        
        # get only L channel & trim the image in high and width
        trim_factor = 0.1 
        slef.l_ch = self.img_luv[int(trim_factor*self.img_h):int((1.0 - trim_factor)*self.img_h),int(trim_factor*self.img_w):int((1.0-trim_factor)*self.img_w),0]

        down_count = 0
        mid_count = 0
        top_count = 0

        color_count = {'RED': 0, 'YELLOW':0, 'GREEN': 0}
        
        # more info about the L channel: http://cs.haifa.ac.il/hagit/courses/ist/Lectures/Demos/ColorApplet/me/infoluv.html

        # divide the l channel hight to three ranges 
        hight, w = slef.l_ch.shape
        bottom  = int(hight / 3)
        middle  = int(hight - bottom)

        # count GREEN pixels - top third 
        # strat from top part -> GREEN 

        for i in range(middle, hight):
            for j in range(w):
                g += self.l_channel[i][j]
        color_count['GREEN'] = g

        # count yellow - in the middle region
        for i in range(bottom, middle):
            for j in range(w):
                y += self.l_channel[i][j]
        color_count['YELLOW'] = y

        # count RED - in the bottom region
        for i in range(bottom):
            for j in range(self.img_w):
                r += self.l_channel[i][j]
        count_result['RED'] = r

        light = max(count_result, key=lambda key:count_result[key])

        r = TrafficLight.UNKNOWN

        if light == 'GREEN':
            rospy.logdebug("tl_classifier result: Green") 
            r = TrafficLight.GREEN
        elif light == 'YELLOW':
            rospy.logdebug("tl_classifier result: Yellow") 
            r = TrafficLight.YELLOW
        elif light == 'RED':
            rospy.logdebug("tl_classifier result: Red") 
            r = TrafficLight.RED
        else:
            rospy.logdebug("tl_classifier result: unknow - ERROR!") 


        return r

