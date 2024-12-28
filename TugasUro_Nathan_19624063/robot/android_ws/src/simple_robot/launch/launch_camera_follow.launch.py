import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='gazebo_ros',
            executable='gzserver',
            name='gazebo',
            output='screen',
            parameters=[{'use_sim_time': True}],
        ),
        Node(
            package='gazebo_ros',
            executable='gzclient',
            name='gazebo_gui',
            output='screen',
        ),
        Node(
            package='simple_robot',
            executable='camera_follow.py',
            name='camera_follow',
            output='screen',
            parameters=[{'use_sim_time': True}],
        ),
    ])

