# Running VIO on Jackal
##### Author: Saina Rezvani (saina.r6@gmail.com, srezvani@wpi.edu)
##### Presentation can be found [Here](https://docs.google.com/presentation/d/1mA3TWaiyB9V24z-W7W0Zaq33_DxgVm4Up-m9AwFyCLQ/edit?usp=sharing)
###### Last updated on Sept 18th, 2019

#### Packages

- updated firmware on D435i
- librealsense
- OpenCV (installation script is in the utility folder)
- Ceres
- Pangolin
- Camodocal (instrinsic calibration only and not as good as kalibr)
- Evo (trajectory visualization)

#### ROS Packages

- realsense-ros (librealsense ros wrapper)
- ddynamic_reconfigure (realsense requirement)
- image_pipeline (decompressing images)
- Vins-Fusion
- Kalibr (calibration)
- code_util(requirement for imu_util)
- imu_util (imu calibration)
- robot_localization (EKF)


### Collecting Data with Jackal
    
Realsense D435i and T265:
In order to launch the realsense camera and imu, the camera should be installed on the robot and
the launch files in the Realsense folder should be moved to the realsense-ros folder in catkin workspace
    
        $ roslaunch realsense2_camera rs_camera_d435i_t265.launch

Launching joystick, wheel encoder, 3dm IMU:

        $ drive

Launching vicon:

        $ roslaunch vicon trakcer.launch

The file t265_rosbag_cmd.sh in the utility folder includes all the necessary topics for recording the d435i camera, the two imu topics, encoder, vicon and some other useful topics.

**Do not play the bag files when drive is running or else jackal will start to climb the desk

#### Bag Files

There are two bag files that have been recorded with the most updated version of firmware and linbrealsense. The links to them are:
        
- Driving Jackal with its normal speed around vicon. This bag files include realsense cameras, imu, 3dm imu, vicon and wheel odometry
    - [jackal_viconspace_slow.bag](https://drive.google.com/file/d/1sYsLxxQK4xXeZ2eT8oC1rTMDJ9iRvvsF/view?usp=sharing)

- Driving Jackal with its highest speed around vicon. This bag files include realsense cameras, imu, 3dm imu, vicon and wheel odometry
    - [jackal_viconspace_fast.bag](https://drive.google.com/file/d/1Sj_o6rLlZ8asjuD_INz8Q8w4T9Vs7vZe/view?usp=sharing)

- The slow bag file mentioned above with certain transforms removed so it can be run with ekf
    - [ekf_jackal_viconspace_slow.bag](https://drive.google.com/file/d/1sNZpI5NwlZFr0Y0Gnzkj7Kvy9_LBqBDY/view?usp=sharing)

- The fast bag file mentioned above with certain transforms removed so it can be run with ekf
    - [ekf_jackal_viconspace_fast.bag](https://drive.google.com/file/d/1v4F5ocN3PDI-fmBtvf-nsM0RgnOoJGDh/view?usp=sharing)

### Calibration

For calibration, first the camera needs to be calibrated (instrinsic parameters) and then the camera and imu (extrinsic parameters).

###### (Taken from Kalibr's Wiki)
**Supported Projection Models:**

- pinhole camera model (pinhole)\
    (*intrinsics vector: [fu fv pu pv]*)
- omnidirectional camera model (omni)\
    (*intrinsics vector: [xi fu fv pu pv]*)
- double sphere camera model (ds)\
    (*intrinsics vector: [xi alpha fu fv pu pv]*)
- extended unified camera model (eucm)\
    (*intrinsics vector: [alpha beta fu fv pu pv]*)

**Supported Distortion Models:**

- radial-tangential (radtan)\
    (*distortion_coeffs: [k1 k2 r1 r2]*)
- equidistant (equi)\
    (*distortion_coeffs: [k1 k2 k3 k4]*)
- fov (fov)\
    (*distortion_coeffs: [w]*)
- none (none)\
    (*distortion_coeffs: []*)


Intrinsic calibration: 

        $ kalibr_calibrate_cameras --bag [filename.bag] --topics [TOPIC_0 ... TOPIC_N] --models [MODEL_0 ... MODEL_N] --target [target.yaml]

**The checkboard config/info file can be found in the utility folder

Extrinsic calibration:

        $ kalibr_calibrate_imu_camera --bag [filename.bag] --cam [camchain.yaml] --imu [imu.yaml] --target [target.yaml]

**The D435i, T265 and 3dm intrinsic IMU calibration files can be found in the utility/imu_intrinsics folder
**One possible error could be that the default syncronization tolarance is too low. In that case you can use the "--approx-sync" parameter with a value higher than 0.02 (default)

For more information refer to the imu_util and Kalibr's wiki pages.

### VINS-Fusion

For Running Vins-Fusion refer to the read me in the forked repo in mit-acl github repo which can also be found as a submodule in this repository 

### EKF

Running EKF:

    $ roslaunch jackal_odometry jackal_odometry.launch

Running EKF and Vins-Fusion:

    $ rosrun vins vins_node ~/catkin_ws/src/VINS-Fusion/config/realsense_d435i/realsense_stereo_imu_config_3.yaml
    $ roslaunch jackal_odometry jackal_odometry_vins.launch

**The rviz config file is in the launch folder and can be uploaded into rviz

### Visualization

#### Evo:

For running the tum format, the text files can be generated with the generate_txtfile_from_topic.py and the following command: (more info on evo wiki page)

        $ evo_traj tum traj_1.txt traj_2.txt --ref traj_3.txt --p

#### Visualizing vicon:

The script `/EKF/scripts/createpath.py` can be used to visualize the vicon trajectory in rviz




    
