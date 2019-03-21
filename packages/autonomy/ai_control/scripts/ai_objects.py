#!/usr/bin/env python
import rospy
from std_msgs.msg import Int8, Int16, String
from nav_msgs.msg import Odometry
from gazebo_msgs.msg import LinkStates
from sensor_msgs.msg import JointState
from ai_control.msg import ObstacleDetection


class WorldState():

    def __init__(self):
        self.state_flags = {'positionX': 0, 'positionY': 0, 'positionZ': 0, 
                            'front_arm_angle': 0, 'back_arm_angle': 0, 
                            'front_arm_angle': 0, 'heading': 0, 'warning_flag': 0}

        self. auto_function_command = 0


    def jointCallBack(self, data):
        """ Set state_flags joint position data. """

        self.state_flags['front_arm_angle'] = -(data.position[1])
        self.state_flags['back_arm_angle'] = data.position[0]
    

    def odometryCallBack(self, data):
        """ Set state_flags world position data. """

        self.state_flags['positionX'] = data.pose.pose.position.z
        self.state_flags['positionY'] = data.pose.pose.position.y
        self.state_flags['heading'] = data.twist.twist.linear.z
        

    def visionCallBack(self, data):
        """ Set state_flags vision data. """

        self.state_flags['warning_flag'] = data.data


class ROSUtility():

    def __init__(self):
                                            # ezrassor/routine_responses
        self.command_pub = rospy.Publisher('ezrassor/routine_responses', Int16, queue_size=100)
        self.status_pub = rospy.Publisher('ez_rassor/status', String, queue_size=100)
        self.rate = rospy.Rate(30) # 30hz

        self. auto_function_command = 0

        self.commands = {'forward' : 0b100000000000, 'reverse' : 0b010000000000, 'left' : 0b001000000000, 'right' : 0b000100000000, 
                'front_arm_up' : 0b000010000000, 'front_arm_down' : 0b000001000000, 'back_arm_up' : 0b000000100000, 'back_arm_down' : 0b000000010000,
                'front_dig' : 0b000000001000, 'front_dump' : 0b000000000100, 'back_dig' : 0b000000000010, 'back_dump' : 0b000000000001,
                'arms_up' : 0b000010100000, 'arms_down' : 0b000001010000, 'null': 0b000000000000}

    def autoCommandCallBack(self, data):
        """ Set auto_function_command to the current choice. """
        self.auto_function_command = data.data


