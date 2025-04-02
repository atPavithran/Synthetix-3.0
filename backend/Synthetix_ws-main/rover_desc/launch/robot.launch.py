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

    namespace_arg = DeclareLaunchArgument(
            'namespace', default_value='rover', description='Namespace for the robot'
        )
    namespace = LaunchConfiguration('namespace')

    x_position_arg = DeclareLaunchArgument(
        'x_position', default_value='0.0', description='X position of the robot'
    )
    x_position = LaunchConfiguration('x_position')

    xacro_file = os.path.join(pkg_share, 'urdf', 'rover.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file, mappings={'robot_namespace': namespace})
    robot_description = {'robot_description': robot_description_config.toxml()}

    robot_name = LaunchConfiguration('namespace')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        )
    )

    # Group actions under namespace
    robot_group = GroupAction([
        Node(
            package='gazebo_ros',
            executable="spawn_entity.py",
            arguments=['-topic', 'robot_description', '-entity', robot_name, '-x', x_position],
            parameters=[{'use_sim_time': True}],
            namespace=namespace
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[robot_description, {'use_sim_time': True}],
            namespace=namespace
        )
    ])
    return LaunchDescription([
        gazebo,
        namespace_arg,
        x_position_arg,
        robot_group
    ])
