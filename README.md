# overview
https://github.com/SLAM-Handbook-contributors/slam-handbook-public-release.git

## sensor
全景rgbd

dreamvu

Ouster REV8

激光雷达
mid360

## 标定
https://github.com/Taeyoung96/GRIL-Calib

ROS1 https://github.com/hku-mars/LiDAR_IMU_Init

ROS2 https://github.com/hku-mars/LiDAR_IMU_Init

# 定位
# 里程计
DLO https://github.com/vectr-ucla/direct_lidar_odometry

DLO_ROS2 https://github.com/Cardinal-Space-Mining/direct_lidar_odometry

DLIO https://github.com/vectr-ucla/direct_lidar_inertial_odometry

fastlio https://github.com/hku-mars/FAST_LIO

rko_lio https://github.com/PRBonn/rko_lio

Ultra-Fusion https://github.com/sjtuyinjie/Ultra-Fusion

https://github.com/hku-mars/Voxel-SLAM
# 后端
https://github.com/koide3/glim

https://github.com/ganlumomo/VisualInertialOdometry

https://github.com/gisbi-kim/FAST_LIO_SLAM

https://github.com/manankharwar/fusioncore

# 建图 

# 地图形式
原始观测：点云地图

定位地图：Voxel Map/ ikdtree

规划地图：OctoMap /TSDF(https://github.com/ethz-asl/voxblox)/ ESDF/ elevation map / traversability map/ Visibility Graph/ 

Offline: https://github.com/xuankuzcr/Global-LVBA

mesh地图: https://github.com/uos/rmcl



# 地图保存、更新和利用
rtabmap
https://github.com/MOLAorg/mola
https://github.com/leggedrobotics/open3d_slam

# 图纸/BIM转地图
https://github.com/janstueh/LIO-BIM

https://github.com/HKUST-Aerial-Robotics/SLABIM

https://github.com/MigVega/Ogm2Pgbm

# SLAM 里程计和建图
Voxel-SLAM https://github.com/hku-mars/Voxel-SLAM

# 规划
## 导航框架
地面机器人：https://github.com/HongbiaoZ/autonomous_exploration_development_environment

四足：

https://github.com/jizhang-cmu/autonomy_stack_go2

无人机：

fast planner(voxel map)/ego planner/MRS UAV System(OctoMap)/Aerostack2

Trajectory Optimization	B-spline / Minimum Snap	生成平滑、可执行的轨迹

Trajectory Tracking	Position / Velocity Controller	跟踪期望轨迹

ros nav2

## 规划器
全局规划器：

Kinodynamic A*/hybrid a*/SmacPlannerLattice

局部规划器:

dwa/teb/MPPI Controller

特殊:

https://github.com/MichaelFYang/far_planner.git (use Visibility Graph)


## acitve loop

https://github.com/yzhangec/Exploration-with-Global-Consistency

https://github.com/IMRL/ActiveLoopClosure

# 未来
## Hybrid Planning

工作1，跨地形、跨楼层的混合导航

- Continuous Planning：平地、坡道、楼梯上的连续运动规划
- 
- Discrete Planning：电梯、门、楼层切换等离散状态规划

## 空间表示 
scene graph

S-Graphs+: Real-time Localization and Mapping leveraging Hierarchical Representations

https://github.com/snt-arg/lidar_situational_graphs
