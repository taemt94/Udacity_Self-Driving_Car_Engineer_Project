# Udacity Self-Driving Car Engineer

## Introduction
Self-Driving Car Engineer Nanodegree program is one of the prominent programs in Udacity that provides skills and techniques used by self-driving car teams at the most advanced technology companies in the world. 

By this program, I have learnt the techniques that power self-driving cars across the full stack of a vehicle’s autonomous capabilities. Specifically, there are 5 courses, which are *Computer Vision, Sensor Fusion, Localization, Planning* and *Control*. During each course, I learnt the basic theory of each technology and completed one or more projects. In this repository, I organized all projects and the brief explanation is under below.

---
## Project 1. Object Detection in an Urban Environment

- This project is to train deep learning models for object detection using Waymo dataset, which is the real world dataset.
By this project, I could practice how to use Tensorflow Object Detection API and train different types of deep learning models under various hyperparameters to improve detection performance on the Waymo dataset.
- You can find the analysis of the dataset and the training results at [this page](./1_Object_Detection_in_an_Urban_Environment/submission.md).
- Main Tools : Python, Tensorflow

## Project 2-1. 3D Object Detection

- In this project, a deep-learning approach is used to detect vehicles in LiDAR data based on a birds-eye view perspective of the 3D point-cloud. Also, a series of performance measures is used to evaluate the performance of the detection approach.
- You can find the write-up of this project including the detection results and metrics plot [here](./2_Sensor_fusion/1_Mid-Term_Project_3D_Object_Detection/student/writeup.md).
- Main Tools : Python, Pytorch

## Project 2-2. Sensor Fusion and Object Tracking

- In this project, I could learn how to fuse measurements from LiDAR and camera and track vehicles over time. Using real-world data from the Waymo Open Dataset, the algorithm detects objects in 3D point clouds and applies an extended Kalman filter for sensor fusion and tracking over time, based on the lidar detections fused with camera detections. Data association and track management are implemented as well.
- The tracking result and answers for writeup questions are [here](./2_Sensor_fusion/2_Final_Project_Sensor_Fusion_and_Object_Detection/writeup.md).
- Main Tools : Python, Pytorch


## Project 3. Localization
- This project is intended to localize a ego vehicle driving in CARLA simulator. It use a LiDAR point cloud for localization and a point cloud map is given so it is not a SLAM system but more like just localization. `ICP` or `NDT` matching algorithm are used to get the vehicle's position in the given map and the goal is to localize the vehicle for at least 170m from the starting point within a distance pose error of 1.2m.
- You can find the result videos (ICP, NDT) from [here](3_Localization/Result.md). 

## Project 4. Motion Planning and Decision Making for Autonomous Vehicles
- In this project, the Behavior Planner and the Motion Planner are implemented.
- The Behavior Planner uses FSM (Finite State Machine) as its planning logic and the ego vehicle needs to avoid crashing with the static objects under the FSM.
- The Motion Planner generates path and trajectory using cubic spirals and selects the best trajectory through a cost function evaluation.
- The result of a driving scenario that the ego vehicle avoids static obstacles while driving are [here](4_Motion_Planning_and_Decision_Making_for_Autonomous_Vehicles/README.md).


## Project 5. Control and Trajectory Tracking for Autonomous Vehicles
- In this project, a PID controller is designed in order to perform vehicle trajectory tracking. Given a trajectory as an array of locations, a PID controller controls an ego vehicle and its efficiency is tested on the CARLA simulator used in the industry.
- Two PID controllers, in which one is for steering and the other one is for throttling, are built so that the ego vehicle follows the trajectory generated from the Motion Planner.
- The parameters, $K_P, K_I, K_D$, are tuned to drive without any collision in the scenario.
- You can find [a result video and a writeup](5_Control_and_Trajectory_Tracking_for_Autonomous_Vehicles/README.md) that includes detailed analysis of a tuning PID parameters process.