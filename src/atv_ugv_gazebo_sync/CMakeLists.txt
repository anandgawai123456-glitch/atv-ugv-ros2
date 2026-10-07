cmake_minimum_required(VERSION 3.8)
project(atv_ugv_gazebo_sync)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(geometry_msgs REQUIRED)

find_package(gz-transport13 REQUIRED)
find_package(gz-msgs10 REQUIRED)

add_executable(gazebo_rviz_sync
  src/gazebo_rviz_sync.cpp
)

ament_target_dependencies(gazebo_rviz_sync
  rclcpp
  tf2
  tf2_ros
  geometry_msgs
)

target_link_libraries(gazebo_rviz_sync
  gz-transport13::gz-transport13
  gz-msgs10::gz-msgs10
)

install(TARGETS
  gazebo_rviz_sync
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
