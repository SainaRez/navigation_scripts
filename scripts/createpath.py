#!/usr/bin/env python

import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped,Vector3, Pose
import tf
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Transform
from tf2_msgs.msg import TFMessage
from visualization_msgs.msg import Marker
from std_msgs.msg import Header, ColorRGBA

path = Path()
transform = Transform()
count = 0

def create_markers(msg):
    global count
    marker = Marker()

    marker.type = Marker.SPHERE
    marker.id = 0
    marker.lifetime = rospy.Duration(1000)
    marker.pose = msg.pose
    marker.scale = Vector3(0.009, 0.009, 0.009)
    marker.header = Header(frame_id='world')
    marker.color = ColorRGBA(5.0, 2.0, 0.0, 0.8)

    count = count + 1
    marker.id = count
    marker_publisher.publish(marker)


def callback(data):  
    global path
    pose = PoseStamped()
    pose.header = data.header
    pose.pose = data.pose
    path.header = pose.header
    path.poses.append(pose)
    pub.publish(path)

def world_broadcaster(msg):
    global transform
    transform.translation.x = msg.transforms[0].transform.translation.x
    transform.translation.y = msg.transforms[0].transform.translation.y
    transform.translation.z = msg.transforms[0].transform.translation.z
    transform.rotation.x = msg.transforms[0].transform.rotation.x
    transform.rotation.y = msg.transforms[0].transform.rotation.y
    transform.rotation.z = msg.transforms[0].transform.rotation.z
    transform.rotation.w = msg.transforms[0].transform.rotation.w
    pub2.publish(transform)
    
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(1000.0)
    br.sendTransform((msg.transforms[0].transform.translation.x, msg.transforms[0].transform.translation.y, msg.transforms[0].transform.translation.z),
                     (msg.transforms[0].transform.rotation.x, msg.transforms[0].transform.rotation.y, msg.transforms[0].transform.rotation.z, msg.transforms[0].transform.rotation.w),
                     rospy.Time.now(),
                     "vins_world",
                     "world")


if __name__ == '__main__':
   # rospy.init_node('world_tf_broadcaster')
    # listener = tf.TransformListener()
    # (trans,rot) = listener.lookupTransform('/world', '/vins_world', rospy.Time(0))

    """ Publish a path message """
    # rospy.init_node('vicon_path_node', anonymous=True)
    # pub = rospy.Publisher("/JA01/vicon/path", Path, queue_size=1)
    # vicon_msg = PoseStamped()
    # vicon_msg = rospy.Subscriber("/JA01/world", PoseStamped, callback)

    """ Publish markers """
    rospy.init_node('vicon_path_node', anonymous=True)
    count = 0
    marker_publisher = rospy.Publisher('/JA01/vicon/markers', Marker, queue_size=5)
    vicon_msg = PoseStamped()
    vicon_msg = rospy.Subscriber("/JA01/world", PoseStamped, create_markers)
    rospy.sleep(0.5)

    # pub2 = rospy.Publisher("/tf/world", Transform, queue_size=1)
    # world_tf_msg = TFMessage()
    # world_tf_msg = rospy.Subscriber("/tf_static", TFMessage, world_broadcaster)
    
    rospy.spin()
    try:
        while not rospy.is_shutdown():  
            pass
    except rospy.ROSInterruptException:
        pass
