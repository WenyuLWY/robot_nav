import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription,DeclareLaunchArgument,GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource,AnyLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    rviz=GroupAction([
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', os.path.join(get_package_share_directory('robot_nav'), 'config', 'nav.rviz')],
            output='screen',
            ),
    ])
 
    scout_base=GroupAction([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('scout_base'),
                'launch',
                'scout_base.launch.py')
                ),
            launch_arguments={
                'port_name': 'can1',
                'is_scout_mini': 'true',
                'odom_topic_name': '/wheel/odom'
            }.items()
        ) 
    ])

    scout_description=GroupAction([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('scout_description'),
                'launch',
                'scout_base_description.launch.py')
                ),
            launch_arguments={
                'use_sim_time': 'false',
            }.items()
        )
    ])

    imu=GroupAction([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('hipnuc_imu'),
                'launch',
                'imu_spec_msg.launch.py')
            ),
        )
    ])

    camera=GroupAction([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('realsense2_camera'),
                'launch',
                'rs_launch.py')
            ),  
        )
    ])

    rslidar= GroupAction([
        Node(
            namespace='rslidar_sdk',
            package='rslidar_sdk',
            executable='rslidar_sdk_node',
            output='screen',
            parameters=[{'config_path': os.path.join(get_package_share_directory('robot_nav'), 'config','rslidar.yaml')}],
        ),
    ])

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
                # 'imu_topic': '/imu/data',
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

    aede=GroupAction([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('robot_nav'), 'launch', 'system_real_robot.launch.py')
            ),
        )
    ]) 

    ld= LaunchDescription()
    ld.add_action(rviz)
    ld.add_action(scout_base)
    # ld.add_action(scout_description)

    # ld.add_action(imu)
    # ld.add_action(camera)
    ld.add_action(rslidar)

    ld.add_action(static_transform_node)
    ld.add_action(rtabmap)
    ld.add_action(trajectory)

    ld.add_action(aede)


    return ld