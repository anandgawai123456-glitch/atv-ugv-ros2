# ATV UGV — ROS 2 Autonomous Navigation Simulation

A ROS 2 Jazzy simulation of an **All-Terrain Vehicle (ATV) Unmanned Ground Vehicle (UGV)** focused on autonomous navigation, LiDAR-based perception, mapping, localization, and obstacle avoidance in simulation.

The project is being developed as a foundation for testing autonomous navigation on challenging outdoor terrain before transferring the stack to physical hardware.

---

## 🚙 Project Overview

The ATV UGV is a four-wheel-drive robotic platform designed for autonomous operation in outdoor environments.

The current simulation integrates:

* ROS 2 Jazzy
* Gazebo / Gazebo Sim
* LiDAR-based perception
* Wheel odometry
* TF2 transforms
* SLAM Toolbox
* Map Server
* AMCL localization
* Nav2 navigation
* RViz2 visualization
* Differential-drive controller
* Custom robot description using URDF/Xacro

### Current Navigation Pipeline

```text
                    ┌─────────────────┐
                    │     Gazebo      │
                    │   ATV / UGV     │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
           LiDAR                         Odometry
              │                             │
        /scan_raw                         /odom
              │                             │
        Scan Filtering                     │
              │                             │
        /scan_filtered                     │
              │                             │
              └──────────────┬──────────────┘
                             │
                         TF2 Frames
                             │
                 ┌───────────┴───────────┐
                 │                       │
             SLAM / Map              Localization
                 │                       │
                /map                  AMCL
                 │                       │
                 └───────────┬───────────┘
                             │
                            Nav2
                             │
                       Path Planning
                             │
                       Local Control
                             │
                          /cmd_vel
                             │
                            ATV
```

---

# 🛠️ Current Features

### Robot Simulation

* ATV/UGV model simulated in Gazebo
* Four-wheel configuration
* Differential-drive controller
* Wheel odometry
* LiDAR sensor
* IMU sensor
* ROS 2 TF tree
* Simulated `/clock`

### Perception

Current perception is primarily LiDAR based.

```text
Gazebo LiDAR
     ↓
/scan_raw
     ↓
Scan filtering / frame relay
     ↓
/scan_filtered
     ↓
SLAM / Localization / Costmaps
```

### Mapping

The project uses **SLAM Toolbox** for creating 2D occupancy-grid maps.

The generated map can be saved as:

```text
atv_map.yaml
atv_map.pgm
```

The current map resolution is:

```text
0.05 m / pixel
```

### Localization

The saved map is used with:

* Nav2 Map Server
* AMCL
* `map → odom → base_footprint` TF chain

### Navigation

Nav2 is used as the navigation framework for:

* Global planning
* Local planning/control
* Global costmap
* Local costmap
* Obstacle avoidance
* Robot recovery behavior

---

# 🧩 Major Development Challenges

Developing the simulation involved several issues that are common when building a real robotic navigation stack.

## 1. Wheel Geometry and Odometry

One of the early challenges was ensuring that the wheel geometry used by Gazebo matched the parameters used by the ROS 2 differential-drive controller.

Differences in:

* Wheel separation
* Wheel radius
* Wheel joint positions
* Robot footprint

caused noticeable differences between simulated robot motion and ROS odometry.

The controller parameters were therefore adjusted to match the actual simulated wheel geometry.

---

## 2. Odometry and TF Alignment

Navigation depends heavily on a consistent TF tree.

The required relationship is:

```text
map
 ↓
odom
 ↓
base_footprint
 ↓
lidar_link
```

Incorrect or inconsistent transforms can result in:

* LiDAR appearing to drift
* Robot position appearing incorrect in RViz
* Costmaps becoming misaligned
* Navigation planners failing to transform robot poses
* AMCL failing to establish the expected localization transform

TF consistency therefore became one of the most important parts of the project.

---

## 3. LiDAR Frame Handling

The Gazebo LiDAR initially produced a sensor frame that did not directly match the frame expected by the navigation stack.

The project therefore introduced a scan-frame relay/filtering stage:

```text
Gazebo LiDAR
     ↓
/scan_raw
     ↓
scan frame processing
     ↓
/scan_filtered
     ↓
Navigation stack
```

This helped keep the sensor interface consistent with the robot's TF structure.

Further tuning is still required for accurate obstacle perception during motion.

---

## 4. SLAM and Map Generation

Getting SLAM to work reliably required coordinating:

* LiDAR data
* Odometry
* TF
* `use_sim_time`
* SLAM Toolbox
* Gazebo timing
* RViz visualization

Once the pipeline was functioning, a 2D occupancy-grid map was successfully generated and saved.

---

## 5. Map Server and Localization

Another challenge was ensuring that the saved map was correctly loaded by Nav2's Map Server and made available to localization.

The localization pipeline depends on:

```text
Map YAML
    ↓
Map Server
    ↓
/map
    ↓
AMCL
    ↓
map → odom
```

Incorrect map paths, lifecycle states, QoS settings, or missing transforms can prevent the navigation stack from receiving the map correctly.

---

## 6. Local Costmap and Obstacle Avoidance

The robot can detect obstacles using LiDAR, but obstacle avoidance is not yet perfectly tuned.

Current limitations include:

* Occasional LiDAR drift during motion
* Conservative or inaccurate obstacle inflation
* The ATV occasionally getting slightly stuck
* Avoidance behavior requiring further tuning
* Costmap parameters needing optimization for the ATV footprint
* Navigation behavior changing depending on obstacle geometry

