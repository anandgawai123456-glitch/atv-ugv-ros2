import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy
from nav_msgs.msg import OccupancyGrid


class MapRvizRelay(Node):
    def __init__(self):
        super().__init__('map_rviz_relay')

        transient_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        volatile_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        self.latest_map = None

        self.subscription = self.create_subscription(
            OccupancyGrid,
            '/map',
            self.map_callback,
            transient_qos,
        )

        self.publisher = self.create_publisher(
            OccupancyGrid,
            '/map_rviz',
            volatile_qos,
        )

        self.timer = self.create_timer(1.0, self.republish_map)

    def map_callback(self, msg):
        self.latest_map = msg

    def republish_map(self):
        if self.latest_map is not None:
            self.publisher.publish(self.latest_map)


def main(args=None):
    rclpy.init(args=args)
    node = MapRvizRelay()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
