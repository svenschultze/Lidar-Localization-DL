# LiDAR-Based Robot Localization with Deep Learning
*This project is the result of the course __Robotics 2__ at the University of Oldenburg.*

Authors: Dennis Lindt, Svenja Schuirmann, Sven Schultze

In many robotic systems, knowing the position of the robot is an essential requirement. It helps the system to understand how close it is to complete a task, and what to do next. There are two main approaches to robot localization: 1) using indoor positioning systems (IPS), and 2) using robot-mounted sensors such as light detection and ranging sensors (LiDAR) and odometry. IPS's make use of different technologies, such as signal beacons with fixed positions to triangulate the current position, or magnetic sensors that react to abnormalities in the magnetic field inside buildings. 

While these IPS's can reach high accuracy, they are often expensive and difficult to install. Because of this, robot-mounted systems are more commonly used. For example, a combination of LiDAR data and odometry can yield information about relative position changes over time, which can be used to create a map of the robot's environment.

An example for such a localization system is Simultaneously Localization and Mapping (SLAM). SLAM is stateful, meaning that it uses previous odometry, location and sensor data to make predictions about the robot's current location. Over time, the system generates a map of its surroundings, which allows it to recognize places it has visited before. However, this approach can lead to problems and errors when the robot is disturbed. For example, if a robot is moved, picked up or shifted in an unexpected way. Another source of error could be its dependency on odometry. Odometry is often inaccurate because it relies on assumptions about physical properties of the robot and the underground. This make measurements unreliable and can falsify the position of the robot on the map. This error can get incrementally worse. 

A stateless localization system is not prone to these errors. By using nothing but LiDAR data as input, the system does not consider its previous states to estimate the robot's location. Thus, the robot can be moved without issue. Further, the system does not depend on odometry, which is often faulty and leads to errors.
This project aims for a stateless localization system based on LiDAR data that uses a convolutional neural network as its backbone. The network extracts features from the LiDAR data, detecting walls, corners, and objects. Then, it estimates the robot's location based upon its findings.

*Read more in our [documentation](documentation/lidar_localization_documentation.pdf), or view our notebooks in Google Colab:*

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/svenschultze/Lidar-Localization-DL/)

