#!/usr/bin/python3
from email import message_from_string
from re import MULTILINE, split
import serial
import time
import rospy
from std_msgs.msg import String

temp = 1

def subscriber():
      sub = rospy.Subscriber('gcode_topic', String, callback)
      rospy.spin()


def callback(message):
      # Open grbl serial port ==> CHANGE THIS BELOW TO MATCH YOUR USB LOCATION
      s = serial.Serial('/dev/ttyACM0',115200) # GRBL operates at 115200 baud. Leave that part alone.
      f= open("/home/youssef/catkin_ws/src/caligraphy_robot/engrave/grbl.gcode","r")
      while not rospy.is_shutdown():
            
            # Wake up grbl
            s.write(str.encode('\r\n\r\n'))
            time.sleep(2)   # Wait for grbl to initialize
            s.flushInput()  # Flush startup text in serial input
            # Stream g-code to grbl
            
            for line in f:
                  l = line.strip() # Strip all EOL characters for consistency
                  print ('Sending: ' + l,)
                  s.write(str.encode(l + '\n')) # Send g-code block to grbl
                  grbl_out = s.readline() # Wait for grbl response with carriage return
                  grbl_out= str(grbl_out)
                  print (' : ' + grbl_out.strip())
            



            #input("  Press <Enter> to exit and disable grbl.")
            print("Finished")
            # Close file and serial port
            f.close()
            s.close()

if __name__ == '__main__':
      rospy.init_node('engrave_subscriber')
      subscriber()
