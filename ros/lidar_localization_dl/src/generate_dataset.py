#!/usr/bin/env python

from sensor_msgs.msg import LaserScan
from gazebo_msgs.srv import GetModelState, SetModelState
from gazebo_msgs.msg import ModelState
import numpy as np

import random

import json
import yaml

from ros_tools import Node as ROS

ros = ROS("dataset_generator")

dataset = []

get_robot_state = ros.service_proxy('/gazebo/get_model_state', GetModelState)
set_robot_state = ros.service_proxy('/gazebo/set_model_state', SetModelState)

def next_state(old_state):
    new_state = ModelState()
    new_state.model_name = "turtlebot3"

    new_state.pose.position.x = random.uniform(-7.33, 7.25)
    new_state.pose.position.y = random.uniform(5.07, -5.01)
    new_state.pose.position.z = old_state.pose.position.z
    new_state.pose.orientation.x = 0
    new_state.pose.orientation.y = 0
    new_state.pose.orientation.z = 0
    new_state.pose.orientation.w = 0

    set_robot_state(new_state)

@ros.subscribe("scan", LaserScan)
def on_lidar(lidar):
    state = get_robot_state(model_name="turtlebot3")
    pose = yaml.load(str(state.pose))
    sample = {
        "pose": pose,
        "lidar": lidar.ranges
    }

    dataset.append(sample)
    
    print(len(dataset))

    if(len(dataset) % 5000 == 0):
        print('Saving dataset...')
        dataset_json = json.dumps(dataset)

        with open("dataset_%s.json" % len(dataset), "w") as dataset_file:
            dataset_file.write(dataset_json)

        print('Dataset saved.')

    next_state(state)

if __name__ == '__main__':
    ros.spin()