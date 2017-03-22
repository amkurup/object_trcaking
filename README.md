# Readme file for EE5900 project_6

### Group
[Akhil](mailto:amkurup@mtu.edu) (team lead)
[Prithvi](mailto:pkambham@mtu.edu)
[Aswin](mailto:ajayapra@mtu.edu)


This document describes how to download the package and use it. For details on the algorithm please refer to the [wiki](https://github.com/amkurup/object_trcaking/wiki)


1. If not already installed, install the camera package in ROS 
```

$ sudo apt-get install ros-indigo-usb-cam

```
2. If not already installed,  install opencv
```

$ sudo apt-get install libopencv-dev python-opencv
```

3. Clone this git repository
```
$ git clone git@github.com:amkurup/object_trcaking.git
```

4. change working directory to the clones repository
```
cd <path to repository> 
```

5. Source the path variable and the remote jackal script (we have used jackal3)
```
$ source devl/setup.bash
$ source remote-jackal.sh jackal3
```

6. Launch the joystick launch file
```
$ roslaunch object_tracking joystick.launch
```
(All other launch files are for individual modules and need not be used! They were/will be used for debugging or testing individual modules)

7. To start the tracking code, press the circle on the joystick. You should be able to press the X on the joystick and stop the tracking at any point in time and restart it using the circle.


