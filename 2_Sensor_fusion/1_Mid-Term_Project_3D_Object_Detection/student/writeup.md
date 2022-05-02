# Sensor Fusion Mid-term Project
## Step 1 Part 2
This report is for sensor fusion mid-term project and there are two items that needed to be included.
1. Find and display 10 examples of vehicles with varying degrees of visibility in the point-cloud
2. Identify vehicle features that appear as a stable feature on most vehicles (e.g. rear-bumper, tail-lights) and describe them briefly. Also, use the range image viewer from the last example to underpin your findings using the lidar intensity channel.

These tasks will be resolved under below.
1. Find and display 10 examples of vehicles with varying 
degrees of visibility in the point-cloud
    - To do this task, firstly I used open3d visualizer to inpect point clouds in different view point and captured the visualization of them.
    - The images of point cloud in different view point are under below.
![image 1-1](examples/1-1.PNG)
![image 1-2](examples/1-2.PNG)
![image 2-1](examples/2-1.PNG)
![image 2-2](examples/2-2.PNG)
![image 3-1](examples/3-1.PNG)
![image 3-2](examples/3-2.PNG)
![image 4-1](examples/4-1.PNG)
![image 4-2](examples/4-2.PNG)
![image 5-1](examples/5-1.PNG)
![image 5-2](examples/5-2.PNG)
![image 6-1](examples/6-1.PNG)
![image 6-2](examples/6-2.PNG)
![image 7-1](examples/7-1.PNG)
![image 7-2](examples/7-2.PNG)
![image 8-1](examples/8-1.PNG)
![image 8-2](examples/8-2.PNG)
![image 9-1](examples/9-1.PNG)
![image 9-2](examples/9-2.PNG)
![image 10-1](examples/10-1.PNG)
![image 10-2](examples/10-2.PNG)

2. Identify vehicle features that appear as a stable feature on most vehicles (e.g. rear-bumper, tail-lights) and describe them briefly. Also, use the range image viewer from the last example to underpin your findings using the lidar intensity channel.
    - To accomplish this task, I used the last example of the third sequence data and found proper vehicles that can be easily identified.
    - I attached the images of identified vehicle features in point cloud as well as the intensity channel of the same vehicle.
![image 2-1-1](examples/2-1-1.PNG)
![image 2-1-2](examples/2-1-2.PNG)
![image 2-2-1](examples/2-2-1.PNG)
![image 2-2-2](examples/2-2-2.PNG)
    - In the first image, I could identify the head-light and front bumper by the shape of point cloud.
    - In the seconde image, Front tire, Rear tire, Rear bumper and side window can be visible in the point cloud.
    - Interestingly, because laser from Lidar can penetrate the side window that is usually transparent, there are very few reflected points representing the window so it can be easily identified.

- Every images are in `examples/`