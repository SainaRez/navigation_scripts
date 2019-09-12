import rospy
import message_filters
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu

count1 = 0
count2 = 0
count3 = 0

def vins_callback(vins):
    global count1
    print "vins"
    print count1 
    print vins.header.stamp
    count1 = count1 + 1
def odom_callback(odom):
    print "odom"
    global count2
    print count2
    print odom.header.stamp
    count2 = count2 + 1
def imu_callback(imu):
    global count3
    print "imu"
    print count3
    print imu.header.stamp
    count3 = count3 + 1


def callback(vins, odom, imu):
    vins_publisher.publish(vins)
    odom_publisher.publish(odom)
    imu_publisher.publish(imu)

if __name__ == '__main__':

    rospy.init_node('sync_node', anonymous=True)
    vins_publisher = rospy.Publisher('/vins_estimator/odometry/synced', Odometry, queue_size=5)
    odom_publisher = rospy.Publisher('/JA01/jackal_velocity_controller/odom/synced', Odometry, queue_size=5)
    imu_publisher = rospy.Publisher('/camera_d435i/imu/synced', Imu, queue_size=5)
    
    vins_msg = Odometry()
    odom_msg = Odometry()
    imu_msg = Imu()
    vins_msg = rospy.Subscriber("/vins_estimator/odometry", Odometry, vins_callback)
    odom_msg = rospy.Subscriber("/JA01/jackal_velocity_controller/odom", Odometry, odom_callback)
    imu_msg = rospy.Subscriber("/camera_d435i/imu", Imu, imu_callback)
    rospy.spin()


    # vins_sub = message_filters.Subscriber('/vins_estimator/odometry', Odometry)
    # odom_sub = message_filters.Subscriber('/JA01/jackal_velocity_controller/odom', Odometry)
    # imu_sub = message_filters.Subscriber('/camera_d435i/imu', Imu)

    # ats = message_filters.ApproximateTimeSynchronizer([vins_sub, odom_sub, imu_sub], queue_size=5, slop=0.1)
    # ats.registerCallback(callback)
    # rospy.spin()