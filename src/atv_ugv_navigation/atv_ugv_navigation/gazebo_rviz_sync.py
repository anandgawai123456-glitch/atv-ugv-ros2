import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
from ros_gz_interfaces.msg import EntityState
from ros_gz_interfaces.srv import GetEntityState


class GazeboRvizSync(Node):

    def __init__(self):
        super().__init__('gazebo_rviz_sync')

        self.tf_broadcaster = TransformBroadcaster(self)

        self.client = self.create_client(
            GetEntityState,
            '/world/empty/get_entity_state'
        )

        self.timer = self.create_timer(0.02, self.update_tf)

        self.get_logger().info('Gazebo → RViz2 sync node started')

    def update_tf(self):

        if not self.client.service_is_ready():
            return

        request = GetEntityState.Request()
        request.name = 'atv_ugv'
        request.reference_frame = 'world'

        future = self.client.call_async(request)
        future.add_done_callback(self.publish_tf)

    def publish_tf(self, future):

        try:
            result = future.result()
        except Exception:
            return

        if not result.success:
            return

        pose = result.state.pose

        transform = TransformStamped()

        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = 'odom'
        transform.child_frame_id = 'base_footprint'

        transform.transform.translation.x = pose.position.x
        transform.transform.translation.y = pose.position.y
        transform.transform.translation.z = pose.position.z

        transform.transform.rotation.x = pose.orientation.x
        transform.transform.rotation.y = pose.orientation.y
        transform.transform.rotation.z = pose.orientation.z
        transform.transform.rotation.w = pose.orientation.w

        self.tf_broadcaster.sendTransform(transform)


def main(args=None):
    rclpy.init(args=args)

    node = GazeboRvizSync()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
