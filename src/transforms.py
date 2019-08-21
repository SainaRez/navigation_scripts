#!usr/bin/env python

import rospy
import roslib
import math
import tf
import geometry_msgs.msg

if __name__ == '__main__':

    vicon_file = open('vicon_transforms.txt','w')
    vins_file = open('vins_transforms.txt','w')
    
    rospy.init_node('jackal_tf_listener')

    vicon_listener = tf.TransformListener()
    vins_listener = tf.TransformListener()

    
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:

            (vicon_trans,vicon_rot) = vicon_listener.lookupTransform('/JA01', '/world', rospy.Time(0))
            print(vicon_trans, vicon_rot)

            (vins_trans,vins_rot) = vins_listener.lookupTransform('/camera', '/vins_world', rospy.Time(0))
            print(vins_trans, vins_rot)

            vicon_file.write('{0} {1} {2} {3} {4} {5} {6}\n'.format(vicon_trans[0], vicon_trans[1], vicon_trans[2], vicon_rot[0], vicon_rot[1], vicon_rot[2], vicon_rot[3]))
            vins_file.write('{0} {1} {2} {3} {4} {5} {6}\n'.format(vins_trans[0], vins_trans[1], vins_trans[2], vins_rot[0], vins_rot[1], vins_rot[2], vins_rot[3]))

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        
        rate.sleep()

   
     