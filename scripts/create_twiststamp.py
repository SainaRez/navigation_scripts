#!/usr/bin/env python

import rospy
from nav_msgs.msg import Path, Odometry
from geometry_msgs.msg import PoseStamped,Vector3, Pose, Transform, TransformStamped, TwistStamped
import tf
from tf2_msgs.msg import TFMessage
from visualization_msgs.msg import Marker
from std_msgs.msg import Header, ColorRGBA


def callback(msg):  
    t = TwistStamped()
    t.twist.linear = msg.twist.twist.linear
    t.twist.angular = msg.twist.twist.angular
    t.header = msg.header
    pub.publish(t)


if __name__ == '__main__':

    """ Publish TwistStamp Message """

    rospy.init_node('vins_twist_node', anonymous=True)
    pub = rospy.Publisher("/vins/twist", TwistStamped, queue_size=1)
    vins_twist_msg = Odometry()
    vins_twist_msg = rospy.Subscriber("/vins_estimator/odometry", Odometry, callback)
    rospy.sleep(0.5)

    rospy.spin()
    try:
        while not rospy.is_shutdown():  
            pass
    except rospy.ROSInterruptException:
        pass
