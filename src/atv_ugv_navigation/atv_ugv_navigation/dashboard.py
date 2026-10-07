import tkinter as tk
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class Dashboard(Node):

    def __init__(self):
        super().__init__('atv_dashboard')

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.linear_speed = 0.20
        self.angular_speed = 0.60

    def send_cmd(self, linear=0.0, angular=0.0):
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.cmd_pub.publish(msg)

    def stop(self):
        self.send_cmd(0.0, 0.0)


def main():
    rclpy.init()

    node = Dashboard()

    root = tk.Tk()
    root.title("ATV UGV Dashboard")
    root.geometry("400x400")

    title = tk.Label(
        root,
        text="ATV UGV",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=20)

    forward = tk.Button(
        root,
        text="▲ FORWARD",
        font=("Arial", 16, "bold"),
        width=15,
        height=2,
        command=lambda: node.send_cmd(
            node.linear_speed,
            0.0
        )
    )
    forward.pack(pady=5)

    backward = tk.Button(
        root,
        text="▼ BACKWARD",
        font=("Arial", 16, "bold"),
        width=15,
        height=2,
        command=lambda: node.send_cmd(
            -node.linear_speed,
            0.0
        )
    )
    backward.pack(pady=5)

    left = tk.Button(
        root,
        text="↶ LEFT",
        font=("Arial", 16, "bold"),
        width=15,
        height=2,
        command=lambda: node.send_cmd(
            0.0,
            node.angular_speed
        )
    )
    left.pack(pady=5)

    right = tk.Button(
        root,
        text="↷ RIGHT",
        font=("Arial", 16, "bold"),
        width=15,
        height=2,
        command=lambda: node.send_cmd(
            0.0,
            -node.angular_speed
        )
    )
    right.pack(pady=5)

    stop = tk.Button(
        root,
        text="■ STOP",
        bg="red",
        fg="white",
        font=("Arial", 16, "bold"),
        width=15,
        height=2,
        command=node.stop
    )
    stop.pack(pady=15)

    root.mainloop()

    node.stop()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
