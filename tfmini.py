#!/usr/bin/python

import rospy
import serial
from sensor_msgs.msg import Range

ser = serial.Serial("/dev/ttyS0", 115200)
topic = "~bottom"

def getTFminiData():
    sensor = Range()
    rate = rospy.Rate(100)
    pub = rospy.Publisher(topic,  Range ,queue_size=10)
    while not rospy.is_shutdown():
        count = ser.in_waiting
        if count > 8:
            recv = ser.read(9)
            ser.reset_input_buffer()
            if recv[0] == 'Y' and recv[1] == 'Y': # 0x59 is 'Y'
                low = int(recv[2].encode('hex'), 16)
                high = int(recv[3].encode('hex'), 16)
                sensor.range = float(low + high * 256) / 100.0
     
                pub.publish(sensor)

        rate.sleep()


if __name__ == '__main__':
    try:
        rospy.init_node("tfmini")
        if ser.is_open == False:
            ser.open()
        getTFminiData()
    except rospy.ROSInterruptException:   # Ctrl+C
        if ser != None:
            ser.close()
