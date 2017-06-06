#!/usr/bin/env python

import rospy
import message_filters
import cv2
import numpy as np
from sensor_msgs.msg import Image, CameraInfo
from std_msgs.msg import Empty
from cv_bridge import CvBridge, CvBridgeError

callback_id = 0
enabled = False
callbacks_per_trigger = 5
save_dir = "~/Desktop"
cv_bridge = CvBridge()
global_id = 0   
person_id = 0
pose_id = 0

def trigger_callback(data):
  global enabled
  global person_id
  global global_id
  enabled = True
  person_id = rospy.get_param("/person_id", 0)
  global_id = rospy.get_param("/global_id", 0)
  print("Triggered! person_id: ", person_id, " global_id: ", global_id)

def sensor_callback(rgb, depth, rgb_info, depth_info):
  global cv_bridge
  global enabled
  global callback_id
  global callbacks_per_trigger
  global global_id
  global person_id
  params = list()
  params.append(cv2.IMWRITE_PNG_COMPRESSION)
  params.append(1)
  rgb_image = cv_bridge.imgmsg_to_cv2(rgb, desired_encoding="passthrough")
  depth_image = cv_bridge.imgmsg_to_cv2(depth, desired_encoding="passthrough")
  if enabled:
    print (save_dir + "/" + str(person_id).zfill(3) + "_" + str(global_id).zfill(4) + "_rgb.png")
    cv2.imwrite(save_dir + "/" + str(person_id).zfill(3) + "_" + str(global_id).zfill(4) + "_rgb.png", rgb_image, params)
    cv2.imwrite(save_dir + "/" + str(person_id).zfill(3) + "_" + str(global_id).zfill(4) + "_depth.png", depth_image, params)
    np.savetxt(save_dir + "/" + str(person_id).zfill(3) + "_" + str(global_id).zfill(4) + "_rgb_info.txt", rgb_info.P, delimiter=',')
    np.savetxt(save_dir + "/" + str(person_id).zfill(3) + "_" + str(global_id).zfill(4) + "_depth_info.txt", depth_info.P, delimiter=',')
    print ("Saved in " + save_dir + "/" + str(person_id).zfill(3) + "_" + str(global_id).zfill(4), callback_id)
    global_id +=1
    callback_id += 1
    if callback_id == callbacks_per_trigger:
      callback_id = 0
      enabled = False
      rospy.set_param("/global_id", global_id)
  

def listener():
  global callbacks_per_trigger
  global save_dir
  global person_id
  global global_id
  callback_id = 0
  enabled = False
  rospy.init_node('save_topic')
  save_dir = rospy.get_param("/save_folder", "~/Desktop")
  trigger_topic = rospy.get_param("/trigger_topic_name", "/trigger")
  rgb_topic = rospy.get_param("/rgb_topic_name", "/rgb")
  depth_topic = rospy.get_param("/depth_topic_name", "/depth")
  rgb_info_topic = rospy.get_param("/rgb_info_topic_name", "/rgb_info")
  depth_info_topic = rospy.get_param("/depth_info_topic_name", "/depth_info")
  callbacks_per_trigger = rospy.get_param("/callbacks_to_save", 5)
  rgb_sub = message_filters.Subscriber("/rgb", Image)
  depth_sub = message_filters.Subscriber("/depth", Image)
  rgb_info_sub = message_filters.Subscriber("/rgb_info", CameraInfo)
  depth_info_sub = message_filters.Subscriber("/depth_info", CameraInfo)
  rospy.Subscriber(trigger_topic, Empty, trigger_callback)
  ts = message_filters.TimeSynchronizer([rgb_sub, depth_sub, rgb_info_sub, depth_info_sub], 10)
  ts.registerCallback(sensor_callback)
  rospy.spin()

if __name__ == '__main__':
  try:
    listener()
  except rospy.ROSInterruptException:
    pass