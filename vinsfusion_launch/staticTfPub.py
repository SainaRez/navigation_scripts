#!usr/bin/env python

import rospy
import tf2_ros
import geometry_msgs.msg
    

if __name__ == "__main__":
    
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            trans = tfBuffer.lookup_transform('vins_world', 'camera', rospy.Time())
            break
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            continue
            rate.sleep()


    rospy.init_node('tf2_listener')
    broadcaster = tf2_ros.StaticTransformBroadcaster()
    static_transformStamped = geometry_msgs.msg.TransformStamped()

    static_transformStamped.header.stamp = rospy.Time.now()
    static_transformStamped.header.frame_id = "world"
    static_transformStamped.child_frame_id = "vins_world"
    static_transformStamped.transform.translation = trans.transform.translation
    static_transformStamped.transform.rotation = trans.transform.rotation

    broadcaster.sendTransform(static_transformStamped)
    rospy.spin()

