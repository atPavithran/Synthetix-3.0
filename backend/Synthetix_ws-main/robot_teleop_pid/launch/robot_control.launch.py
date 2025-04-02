import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from launch_ros.actions import Node


def generate_launch_description():
    # Declare launch arguments
    active_robot = DeclareLaunchArgument(
        'active_robot',
        default_value='0',
        description='Which robot to control (0 = all, 1-5 for specific robot)'
    )
    
    kp = DeclareLaunchArgument(
        'kp',
        default_value='23.0',
        description='Proportional gain for PID controller'
    )
    
    ki = DeclareLaunchArgument(
        'ki',
        default_value='0.5',
        description='Integral gain for PID controller'
    )
    
    kd = DeclareLaunchArgument(
        'kd',
        default_value='1.0',
        description='Derivative gain for PID controller'
    )
    
    teleop_node_start = DeclareLaunchArgument(
        'teleop_node_start',
        default_value='true',
        description='Whether to start the teleop node'
    )
    
    # Teleop node with condition
    teleop_node = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        name='teleop',
        output='screen',
        remappings=[
            ('/cmd_vel', '/teleop_key/cmd_vel')
        ],
        condition=IfCondition(LaunchConfiguration('teleop_node_start'))
    )
    
    # PID controller node
    pid_controller_node = Node(
        package='robot_teleop_pid',
        executable='teleop_pid_controller',  # Remove .py extension - must match entry_point name
        name='teleop_pid_controller',
        output='screen',
        parameters=[
            {'active_robot': LaunchConfiguration('active_robot')},
            {'kp': LaunchConfiguration('kp')},
            {'ki': LaunchConfiguration('ki')},
            {'kd': LaunchConfiguration('kd')}
        ]
    )
    
    return LaunchDescription([
        active_robot,
        kp,
        ki,
        kd,
        teleop_node_start,
        teleop_node,
        pid_controller_node
    ])