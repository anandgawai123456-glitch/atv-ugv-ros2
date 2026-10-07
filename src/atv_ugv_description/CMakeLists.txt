cmake_minimum_required(VERSION 3.8)
project(atv_ugv_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(urdf REQUIRED)
find_package(xacro REQUIRED)

# Install launch, URDF, and mesh directories before calling ament_package()
install(
  DIRECTORY launch urdf meshes config worlds scripts
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
