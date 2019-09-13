#!/usr/bin/env python

""" this script extracts images from a rosbag file """
""" Modified the file at: https://gist.github.com/wngreene/835cda68ddd9c5416defce876a4d7dd9 """

import os
import argparse
import cv2
import rosbag
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage
import numpy as np
from scipy.ndimage import filters


def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")

def main():
    """
    Extract a folder of images from a rosbag.
    """
    parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("output_dir", help="Output directory.")
    parser.add_argument("image_topic_0", help="Image topic 0.")
    parser.add_argument("image_topic_1", help="Image topic 1.")
    parser.add_argument("image_topic_2", help="Image topic 2.")

    args = parser.parse_args()

    print "Extract images from %s on topic %s and %s and %s into %s" % (args.bag_file,
                                                          args.image_topic_0, args.image_topic_1, args.image_topic_2, args.output_dir)
    f = open("/home/swarm/MultiCol-SLAM/data/jackal_data/images_and_timestamps.txt","w+")
    print "made timestamp file"

    bag = rosbag.Bag(args.bag_file, "r")

    #bridge = CvBridge()
  
    count = 0
    for topic, msg, t in bag.read_messages(topics=[args.image_topic_0]):

        #### direct conversion to CV2 ####
        np_arr = np.fromstring(msg.data, np.uint8)
        #image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) # OpenCV >= 3.0:
        gray_img = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)


        #cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")

        path_0 = args.output_dir + '/cam0'

        cv2.imwrite(os.path.join(path_0, "img%06i.png" % count), gray_img)
        print "Wrote image %i" % count
        
        count += 1

    count = 0
    for topic, msg, t in bag.read_messages(topics=[args.image_topic_1]):
        
        np_arr = np.fromstring(msg.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) # OpenCV >= 3.0:
        gray_img = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)


        #cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")

        path_1 = args.output_dir + '/cam1'
        cv2.imwrite(os.path.join(path_1, "img%06i.png" % count), gray_img)
        print "Wrote image %i" % count
       
        count += 1

    count = 0
    for topic, msg, t in bag.read_messages(topics=[args.image_topic_2]):
        
        np_arr = np.fromstring(msg.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) # OpenCV >= 3.0:
        gray_img = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

        #cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")

        path_2 = args.output_dir + '/cam2'
        image_name = "img%06i.png" % count
        cv2.imwrite(os.path.join(path_2, "img%06i.png" % count), gray_img)
        print "Wrote image %i" % count

        time = msg.header.stamp
        seconds = time.to_sec()
        
        f.write("%f" % seconds)
        f.write(" " + "imgs/cam0/" + image_name + " " + "imgs/cam1/" + image_name + " " + "imgs/cam2/" + image_name + "\n")
        count += 1


    bag.close()
    f.close() 

    return

if __name__ == '__main__':
    main()