##########

# README for running VIO on Jackal
# Author: Saina Rezvani (saina.r6@gmail.com)
# Sept 13th, 2019

##########

Packages:

- updates firmware on D435i
- librealsense
- OpenCV (installation script is in the utility folder)
- Ceres
- Pangolin
- Camodocal (instrinsic calibration only and not as good as kalibr)
- Evo (trajectory visualization)

ROS Packages:

- realsense-ros (librealsense ros wrapper)
- ddynamic_reconfigure (realsense requirement)
- image_pipeline (decompressing images)
- Vins-Fusion
- Kalibr (calibration)
- code_util(requirement for imu_util)
- imu_util (imu calibration)
- robot_localization (EKF)


##########

Collecting data with Jackal:
    
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

    There are two bag files that have been recorded with the most updated version of firmware and linbrealsense. The links to them are:
        
        - Driving Jackal with its normal speed around vicon. This bag files include realsense cameras, imu, 3dm imu, vicon and wheel odometry
            (https://drive.google.com/file/d/1sYsLxxQK4xXeZ2eT8oC1rTMDJ9iRvvsF/view?usp=sharing)
        
        - Driving Jackal with its highest speed around vicon. This bag files include realsense cameras, imu, 3dm imu, vicon and wheel odometry
            (https://drive.google.com/file/d/1Sj_o6rLlZ8asjuD_INz8Q8w4T9Vs7vZe/view?usp=sharing)
        
        - The slow bag file mentioned above with certain transforms removed so it can be run with ekf
            (https://drive.google.com/file/d/1sNZpI5NwlZFr0Y0Gnzkj7Kvy9_LBqBDY/view?usp=sharing)
        
        - The fast bag file mentioned above with certain transforms removed so it can be run with ekf
            (https://drive.google.com/file/d/1v4F5ocN3PDI-fmBtvf-nsM0RgnOoJGDh/view?usp=sharing)

##########

For calibrating camera and imu refer to the Kalibr and imu_util wiki pages
    - The D435i, T265 and 3dm intrinsic IMU calibration files can be found in the utility/imu_intrinsics folder
    - The checkboard config/info file can be found in the utility folder

##########

For Running Vins-Fusion refer to the read me in the forked repo in mit-acl github repo

##########

The script createpath.py can be used to visualize the vicon trajectory in rviz

##########

Running EKF:

    $ roslaunch jackal_odometry jackal_odometry.launch

Running EKF and Vins-Fusion:

    $ rosrun vins vins_node ~/catkin_ws/src/VINS-Fusion/config/realsense_d435i/realsense_stereo_imu_config_3.yaml
    $ roslaunch jackal_odometry jackal_odometry_vins.launch

    **The rviz config file is in the EKF/rviz folder and can be uploaded into rviz

##########

Running Evo:

    For running the tum format, the text files can be generated with the generate_txtfile_from_topic.py and the following command: (more info on evo wiki page)

        $ evo_traj tum traj_1.txt traj_2.txt --ref traj_3.txt --p


    