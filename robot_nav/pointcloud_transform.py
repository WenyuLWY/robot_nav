
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from rclpy.qos import qos_profile_sensor_data
from rclpy.duration import Duration

from sensor_msgs.msg import PointCloud2

from tf2_ros import Buffer, TransformListener, TransformException
from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud


class PointCloudTransformNode(Node):
    def __init__(self):
        super().__init__('pointcloud_transform_node')

        # # Declare parameters
        # self.declare_parameter('input_topic', '/rslidar_points')
        # self.declare_parameter('output_topic', '/rslidar_points_registered')
        # self.declare_parameter('target_frame', 'map')

        # # Get parameters
        # input_topic = self.get_parameter('input_topic').value
        # output_topic = self.get_parameter('output_topic').value
        # self.target_frame = self.get_parameter('target_frame').value
        input_topic='/rslidar_points'
        output_topic='/rslidar_points_registered'
        self.target_frame='map'


        # TF listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(
            self.tf_buffer, self
        )

        # Subscriber
        self.pc_sub = self.create_subscription(
            PointCloud2,
            input_topic,
            self.pc_callback,
            qos_profile_sensor_data
        )

        # Publisher
        self.registered_pc_pub = self.create_publisher(
            PointCloud2,
            output_topic,
            10
        )

        self.get_logger().info(
            'PointCloud Registration Node started.'
        )

    def pc_callback(self, msg: PointCloud2):
        source_frame = msg.header.frame_id
        target_frame = 'map'

        try:
            # Lookup TF at point cloud timestamp
            transform = self.tf_buffer.lookup_transform(
                target_frame,
                source_frame,
                # Time.from_msg(msg.header.stamp),
                Time(seconds=0), 
                timeout=Duration(seconds=0.1)
            )

            # Transform point cloud to map frame
            registered_cloud = do_transform_cloud(
                msg, transform
            )

            # Publish
            self.registered_pc_pub.publish(
                registered_cloud
            )

        except TransformException as ex:
            self.get_logger().warn(
                f'TF lookup failed: {ex}',
                throttle_duration_sec=2.0
            )


def main(args=None):
    rclpy.init(args=args)

    node = PointCloudTransformNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
