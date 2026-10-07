#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class ScanFrameRelay(Node):
    def __init__(self):
        super().__init__('scan_frame_relay')

        self.subscription = self.create_subscription(
            LaserScan,
            '/scan_filtered_raw',
            self.scan_callback,
            10,
        )

        self.publisher = self.create_publisher(
            LaserScan,
            '/scan_filtered',
            10,
        )

    def scan_callback(self, msg: LaserScan):
        msg.header.frame_id = 'lidar_link'
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ScanFrameRelay()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
