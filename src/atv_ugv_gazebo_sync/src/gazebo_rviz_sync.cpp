#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "tf2_ros/transform_broadcaster.h"
#include "tf2_msgs/msg/tf_message.hpp"

class GazeboRvizSync : public rclcpp::Node
{
public:
  GazeboRvizSync()
  : Node("gazebo_rviz_sync")
  {
    tf_broadcaster_ =
      std::make_unique<tf2_ros::TransformBroadcaster>(*this);

    pose_sub_ = this->create_subscription<tf2_msgs::msg::TFMessage>(
      "/world/empty/dynamic_pose/info",
      rclcpp::QoS(10),
      std::bind(
        &GazeboRvizSync::pose_callback,
        this,
        std::placeholders::_1));

    RCLCPP_INFO(
      this->get_logger(),
      "Subscribed to /world/empty/dynamic_pose/info");
  }

private:
  void pose_callback(const tf2_msgs::msg::TFMessage::SharedPtr msg)
  {
    if (msg->transforms.empty()) {
      return;
    }

    /*
     * Gazebo dynamic_pose contains multiple transforms.
     * The ATV base pose is the transform with approximately:
     *
     * x = 0
     * y = 0
     * z = 0
     *
     * while the wheel transforms are around z = 0.05.
     *
     * We select the transform with the lowest z value.
     */

    const geometry_msgs::msg::TransformStamped * robot_pose = nullptr;

    double lowest_z = 1e9;

    for (const auto & transform : msg->transforms)
    {
      double z = transform.transform.translation.z;

      if (z < lowest_z)
      {
        lowest_z = z;
        robot_pose = &transform;
      }
    }

    if (robot_pose == nullptr) {
      return;
    }

    geometry_msgs::msg::TransformStamped tf_msg;

    tf_msg.header.stamp = this->get_clock()->now();
    tf_msg.header.frame_id = "odom";
    tf_msg.child_frame_id = "base_footprint";

    tf_msg.transform.translation.x =
      robot_pose->transform.translation.x;

    tf_msg.transform.translation.y =
      robot_pose->transform.translation.y;

    tf_msg.transform.translation.z = 0.0;

    tf_msg.transform.rotation =
      robot_pose->transform.rotation;

    tf_broadcaster_->sendTransform(tf_msg);
  }

  rclcpp::Subscription<tf2_msgs::msg::TFMessage>::SharedPtr pose_sub_;

  std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);

  rclcpp::spin(
    std::make_shared<GazeboRvizSync>());

  rclcpp::shutdown();

  return 0;
}
