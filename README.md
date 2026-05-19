# Autoware - the world's leading open-source software project for autonomous driving

![Autoware_RViz](https://user-images.githubusercontent.com/63835446/158918717-58d6deaf-93fb-47f9-891d-e242b02cba7b.png)
[![Discord](https://img.shields.io/discord/953808765935816715?label=Autoware%20Discord&style=for-the-badge)](https://discord.gg/Q94UsPvReQ)

Autoware is an open-source software stack for self-driving vehicles, built on the [Robot Operating System (ROS)](https://www.ros.org/). It includes all of the necessary functions to drive an autonomous vehicles from localization and object detection to route planning and control, and was created with the aim of enabling as many individuals and organizations as possible to contribute to open innovations in autonomous driving technology.

![Autoware architecture](https://static.wixstatic.com/media/984e93_552e338be28543c7949717053cc3f11f~mv2.png/v1/crop/x_0,y_1,w_1500,h_879/fill/w_863,h_506,al_c,usm_0.66_1.00_0.01,enc_auto/Autoware-GFX_edited.png)

## Documentation

To learn more about using or developing Autoware, refer to the [Autoware documentation site](https://autowarefoundation.github.io/autoware-documentation/main/). You can find the source for the documentation in [autowarefoundation/autoware-documentation](https://github.com/autowarefoundation/autoware-documentation).

## Repository overview

- [autowarefoundation/autoware](https://github.com/autowarefoundation/autoware)
  - Meta-repository containing `.repos` files to construct an Autoware workspace.
  - It is anticipated that this repository will be frequently forked by users, and so it contains minimal information to avoid unnecessary differences.
- [autowarefoundation/autoware_common](https://github.com/autowarefoundation/autoware_common)
  - Library/utility type repository containing commonly referenced ROS packages.
  - These packages were moved to a separate repository in order to reduce CI execution time
- [autowarefoundation/autoware.core](https://github.com/autowarefoundation/autoware.core)
  - Main repository for high-quality, stable ROS packages for Autonomous Driving.
  - Based on [Autoware.Auto](https://gitlab.com/autowarefoundation/autoware.auto/AutowareAuto) and [Autoware.Universe](https://github.com/autowarefoundation/autoware.universe).
- [autowarefoundation/autoware.universe](https://github.com/autowarefoundation/autoware.universe)
  - Repository for experimental, cutting-edge ROS packages for Autonomous Driving.
  - Autoware Universe was created to make it easier for researchers and developers to extend the functionality of Autoware Core
- [autowarefoundation/autoware_launch](https://github.com/autowarefoundation/autoware_launch)
  - Launch configuration repository containing node configurations and their parameters.
- [autowarefoundation/autoware-github-actions](https://github.com/autowarefoundation/autoware-github-actions)
  - Contains [reusable GitHub Actions workflows](https://docs.github.com/ja/actions/learn-github-actions/reusing-workflows) used by multiple repositories for CI.
  - Utilizes the [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) concept.
- [autowarefoundation/autoware-documentation](https://github.com/autowarefoundation/autoware-documentation)
  - Documentation repository for Autoware users and developers.
  - Since Autoware Core/Universe has multiple repositories, a central documentation repository is important to make information accessible from a single place.

## Using Autoware.AI

If you wish to use Autoware.AI, the previous version of Autoware based on ROS 1, switch to [autoware-ai](https://github.com/autowarefoundation/autoware_ai) repository. However, be aware that Autoware.AI has reached the end-of-life as of 2022, and we strongly recommend transitioning to Autoware Core/Universe for future use.

## Minimal RViz Manual Controller

For speed and steering demos, Autoware's RViz manual controller can be built without importing the full Autoware workspace. Use `manual-controller.repos` to import only the RViz panel package and the message packages it needs.

```bash
sudo apt update
sudo apt install python3-vcstool python3-rosdep python3-colcon-common-extensions ros-humble-rviz2
sudo rosdep init 2>/dev/null || true
rosdep update
mkdir -p ~/manual_controller_ws/src
cd ~/manual_controller_ws
source /opt/ros/humble/setup.bash
vcs import src < /path/to/autoware/manual-controller.repos
rosdep install --from-paths \
  src/core/autoware_cmake \
  src/core/autoware_msgs/autoware_common_msgs \
  src/core/autoware_msgs/autoware_control_msgs \
  src/core/autoware_msgs/autoware_planning_msgs \
  src/core/autoware_msgs/autoware_vehicle_msgs \
  src/core/autoware_utils/autoware_utils_rclcpp \
  src/universe/external/tier4_autoware_msgs/tier4_control_msgs \
  src/universe/external/tier4_autoware_msgs/tier4_external_api_msgs \
  src/tools/autoware_tools/common/tier4_control_rviz_plugin \
  --ignore-src -r -y
colcon build --symlink-install --packages-up-to tier4_control_rviz_plugin --cmake-args -DBUILD_TESTING=OFF
source install/setup.bash
rviz2
```

In RViz, open `Panels` -> `Add New Panel`, select `rviz_plugins/ManualController`, and press `OK`. To load it automatically from an RViz config, add this entry under `Panels`:

```yaml
- Class: rviz_plugins/ManualController
  Name: ManualController
```

The panel publishes:

- `/external/selected/control_cmd` (`autoware_control_msgs/msg/Control`)
- `/external/selected/gear_cmd` (`autoware_vehicle_msgs/msg/GearCommand`)
- `/control/gate_mode_cmd` (`tier4_control_msgs/msg/GateMode`) when `Enable Manual Control` is pressed

It also reads status from `/control/current_gate_mode`, `/vehicle/status/velocity_status`, `/api/autoware/get/engage`, and `/vehicle/status/gear_status`. For a minimal demo without the full Autoware gate, publish these status topics yourself or leave the status labels as `INIT`; speed and steering commands are still published after setting a cruise velocity or steering angle.

When using this with MCAV's `sd_vehicle_interface`, start RViz with a remap so the panel writes to the interface input:

```bash
rviz2 --ros-args -r /external/selected/control_cmd:=/control/command/control_cmd
```

If RViz is already running, relay the panel's selected control command instead:

```bash
sudo apt install ros-humble-topic-tools
ros2 run topic_tools relay \
  /external/selected/control_cmd \
  /control/command/control_cmd
```

The manual panel computes acceleration from `/vehicle/status/velocity_status`. If no vehicle velocity publisher is running, provide a simple zero-speed status for bench tests:

```bash
ros2 topic pub /vehicle/status/velocity_status autoware_vehicle_msgs/msg/VelocityReport \
  "{longitudinal_velocity: 0.0, lateral_velocity: 0.0, heading_rate: 0.0}" -r 10
```

## Contributing

- [There is no formal process to become a contributor](https://github.com/autowarefoundation/autoware-projects/wiki#contributors) - you can comment on any [existing issues](https://github.com/autowarefoundation/autoware.universe/issues) or make a pull request on any Autoware repository!
  - Make sure to follow the [Contribution Guidelines](https://autowarefoundation.github.io/autoware-documentation/main/contributing/).
  - Take a look at Autoware's [various working groups](https://github.com/autowarefoundation/autoware-projects/wiki#working-group-list) to gain an understanding of any work in progress and to see how projects are managed.
- If you have any technical questions, you can start a discussion in the [Q&A category](https://github.com/autowarefoundation/autoware/discussions/categories/q-a) to request help and confirm if a potential issue is a bug or not.

## Useful resources

- [Autoware Foundation homepage](https://www.autoware.org/)
- [Support guidelines](https://autowarefoundation.github.io/autoware-documentation/main/support/support-guidelines/)
