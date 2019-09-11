import rospy
import message_filters
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
import tf


def callback(msg):



if __name__ == '__main__':
    
    rospy.init_node('set_ekf_origin_node', anonymous=True)
    ekf_msg = Odometry()
    ekf_msg =  rospy.Subscriber("odometry/imu_encoders", Odometry, callback)

    listener = tf.TransformListener()
    listener.waitForTransform("/odom_ekf", "/JA01_base_link", rospy.Time(0), rospy.Duration(4.0))
    point = PointStamped()
    laser_point.header.frame_id = "base_link"
    laser_point.header.stamp =rospy.Time(0)
    laser_point.point.x=1.0
    laser_point.point.y=1.0
    laser_point.point.z=0.0
    p = listener.transformPoint("world", )