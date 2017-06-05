import rospy
from std_msgs.msg import Empty

def callback(data):
    print("I heard ",data)
    
def listener():
    rospy.init_node('save_topic')
    trigger_topic = rospy.get_param('/trigger_topic_name')
    rospy.Subscriber(trigger_topic, Empty, callback)
    rospy.spin()