import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
import sys
import termios
import tty


class KeyboardTeleop(Node):

    def __init__(self):
        super().__init__('keyboard_teleop')

        self.pub = self.create_publisher(
            TwistStamped,
            '/diff_drive_controller/cmd_vel',
            10
        )

        self.speed = 0.5
        self.turn = 0.8

    def publish(self, linear=0.0, angular=0.0):
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_footprint'

        msg.twist.linear.x = linear
        msg.twist.angular.z = angular

        self.pub.publish(msg)

    def run(self):

        settings = termios.tcgetattr(sys.stdin)

        print("""
ATV UGV Keyboard Teleop
-----------------------
        i
    j   k   l
        ,

i = forward
, = backward
j = left
l = right
k = stop
q = quit

Speed: 0.2 m/s
Turn:  0.8 rad/s
""")

        try:
            tty.setcbreak(sys.stdin.fileno())

            while rclpy.ok():

                key = sys.stdin.read(1)

                if key == 'i':
                    self.publish(0.2, 0.0)

                elif key == ',':
                    self.publish(-0.2, 0.0)

                elif key == 'j':
                    self.publish(0.0, 0.8)

                elif key == 'l':
                    self.publish(0.0, -0.8)

                elif key == 'k':
                    self.publish(0.0, 0.0)

                elif key == 'q':
                    break

        finally:
            self.publish(0.0, 0.0)
            termios.tcsetattr(
                sys.stdin,
                termios.TCSADRAIN,
                settings
            )


def main():
    rclpy.init()

    node = KeyboardTeleop()

    try:
        node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
