#!/usr/bin/env python

import rospy
import tf
import geometry_msgs.msg
import numpy
import tf2_ros
    

if __name__ == "__main__":

    ######################### tf2_ros #######################

    rospy.init_node('vins_to_world_tf_publisher')
    
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            tf_camera_vins = tfBuffer.lookup_transform('camera', 'vins_world', rospy.Time())
            break
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            #tf_camera_world = tfBuffer.lookup_transform('camera_d435i_infra1_optical_frame', 'world', rospy.Time())
            tf_camera_world = tfBuffer.lookup_transform('JA01', 'world', rospy.Time())
            break
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rate.sleep()
            continue

    broadcaster = tf2_ros.StaticTransformBroadcaster()
    tf_vins_world = geometry_msgs.msg.TransformStamped()

    # Get transformation matrix for tf_camera_vins
    trans1_v3 = tf_camera_vins.transform.translation
    rot1_v3 = tf_camera_vins.transform.rotation
    
    trans1 = [trans1_v3.x, trans1_v3.y, trans1_v3.z]
    rot1 = [rot1_v3.x, rot1_v3.y, rot1_v3.z, rot1_v3.w]

    trans1_mat = tf.transformations.translation_matrix(trans1)
    rot1_mat = tf.transformations.quaternion_matrix(rot1)

    mat1 = numpy.dot(trans1_mat, rot1_mat)
    print "mat1", mat1

    # Get transformation matrix for tf_camera_world
    trans2_v3 = tf_camera_world.transform.translation
    rot2_v3 = tf_camera_world.transform.rotation

    trans2 = [trans2_v3.x, trans2_v3.y, trans2_v3.z]
    rot2 = [rot2_v3.x, rot2_v3.y, rot2_v3.z, rot2_v3.w]

    trans2_mat = tf.transformations.translation_matrix(trans2)
    rot2_mat = tf.transformations.quaternion_matrix(rot2)
    
    mat2 = numpy.dot(trans2_mat, rot2_mat)
    print "mat2", mat2

    # Get the translation and quaternion components for tf_vins_world
    mat3_not_inv = numpy.dot(mat1, mat2)
    mat3 = numpy.linalg.inv(mat3_not_inv)
    trans3 = tf.transformations.translation_from_matrix(mat3)
    rot3 = tf.transformations.quaternion_from_matrix(mat3)
    print "trans3, rot3 ", trans3, rot3

    # Create the transform message and send it
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


    ################## tf ###################
    
    # rospy.init_node('vins_to_world_tf_publisher')
    # listener = tf.TransformListener()

    # rate = rospy.Rate(10.0)
    # while not rospy.is_shutdown():
    #     print "entered while loop 1"
    #     try:
    #         print "try 1"
    #         (trans1, rot1) = listener.lookupTransform('camera', 'vins_world', rospy.Time())
    #         break
    #     except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
    #         print "exception 1"
    #         continue
    #         rate.sleep()
    
    # while not rospy.is_shutdown():
    #     print "entered while loop 2"
    #     try:
    #         print "try 2"
    #         (trans2, rot2) = listener.lookupTransform('camera_d435i_infra1_optical_frame', 'world', rospy.Time())
    #         break
    #     except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
    #         print "exception 2"
    #         continue
    #         rate.sleep()


    # trans1_mat = tf.transformations.translation_matrix(trans1)
    # rot1_mat   = tf.transformations.quaternion_matrix(rot1)
    # mat1 = numpy.dot(trans1_mat, rot1_mat)
    # print "mat1: ", mat1

    # trans2_mat = tf.transformations.translation_matrix(trans2)
    # rot2_mat    = tf.transformations.quaternion_matrix(rot2)
    # mat2 = numpy.dot(trans2_mat, rot2_mat)
    # print "mat2: ", mat2

    # inv_mat2 = numpy.linalg.inv(mat2)
    # mat3 = numpy.dot(mat1, inv_mat2)
    # print "mat3: ", mat3
    # trans3 = tf.transformations.translation_from_matrix(mat3)
    # rot3 = tf.transformations.quaternion_from_matrix(mat3)
    # print "trans3, rot3 ", trans3, rot3

    # broadcaster = tf2_ros.StaticTransformBroadcaster()
    # tf_vins_world = geometry_msgs.msg.TransformStamped()
    
    
    # br = tf.TransformBroadcaster()
    # #tf_vins_world = geometry_msgs.msg.TransformStamped()

    # tf_vins_world.header.stamp = rospy.Time.now()
    # tf_vins_world.header.frame_id = "world"
    # tf_vins_world.child_frame_id = "vins_world"

    # tf_vins_world.transform.translation.x = trans3[0]
    # tf_vins_world.transform.translation.y = trans3[1]
    # tf_vins_world.transform.translation.z = trans3[2]
    # tf_vins_world.transform.rotation.x = rot3[0]
    # tf_vins_world.transform.rotation.y = rot3[1]
    # tf_vins_world.transform.rotation.z = rot3[2]
    # tf_vins_world.transform.rotation.w = rot3[3]

    # #broadcaster.sendTransform(tf_vins_world)
    # br.sendTransformMessage(tf_vins_world)
    # #br.sendTransform(trans3,rot3,t,"target","source")
    # rospy.spin()
