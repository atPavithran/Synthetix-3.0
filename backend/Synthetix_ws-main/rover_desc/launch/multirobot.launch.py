import os
from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro

def generate_launch_description():
    package_name = 'rover_desc'
    pkg_share = get_package_share_directory(package_name)

    world_file_path = os.path.join(pkg_share, 'worlds', 'latest.world')

    # xacro_file = os.path.join(pkg_share, 'urdf', 'rover.urdf.xacro')
    robot1_xacro_file = os.path.join(pkg_share,'urdf','robot_1.urdf.xacro')
    robot2_xacro_file = os.path.join(pkg_share,'urdf','robot_2.urdf.xacro')
    robot3_xacro_file = os.path.join(pkg_share,'urdf','robot_3.urdf.xacro')
    robot4_xacro_file = os.path.join(pkg_share,'urdf','robot_4.urdf.xacro')
    robot5_xacro_file = os.path.join(pkg_share,'urdf','robot_5.urdf.xacro')

    robot1_description = {'robot_description': xacro.process_file(robot1_xacro_file).toxml()}
    robot2_description = {'robot_description': xacro.process_file(robot2_xacro_file).toxml()}
    robot3_description = {'robot_description': xacro.process_file(robot3_xacro_file).toxml()}
    robot4_description = {'robot_description': xacro.process_file(robot4_xacro_file).toxml()}
    robot5_description = {'robot_description': xacro.process_file(robot5_xacro_file).toxml()}

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={
            'world': world_file_path
        }.items()
    )

    # Group actions under namespace
    spawn1 = Node(
        package='gazebo_ros',
        executable="spawn_entity.py",
        arguments=['-topic', 'robot_description', '-entity', 'robot_1', '-y', '-36.0'],
        parameters=[{'use_sim_time': True}],
        namespace='robot1'
    )

    spawn2 = Node(
        package='gazebo_ros',
        executable="spawn_entity.py",
        arguments=['-topic', 'robot_description', '-entity', 'robot_2', '-y', '-18.0'],
        parameters=[{'use_sim_time': True}],
        namespace='robot2'
    )

    spawn3 = Node(
        package='gazebo_ros',
        executable="spawn_entity.py",
        arguments=['-topic', 'robot_description', '-entity', 'robot_3'],
        parameters=[{'use_sim_time': True}],
        namespace='robot3'
    )

    spawn4 = Node(
        package='gazebo_ros',
        executable="spawn_entity.py",
        arguments=['-topic', 'robot_description', '-entity', 'robot_4','-y', '18.0'],
        parameters=[{'use_sim_time': True}],
        namespace='robot4'
    )

    spawn5 = Node(
        package='gazebo_ros',
        executable="spawn_entity.py",
        arguments=['-topic', 'robot_description', '-entity', 'robot_5', '-y', '36.0'],
        parameters=[{'use_sim_time': True}],
        namespace='robot5'
    )

    robot1_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot1_description, {'use_sim_time': True}],
        namespace='robot1'
    )

    robot2_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot2_description, {'use_sim_time': True}],
        namespace='robot2'
    )

    robot3_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot3_description, {'use_sim_time': True}],
        namespace='robot3'
    )

    robot4_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot4_description, {'use_sim_time': True}],
        namespace='robot4'
    )

    robot5_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot5_description, {'use_sim_time': True}],
        namespace='robot5'
    )

    return LaunchDescription([
        gazebo,
        spawn1,
        spawn2,
        spawn3,
        spawn4,
        spawn5,
        robot1_publisher,
        robot2_publisher,
        robot3_publisher,
        robot4_publisher,
        robot5_publisher
    ])
