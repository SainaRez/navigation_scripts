import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
import math
import tf2_ros
import tf



if __name__ == '__main__':

    rospy.init_node('vins_pose_broadcaster', anonymous=True)
    listener = tf.TransformListener()

    # w_b_pose = rospy.Publisher('/camera_to_world_pose', PoseStamped, queue_size=1)
    
    # rate = rospy.Rate(20.0)
    # while not rospy.is_shutdown():
    #     try:
    #         (trans,rot) = listener.lookupTransform('/camera', '/world', rospy.Time(0))
    #     except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
    #         continue

    #     msg = PoseStamped()
        
    #     msg.header.stamp = rospy.Time.now()
    #     msg.header.frame_id = "world"
    #     msg.pose.position.x = trans[0]
    #     msg.pose.position.y = trans[1]
    #     msg.pose.position.z = trans[2]
    #     msg.pose.orientation.x = rot[0]
    #     msg.pose.orientation.y = rot[1]
    #     msg.pose.orientation.z = rot[2]
    #     msg.pose.orientation.w = rot[3]

    #     w_b_pose.publish(msg)
        
    #     rate.sleep()
    



    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    w_b_pose = rospy.Publisher('/camera_to_world_pose', PoseStamped, queue_size=1)
    rate = rospy.Rate(20.0)
    while not rospy.is_shutdown():
        try:
            transformObj = tfBuffer.lookup_transform('world', 'camera', rospy.Time())
            
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):

            rate.sleep()
            continue

        msg = PoseStamped()
        
        msg.header.stamp = transformObj.header.stamp
        msg.header.frame_id = "world"
        msg.pose.position.x = transformObj.transform.translation.x
        msg.pose.position.y = transformObj.transform.translation.y
        msg.pose.position.z = transformObj.transform.translation.z
        msg.pose.orientation.x = transformObj.transform.rotation.x
        msg.pose.orientation.y = transformObj.transform.rotation.y
        msg.pose.orientation.z = transformObj.transform.rotation.z
        msg.pose.orientation.w = transformObj.transform.rotation.w

        w_b_pose.publish(msg)
        rate.sleep()