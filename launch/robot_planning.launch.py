import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription,DeclareLaunchArgument,GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource,AnyLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

 
    
    trajectory = GroupAction([
        Node(
        package='mogi_trajectory_server',
        executable='mogi_trajectory_server',
        name='mogi_trajectory_server',
        parameters=[{'reference_frame_id': 'map',
                    'robot_frame_id': 'sensor',
                    'use_sim_time': False}]
        )
    ])

    aede=GroupAction([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('robot_nav'), 'launch', 'system_real_robot.launch.py')
            ),
        )
    ]) 

    ld= LaunchDescription()
    # ld.add_action(rviz)

    ld.add_action(trajectory)

    ld.add_action(aede)


    return ld