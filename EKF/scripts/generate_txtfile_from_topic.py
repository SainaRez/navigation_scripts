#!usr/bin/env python

""" this script generates a textfile of the message data from a specific topic. The current flags include camera, Camera_imu and vicon """

import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
import math
import tf2_ros
import geometry_msgs.msg
import turtlesim.srv



def vins_callback_camera_imu(data):  
    vins_file.write('{0}.{1} {2} {3} {4} {5} {6} {7} {8}\n'.format(data.header.stamp.secs, data.header.stamp.nsecs, data.pose.position.x, data.pose.position.y, data.pose.position.z, data.pose.orientation.x, data.pose.orientation.y, data.pose.orientation.z, data.pose.orientation.w))

def vins_callback_camera(data):  
    vins_file_camera.write('{0}.{1} {2} {3} {4} {5} {6} {7} {8}\n'.format(data.header.stamp.secs, data.header.stamp.nsecs, data.pose.position.x, data.pose.position.y, data.pose.position.z, data.pose.orientation.x, data.pose.orientation.y, data.pose.orientation.z, data.pose.orientation.w))

def vicon_callback(data):
    vicon_file.write('{0}.{1} {2} {3} {4} {5} {6} {7} {8}\n'.format(data.header.stamp.secs, data.header.stamp.nsecs, data.pose.position.x, data.pose.position.y, data.pose.position.z, data.pose.orientation.x, data.pose.orientation.y, data.pose.orientation.z, data.pose.orientation.w))


if __name__ == '__main__':

    #flag = "VINS_FUSION_CAMERA"
    #flag = "VINS_FUSION_CAMERA_IMU"
    #flag = "VICON"

    if flag == "VINS_FUSION_CAMERA":
        vins_file_camera = open('d435i_slowermotionis_2_camera.txt','w') 
        rospy.init_node('vins_evo_data_node', anonymous=True)
        vins_cam_msg = PoseStamped()
        vins_cam_msg = rospy.Subscriber("/camera_to_world_pose", PoseStamped, vins_callback_camera)
        rospy.spin()
        print "callback done"
        vins_file_camera.close


    if flag == "VINS_FUSION_CAMERA_IMU":
        vins_file_camera_imu = open('d435i_slowermotionis_2_cameraimu.txt','w') 
        rospy.init_node('vins_evo_data_node', anonymous=True)
        vins_camimu_msg = PoseStamped()
        vins_camimu_msg = rospy.Subscriber("/camera_to_world_pose", PoseStamped, vins_callback_camera_imu)
        rospy.spin()
        print "callback done"
        vins_file_camera_imu.close


    elif flag == "VICON":
        vicon_file = open('vicon_slow_2.txt','w') 
        rospy.init_node('vicon_evo_path_node', anonymous=True)
        vicon_msg = PoseStamped()
        vicon_msg = rospy.Subscriber("/JA01/world", PoseStamped, vicon_callback)
        vicon_file.close
    
        rospy.spin()
    