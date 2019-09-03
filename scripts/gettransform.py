#!usr/bin/env python

import rospy
import tf2_ros
import tf


if __name__ == "__main__":
    rospy.init_node('tf2_listener')
    vicon_file = open('tf_aug_15_jackal_fast_40.txt','w')
    
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    t = 'translation:'
    r = 'rotation:'
    b = 'vins_world to body'
    c = 'vins_world to camera'

    rate = rospy.Rate(10.0)
    last_b_stamp = rospy.Time(0,0)
    last_c_stamp = rospy.Time(0,0)
    while not rospy.is_shutdown():
        try:
            btrans = tfBuffer.lookup_transform('vins_world', 'body', rospy.Time())
            ctrans = tfBuffer.lookup_transform('vins_world', 'camera', rospy.Time())
            euler = tf.transformations.euler_from_quaternion([ctrans.transform.rotation.x, ctrans.transform.rotation.y, ctrans.transform.rotation.z, ctrans.transform.rotation.w])
            vicon_file.write('{0} {1}.{2}\n {3}\n {4}\n {5}\n {6}\n {7}\n {8}\n'.format(c, ctrans.header.stamp.secs, ctrans.header.stamp.nsecs, t, ctrans.transform.translation, r, euler[0], euler[1], euler[2]))
            current_b_stamp = rospy.Time(btrans.header.stamp.secs, btrans.header.stamp.nsecs)
            current_c_stamp = rospy.Time(ctrans.header.stamp.secs, ctrans.header.stamp.nsecs)
            # if current_b_stamp != last_b_stamp and current_c_stamp != last_c_stamp:
            #     last_b_stamp = current_b_stamp
            #     last_c_stamp = current_c_stamp
            #     vicon_file.write('{0} {1}.{2}\n {3}\n {4}\n {5}\n {6}\n'.format(b, btrans.header.stamp.secs, btrans.header.stamp.nsecs, t, btrans.transform.translation, r, btrans.transform.rotation))
            #     vicon_file.write('{0} {1}.{2}\n {3}\n {4}\n {5}\n {6}\n'.format(c, ctrans.header.stamp.secs, ctrans.header.stamp.nsecs, t, ctrans.transform.translation, r, ctrans.transform.rotation))
            #print "vins_world to body: ", "trans: ", btrans.transform.translation, "rot: ", btrans.transform.rotation
            #print "vins_world to camera: ", "trans: ", ctrans.transform.translation, "rot: ", ctrans.transform.rotation
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            continue
            rate.sleep()