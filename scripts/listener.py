#!/usr/bin/env python

import rospy
from std_msgs.msg import Empty

def callback(data):
  print("I heard ")
    
def listener():
  rospy.init_node('save_topic')
  trigger_topic = rospy.get_param("/trigger_topic_name", "/trigger")
  rospy.Subscriber(trigger_topic, Empty, callback)
  rospy.spin()

if __name__ == '__main__':
  try:
    listener()
  except rospy.ROSInterruptException:
    pass