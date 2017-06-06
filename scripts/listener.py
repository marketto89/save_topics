#!/usr/bin/env python

import rospy
import message_filters
from sensor_msgs.msg import Image, CameraInfo
from std_msgs.msg import Empty

callback_id = 0
enabled = False

def trigger_callback(data):
  global enabled
  enabled = True
  print("Triggered! ")

def sensor_callback(rgb, depth, rgb_info, depth_info):
  global enabled
  global callback_id
  if enabled:
    print ("Yeah", callback_id)
    callback_id += 1
    if callback_id == 5:
      callback_id = 0
      enabled = False

def listener():
  callback_id = 0
  enabled = False
  rospy.init_node('save_topic')
  trigger_topic = rospy.get_param("/trigger_topic_name", "/trigger")
  rgb_topic = rospy.get_param("/rgb_topic_name", "/rgb")
  depth_topic = rospy.get_param("/depth_topic_name", "/depth")
  rgb_info_topic = rospy.get_param("/rgb_info_topic_name", "/rgb_info")
  depth_info_topic = rospy.get_param("/depth_info_topic_name", "/depth_info")
  rgb_sub = message_filters.Subscriber(rgb_topic, Image)
  depth_sub = message_filters.Subscriber(depth_topic, Image)
  rgb_info_sub = message_filters.Subscriber(rgb_info_topic, CameraInfo)
  depth_info_sub = message_filters.Subscriber(depth_info_topic, CameraInfo)
  rospy.Subscriber(trigger_topic, Empty, trigger_callback)
  ts = message_filters.TimeSynchronizer([rgb_sub, depth_sub, rgb_info_sub, depth_info_sub], 10)
  ts.registerCallback(sensor_callback)
  rospy.spin()

if __name__ == '__main__':
  try:
    listener()
  except rospy.ROSInterruptException:
    pass