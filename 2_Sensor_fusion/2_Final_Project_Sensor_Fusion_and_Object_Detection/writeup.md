# Writeup: Track 3D-Objects Over Time

Please use this starter template to answer the following questions:

### 1. Write a short recap of the four tracking steps and what you implemented there (filter, track management, association, camera fusion). Which results did you achieve? Which part of the project was most difficult for you to complete, and why?

In the EKF (Extended Kalman Filter) step, basically I used Kalman Filter to predict objects' state, which includes their position and velocity in 3D space, and then update their state from the sensor measurements. The sensor could be a camera, a LiDAR or even a Radar. 

To execute Kalman filter, I implemented the `predict` and `update` method, and its related method such as `get_hx`, `get_H` method. By this code, I could firstly predict the state of object, which are the mean and the variance of its state, and update its state with the sensor measurements. To update the state with measurements, it is neccessary to convert the coordinates from vehicle coordinate to sensor coordinate and that is the reason why `get_hx` or `get_H` method is needed. 

By the way, the original Kalman filter assumes that the system is a linear system. However, if we convert the state coordinate from vehicle to camera sensor, non-linear transformation has to be done. Thus, this is why EKF (Extended Kalman Filter) is released which approximates non-linear system as linear system using a Talyor series expansion.

In the track management step, firstly it is needed to initialize a new track with its state("initialized") and score. And then, as the ego vehicle runs, the track is literally tracked based on EKF result. The track score should decrease if the track is not detected in the last several frames and the track should be deleted if it's score is below a threshold or it's variance is larger than variance threshold. The track state is needed to keep "confirmed" if the track keeps detected by sensors.

For the track management class, first of all, I implement the `manage_tracks` method to decrease the score for unassigned tracks and then decided the score threshold and variance threshold to delete the old and useless tracks. In addition, by the `handle_updated_track` method, I could increase the track score and set track state to "tentative" or "confirmed" based on my own threshold.

A matching process between the existing tracks and the new measurements from sensors is done in the association step. To do this, I used SNN, which denoted for Single Nearest Assiciation to associate the tracks and the measurements and to calculate the distance between tracks and measurements, Mahalanobis distance is used that can reflect not only the actual distance bus also the variance of tracks. 

By the `associate` methed in the code, a `association_matrix` is implemented between tracks and measurements by calulating the Malalanobis distance and gating the irrelevant matchings. After this, the closest track and measurement are returned by `get_closest_track_and_meas` method and then `update` method is executed.

Finally, in the camera fusion step, it is neccessary to implement the non-linear system, since the transformation from 3D space, which is a real world, to 2D image space is non-linear. To do this, I wrote the `get_hx` method for the camera transformation.

By implementing all of the codes above, I could finally initialize new tracks from sensor detections, keep tracking them by their track score and state, and decide whether to keep them on the tracking list or delete and not to track.

The most difficult part of this project for me was understanding the whole system of object tracking process. To overcome this, I structurized each element such as `Trackmanagement` and `Association` of the system by writing down them on a large paper and tried to see them in a whole picture. By this, I could clearly realize the whole system so that it was easy to implement each element.


### 2. Do you see any benefits in camera-lidar fusion compared to lidar-only tracking (in theory and in your concrete results)? 

I think there are many benefits in camera-lidar fusion compared to lidar-only tracking. First of all, I could see many ghost tracks when I only used the lidar-only tracking sytem in this project, but they decreased dramastically when camera measurements were added for the tracking. Also, when it comes to false negative case, the probability that the sensor cannot detect the object, which could be critical, will decrease if camera-lidar fusion is used since the object that is difficult to be detected by the lidar can be easily detected by the camera.


### 3. Which challenges will a sensor fusion system face in real-life scenarios? Did you see any of these challenges in the project?

In my opinion, one of the most challenging and dangerous situations in real-life scenarios is a false negative case. Obviously, by the sensor fusion system, which leverages several sensors such as camera, radar, and lidar and they can compensate each other's drawbacks, the false negative cases will rarely happen but it does not mean 0. Additionally, Association step can be problematic since heuristic methods for the distance measurement are typically used and they sometimes might not accurate.


Associating measurements with tracks can be difficult. In a situation with many vehicles or other objects to track, the heuristics we use to assign measurements to tracks may break down. Additionally, in situations where one or the other sensor is failing to detect an object in the scene, that object's tracking may never become confirmed. There are also situations where one or the other sensor might perform more or less poorly. For example, cameras may perform poorly at night while lidar might perform poorly in inclement weather. We didn't see any of these particular situations in our project, but its not hard to imagine these types of situations arising in real-world conditions.


### 4. Can you think of ways to improve your tracking results in the future?

As recently I started working in the field of V2X communication, V2X messages can be one of the options to improve tracking results because the tracking information can be supplemented from the information of other vehicles or infrastructures by V2V or V2I messages. Another way to improve tracking results is to improve the detection results. Good detection results mean that we can strongly believe the measurements so that we can depend more on measurements rather than predictions and it would be better since measurements are more accurate than prediction results.