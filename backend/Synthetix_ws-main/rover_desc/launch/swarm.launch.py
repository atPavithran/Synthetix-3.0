import os
from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    package_name = 'rover_desc'
    pkg_share = get_package_share_directory(package_name)

    # Declare arguments for the namespaces and x positions of both robots
    # namespace1_arg = DeclareLaunchArgument(
    #     'namespace1', default_value='rover1', description='Namespace for the first robot'
    # )
    
    # namespace2_arg = DeclareLaunchArgument(
    #     'namespace2', default_value='rover2', description='Namespace for the second robot'
    # )

    # x_position1_arg = DeclareLaunchArgument(
    #     'x_position1', default_value='0.0', description='X position for the first robot'
    # )
    
    # x_position2_arg = DeclareLaunchArgument(
    #     'x_position2', default_value='5.0', description='X position for the second robot'
    # )

    # Include Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        )
    )

    # Path to the robot launch file
    robot_launch_path = os.path.join(pkg_share, 'launch', 'robot.launch.py')

    robot1 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(robot_launch_path),
        launch_arguments={
            'namespace': 'robot1',
            'x_position': '10.0'
        }.items()
    )

    # Robot 2 launch with namespace and x_position
    robot2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(robot_launch_path),
        launch_arguments={
            'namespace': 'robot2',
            'x_position': '20.0'
        }.items()
    )

    robot3 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(robot_launch_path),
        launch_arguments={
            'namespace': 'robot3',
            'x_position': '30.0'
        }.items()
    )

    robot4 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(robot_launch_path),
        launch_arguments={
            'namespace': 'robot4',
            'x_position': '40.0'
        }.items()
    )

    robot5 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(robot_launch_path),
        launch_arguments={
            'namespace': 'robot5',
            'x_position': '50.0'
        }.items()
    )

    # Return LaunchDescription
    return LaunchDescription([
        gazebo,
        # namespace1_arg,
        # namespace2_arg,
        # x_position1_arg,
        # x_position2_arg,
        robot1,
        robot2,
        robot3,
        robot4,
        robot5
    ])
