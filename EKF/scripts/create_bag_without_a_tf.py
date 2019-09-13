#!/usr/bin/env python

""" this script creates a new bag without certain tranforms """

import rosbag
from copy import deepcopy
from geometry_msgs.msg import Vector3, Quaternion
import tf2_ros
import tf2_msgs.msg
import tf

bagInName = '/home/swarm/dataset/vicon/aug_15_jackal_slow_2.bag'
bagIn = rosbag.Bag(bagInName)
bagOutName = '/home/swarm/dataset/vicon/ekf_aug_15_jackal_slow_2.bag'
bagOut = rosbag.Bag(bagOutName,'w')

with bagOut as outbag:
	for topic, msg, t in bagIn.read_messages():
		# print topic
		if topic == '/tf':
			new_msg = tf2_msgs.msg.TFMessage()
			for i,t_f in enumerate(msg.transforms): # go through each frame->frame tf within the msg.transforms
				if t_f.header.frame_id == "JA01" and t_f.child_frame_id == "JA01_base_link":
					continue
				elif t_f.header.frame_id == "JA01_mid_mount":
					continue
				else:
					new_msg.transforms.append(t_f)
			
			outbag.write(topic, new_msg, t)			

		else:
			new_msg = deepcopy(msg)
			outbag.write(topic, new_msg, t)

bagIn.close()
bagOut.close()