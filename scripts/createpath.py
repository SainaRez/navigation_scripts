#!/usr/bin/env python


""" this script subscribes to the vicon topic and creates markers (or path messages) to visualize object's trajectory in vicon """

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
vcount = 0


""" callback function for marker messages """
def create_markers(msg):
    global count
    marker = Marker()

    marker.type = Marker.SPHERE
    marker.id = 0
    marker.lifetime = rospy.Duration(1000)
    marker.pose = msg.pose
    marker.scale = Vector3(0.02, 0.02, 0.02)
    marker.header = Header(frame_id='world')
    marker.color = ColorRGBA(5.0, 2.0, 0.0, 0.8)

    count = count + 1
    marker.id = count
    # publish per 10 messages
    if count%10 == 0: 
        marker_publisher.publish(marker)


""" callback function for path messages """
def create_path(data):  
    global path
    pose = PoseStamped()
    pose.header = data.header
    pose.pose = data.pose
    path.header = pose.header
    path.poses.append(pose)
    pub.publish(path)


if __name__ == '__main__':
    
    """ publish path messages """
    # rospy.init_node('vicon_path_node', anonymous=True)
    # pub = rospy.Publisher("/JA01/vicon/path", Path, queue_size=1)
    # vicon_msg = PoseStamped()
    # vicon_msg = rospy.Subscriber("/JA01/world", PoseStamped, create_path)

    """ publish markers """
    rospy.init_node('vicon_path_node', anonymous=True)
    count = 0
    marker_publisher = rospy.Publisher('/JA01/vicon/markers', Marker, queue_size=5)
    vicon_msg = PoseStamped()
    vicon_msg = rospy.Subscriber("/JA01/world", PoseStamped, create_markers)
    rospy.sleep(0.5)
    
    rospy.spin()