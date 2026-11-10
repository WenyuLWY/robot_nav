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

hdl_localization

DLO https://github.com/vectr-ucla/direct_lidar_odometry

DLO_ROS2 https://github.com/Cardinal-Space-Mining/direct_lidar_odometry

DLIO https://github.com/vectr-ucla/direct_lidar_inertial_odometry

fastlio https://github.com/hku-mars/FAST_LIO

FAST_LIO_SLAM 加入ScanContext，添加SC-PGO模块

FAST_LIO_LC的作者yanliang-wang 回环检测的优化结果，更新到FAST-LIO2的当前帧位姿中，幷进行ikdtree的重构，进而更新submap

FAST_LIO_SAM：将LIO-SAM的后端GTSAM优化部分移植到FAST-LIO2的代码中

rko_lio https://github.com/PRBonn/rko_lio

Ultra-Fusion https://github.com/sjtuyinjie/Ultra-Fusion

Voxel-SLAM https://github.com/hku-mars/Voxel-SLAM

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

## 后端优化

fej问题: 一个状态（或地标）在 t1被初始化、在 tk又被重新观测. 比如VIO 里本来不可观的全局平移和 yaw 会"看起来可观"，滤波器虚假地获得信息，协方差被压得过小，最终过度自信、拒绝修正、发散。



主要是基于滤波的方案+带边际化的滑窗优化（边际化 + 后续重新线性化）

纯批量 BA / 全窗口因子图，固定初始姿态：基本没有;


可观性：某个状态量，能不能只靠“传感器测量 + 运动模型”唯一确定。如果改了它、但所有残差/测量值完全不变 → 它就是“不可观”的。比较好理解：其实就是无法获取绝对信息的维度。比如单目里的深度。xyz rpy不可观，是因为不知道在全局地图的位置，因此无法。如果固定第一帧，则“相对”可观了，除非引入gps一类的绝对信息才可以可观。

退化场景下可观和运动激励有关。如匀速直线：yaw 没旋转激励，尺度/横向位置约束弱 → 漂移。纯旋转：深度、尺度难观。无人机悬停：加速度恒为 g → 尺度不可分。丰富运动（加减速+多轴转动）：更多状态变可观。

如果本来不可观的量如 yaw 被“假可观”，协方差被错误缩小，系统“过度自信”，实际在漂。在不考虑全局地图或gps的典型slam里，一定有4个量不可观，xyz和yaw。把机器人+地图一起平移任意向量 → 观测不变；把机器人+地图一起绕重力轴转任意 yaw → 观测不变；这就是不可观。理想环境下，LIO + GPS + 磁力计 = 所有量都可观。

roll和pitch会因为引入重力而可观。想象你闭眼站在黑屋子里，手里拿个重锤（加速度计）：头向左歪：重锤在手里偏向右侧 → 你知道“我横滚了”；头向前低：重锤往前拉 → 你知道“我俯仰了”；原地转圈（绕竖直轴）：重锤一直垂直向下 → 你不知道自己面朝哪。这就是 roll/pitch 可观、yaw 不可观的物理本质。

不可观不代表这个维度不准确，可观也不代表就这个量就绝对准确。可观性 ≠ 不估计。不可观也要存这个变量，比如 VIO 里照样优化 $x,y,z,\text{yaw}$。优化的是相对增量（帧间运动）。不可观的是绝对偏置。不可观的维度，协方差会随着时间逐渐增大，这就是累计误差产生的原因。比如lio系统允许一段时间后，如果过程中使用严格的滤波器去估计，roll和pitch的协方差由于imu引入就会很小，而xyz和yaw会的协方差会逐渐增大发散。

如果由于fej导致一个量被“错误可观”，也就是协方差很小，那么轨迹就会出现偏差。fej的目的就在于真实准确的估计协方差（哪怕xyz和yaw不可观，也要明确知道协方差具体的大小，也就是到底有多不准，有多不可观）。

VIO位姿图中的回环闭合修正应该只调整航向角+平移（如VINS-Mono所做的那样）——扭曲roll/pitch会破坏重力已经使其可观测的方向。评估VIO系统相对于真值的表现应使用4自由度（航向角+平移）对齐方式，而不是适用于纯视觉里程计的6自由度或7自由度（Sim(3)**S**im**(**3**)**）对齐方式。在没有回环检测或绝对参考（GPS、先验地图）的情况下，沿全局x,y,z和yuaw方向的不确定性应该无限增长；一个报告yaw不确定性在缩小的滤波器,是在告诉你它并不一致，而不是它更准确。

做法：保留状态，但正确维护零空间（FEJ 做的）。yaw/x/y/z 继续作为优化变量。用首次估计雅可比（FEJ）固定线性化点。保证 Hessian 零空间维度不被破坏。协方差自然趋于大值，但不干扰可观量。或者人为固定其中一个（比如第一帧 yaw = 0）。但明确知道这是任意约定，不是估计出来的。所有后续输出都相对于这个约定系。

## Hybrid Planning

工作1，跨地形、跨楼层的混合导航

- Continuous Planning：平地、坡道、楼梯上的连续运动规划
- 
- Discrete Planning：电梯、门、楼层切换等离散状态规划

## 空间表示

scene graph

S-Graphs+: Real-time Localization and Mapping leveraging Hierarchical Representations

https://github.com/snt-arg/lidar_situational_graphs
