import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription,DeclareLaunchArgument,GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource,AnyLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    static_transform_node = GroupAction([
        Node(package='tf2_ros',executable='static_transform_publisher', output='screen',
            arguments=['0','0','0','0','0','0','sensor','rslidar'], name='tf_sensor', 
        ),
        Node(package='tf2_ros',executable='static_transform_publisher', output='screen',
            arguments=['0','0','0','0','0','0','sensor','camera'], name='tf_sensor2camera', 
        ),
        Node(package='tf2_ros',executable='static_transform_publisher', output='screen',
            arguments=['0','0','0','0','0','0','sensor','vehicle'], name='tf_sensor2vehicle', 
        ),
    ])
    
    rtabmap=GroupAction([IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(get_package_share_directory('robot_nav'), 'launch', 'lidar3d.launch.py')
                ),
            launch_arguments={
                'lidar_topic':   'rslidar_points',
                'frame_id':      'sensor',
                'deskewing':     'false',
                'use_sim_time':  'false',
                'localization':  'false',
                'rtabmap_viz':   'false',
                # 'imu_topic': '/IMU_data',
                # 'odom_topic': '/odom',
            }.items(),
        )
    ])  
    
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

    pointcloud_transform=GroupAction([
        Node(
        package='robot_nav',
        executable='pointcloud_transform_node',
        name='pointcloud_transform_node',
        )
    ])

    ld= LaunchDescription()
    # ld.add_action(rviz)

    # ld.add_action(static_transform_node)
    ld.add_action(rtabmap)
    ld.add_action(pointcloud_transform)
    # ld.add_action(trajectory)



    return ld