This is an active area of development.

The goal is to make the local costmap accurately represent the physical dimensions of the ATV and provide smoother obstacle avoidance.

---

## 7. Simulation Performance

The development system is a relatively lightweight laptop, so running Gazebo, RViz2, ROS 2 nodes, SLAM, and Nav2 simultaneously can create significant CPU and memory load.

This required keeping the simulation relatively lightweight and avoiding unnecessary visualization or processing.

---

# 🌲 Future Development — Outdoor / Jungle Terrain

A major future objective is to move beyond a simple indoor-style environment and simulate **realistic outdoor terrain**.

The next environment will introduce a jungle/forest-style terrain containing:

* Uneven ground
* Slopes
* Rocks
* Trees
* Bushes
* Narrow passages
* Irregular obstacles
* Terrain elevation changes
* Potential mud/rough-ground regions

The purpose is to test whether the navigation stack can handle environments that are significantly less structured than a conventional flat indoor map.

### Planned Environment

```text
                    JUNGLE TERRAIN
                           │
          ┌────────────────┼────────────────┐
          │                │                │
       Trees            Rocks             Slopes
          │                │                │
          └────────────────┼────────────────┘
                           │
                         ATV
                           │
                    LiDAR + Camera
                           │
                    Perception System
                           │
                        Nav2
```

This environment will allow the navigation system to be tested under more realistic outdoor conditions.

---

# 📷 Future Perception — Depth Camera

A **depth camera** will be added as the next major perception upgrade.

The current LiDAR-only system provides strong 2D obstacle detection, but a depth camera can provide additional information about the 3D environment.

Planned applications include:

* 3D obstacle detection
* Detection of objects outside the LiDAR scan plane
* Terrain perception
* Tree/vegetation detection
* Rock and uneven-ground detection
* Improved obstacle classification
* Improved perception in complex environments

The future perception pipeline will be:

```text
                 ┌───────────────┐
                 │     LiDAR     │
                 └───────┬───────┘
                         │
                         │
                 ┌───────▼────────┐
                 │                 │
                 │   Perception    │
                 │     Fusion      │
                 │                 │
                 └───────▲─────────┘
                         │
                 ┌───────┴───────┐
                 │  Depth Camera │
                 └───────────────┘
                         │
                         ▼
                3D Environment Data
                         │
                         ▼
                   Navigation
```

Potential future integration includes converting depth information into suitable point-cloud or obstacle representations for the Nav2 costmaps.

---

# 🚧 Future Improvements

### Perception

* [ ] Integrate depth camera
* [ ] Fuse LiDAR and depth-camera data
* [ ] Improve LiDAR filtering
* [ ] Improve obstacle detection
* [ ] Add 3D perception
* [ ] Detect terrain hazards

### Navigation

* [ ] Fine-tune local costmap
* [ ] Fine-tune global costmap
* [ ] Optimize inflation parameters
* [ ] Improve obstacle avoidance
* [ ] Improve recovery behaviors
* [ ] Tune controller velocity/acceleration limits
* [ ] Test narrow passages

### Outdoor Simulation

* [ ] Create jungle environment
* [ ] Add uneven terrain
* [ ] Add slopes
* [ ] Add rocks
* [ ] Add trees and vegetation
* [ ] Test navigation on rough terrain
* [ ] Evaluate localization on challenging terrain

### Hardware Transfer

* [ ] Validate ROS 2 interfaces with real sensors
* [ ] Integrate real LiDAR
* [ ] Integrate real depth camera
* [ ] Validate wheel odometry
* [ ] Validate TF calibration
* [ ] Perform real-world navigation tests

---

# 📁 Repository Structure

```text
atv-ugv-ros2/
│
├── src/
│   ├── atv_ugv_description/
│   │   ├── launch/
│   │   ├── urdf/
│   │   ├── worlds/
│   │   └── config/
│   │
│   ├── atv_ugv_navigation/
│   │   ├── launch/
│   │   ├── config/
│   │   └── maps/
│   │
│   └── atv_ugv_gazebo_sync/
│
├── maps/
│   ├── atv_map.yaml
│   └── atv_map.pgm
│
├── teleop_bridge.py
│
└── .gitignore
```

---

# 🚀 Running the Simulation

Clone the repository:

```bash
git clone https://github.com/anandgawai123456-glitch/atv-ugv-ros2.git
cd atv-ugv-ros2
```

Build the workspace:

```bash
colcon build --symlink-install
```

Source ROS 2 and the workspace:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

Launch the simulation:

```bash
ros2 launch atv_ugv_navigation sim_bringup.launch.py
```

---

# 🧪 Development Philosophy

The project is being developed incrementally:

```text
Robot Model
     ↓
Gazebo Simulation
     ↓
Sensor Integration
     ↓
Odometry + TF
     ↓
LiDAR Perception
     ↓
SLAM
     ↓
Map Generation
     ↓
Localization
     ↓
Nav2
     ↓
Costmap Tuning
     ↓
Obstacle Avoidance
     ↓
Depth Perception
     ↓
Outdoor / Jungle Terrain
     ↓
Real-World Hardware
```

The objective is not only to make the robot navigate in simulation, but to build a navigation architecture that can eventually be transferred to a physical ATV/UGV platform.

---

# 👨‍💻 Author

**Anand Gawai**

Electrical Engineering | Robotics Software | ROS 2 | Autonomous Navigation

GitHub:
https://github.com/anandgawai123456-glitch
