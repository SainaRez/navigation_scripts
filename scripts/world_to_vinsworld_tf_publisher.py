#!/usr/bin/env python

""" this script calculates the transform between world and vins world at robot's initial state and publishes a static transform publisher """

import rospy
import tf
import geometry_msgs.msg
import numpy
import tf2_ros
    

if __name__ == "__main__":

    rospy.init_node('vins_to_world_tf_publisher')
    
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    # Lookup T_v_c and T_c_w (T_vins_camera and T_camera_world)
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            tf_camera_vins = tfBuffer.lookup_transform('vins_world', 'camera', rospy.Time())
            break
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            tf_camera_world = tfBuffer.lookup_transform('camera_d435i_infra1_optical_frame', 'world', rospy.Time())
            break
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue

    broadcaster = tf2_ros.StaticTransformBroadcaster()
    tf_vins_world = geometry_msgs.msg.TransformStamped()

    # Get tranformation matrix T_v_c
    trans1_v3 = tf_camera_vins.transform.translation
    rot1_v3 = tf_camera_vins.transform.rotation
    trans1 = [trans1_v3.x, trans1_v3.y, trans1_v3.z]
    rot1 = [rot1_v3.x, rot1_v3.y, rot1_v3.z, rot1_v3.w]

    trans1_mat = tf.transformations.translation_matrix(trans1)
    rot1_mat = tf.transformations.quaternion_matrix(rot1)

    mat1 = numpy.dot(trans1_mat, rot1_mat)
    euler1 = tf.transformations.euler_from_quaternion(rot1)

    print "euler1: ", euler1
    print "mat1", mat1

    # Get transformation matrix T_c_w
    trans2_v3 = tf_camera_world.transform.translation
    rot2_v3 = tf_camera_world.transform.rotation

    trans2 = [trans2_v3.x, trans2_v3.y, trans2_v3.z]
    rot2 = [rot2_v3.x, rot2_v3.y, rot2_v3.z, rot2_v3.w]

    trans2_mat = tf.transformations.translation_matrix(trans2)
    rot2_mat = tf.transformations.quaternion_matrix(rot2)
    
    mat2 = numpy.dot(trans2_mat, rot2_mat)
    euler2 = tf.transformations.euler_from_quaternion(rot2)
    print "euler2: ", euler2
    print "mat2", mat2

    # Calculate T_w_v 
    # T_v_c . T_c_w = T_v_w
    # T_w_v = (T_v_w)*(-1)
    mat3_vins_world = numpy.dot(mat1, mat2)
    mat3_world_vins = numpy.linalg.inv(mat3_vins_world)
    
    trans3 = tf.transformations.translation_from_matrix(mat3_world_vins)
    rot3 = tf.transformations.quaternion_from_matrix(mat3_world_vins)
    print 'mat3_world_vins', mat3_world_vins
    print "trans3, rot3 ", trans3, rot3
    
    euler3 = tf.transformations.euler_from_quaternion(rot3)
    print "euler3: ", euler3

    # Create the transform message for world and vins_world and broadcast it
    tf_vins_world.header.stamp = rospy.Time.now()
    tf_vins_world.header.frame_id = "world"
    tf_vins_world.child_frame_id = "vins_world"

    tf_vins_world.transform.translation.x = trans3[0]
    tf_vins_world.transform.translation.y = trans3[1]
    tf_vins_world.transform.translation.z = trans3[2]
    tf_vins_world.transform.rotation.x = rot3[0]
    tf_vins_world.transform.rotation.y = rot3[1]
    tf_vins_world.transform.rotation.z = rot3[2]
    tf_vins_world.transform.rotation.w = rot3[3]

    broadcaster.sendTransform(tf_vins_world)
    rospy.spin()
