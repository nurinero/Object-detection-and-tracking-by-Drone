# Object Detection and Tracking by Drone
This project aims to develop a system for real-time object detection and tracking using a drone, with a dashboard to visualize the object's movement and collect data. The system employs various technologies, including [Python](https://www.python.org/), [NumPy](https://github.com/numpy/numpy), [Pandas](https://github.com/pandas-dev/pandas), [TensorFlow](https://github.com/tensorflow/tensorflow), [OpenCV](https://github.com/opencv/opencv), [YOLOv8](https://github.com/ultralytics/ultralytics), [TELLO](https://github.com/dji-sdk/Tello-Python) [PostgreSQL](https://github.com/postgres/postgres), [Matplotlib](https://github.com/matplotlib/matplotlib), [Seaborn](https://github.com/mwaskom/seaborn), [Plotly](https://github.com/plotly), and [Streamlit](https://github.com/streamlit).

## Features
The following features are implemented in this project:

* `Object detection and tracking`: The system can detect and track objects in real-time using a drone. The object detection is performed using the YOLOv8 algorithm.
* `Optimized drone movement`: The drone movement is optimized in real-time using a PID control system to ensure smooth and accurate tracking of the object.
* `Object information collection`: The system collects information about the detected object and saves images to a PostgreSQL database.
* `Dashboard interface`: The system provides a real-time visualization of object movement and drone response through a dashboard interface. The dashboard is implemented using Streamlit, Matplotlib, Seaborn, and Plotly.
![BMTD Features](/videos/BMTD.gif)
![flow diagram](/videos/flow_diagram.gif)
![fWind mill](/videos/Wind_mill.jpg)

## Requirements
The following technologies are required to run this project:

* Python 3.x
* NumPy
* Pandas
* TensorFlow
* OpenCV
* YOLOv8
* TELLO
* PostgreSQL
* Matplotlib
* Seaborn
* Plotly
* Streamlit
![Uesed technologies](/videos/Used_Technologies.jpg)

## Usage
To use this project, follow the steps below:

1. Clone the repository to your local machine.
2. Install the required technologies listed above.
3. Connect to the TELLO drone.
4. Run the main script using the command: `python main.py`.
5. Open the dashboard interface by navigating to http://localhost:7777/ in your web browser.

![dashboard interface runing](/videos/short_dashboard.gif)
## The dashboard interface
The dashboard interface of this project is designed to provide users with complete control over the drone and real-time data visualization capabilities. The interface is divided into three main sections: Real-Time AutoControl System, Real-Time Dashboard, and Data_history_Dashboard. Let's take a closer look at each of these sections:

a. Real-Time AutoControl System: This section of the dashboard interface provides users with complete control over the drone's movement and tracking capabilities. The following tracking tasks are available:

Following Object: This feature allows the drone to follow a detected object in real-time. The user can select the object to track, and the drone will automatically adjust its position to keep the object in view.

Collecting Data: This feature allows the drone to collect data related to the object being tracked, such as its size, color, and movement patterns. This data is saved in a database for later analysis.

**1. Drone Configuration**: The drone configuration section provides users with various options related to drone control. The following features are available:

`Connect and check battery`: This feature allows users to connect to the TELLO drone and check its battery level, ensuring that the drone is ready for use.

`Activate the Streamon`: This feature allows the drone to stream video feed in real-time. The dashboard interface provides an option to activate the Streamon feature, which enables the user to monitor the drone's movements and the object detection in real-time.

`Activate the takeoff`: This feature allows the drone to take off and begin its mission. This feature is essential for real-time object detection and tracking, as it enables the drone to move and follow the detected object.

**2. Real-Time Dashboard**: This section of the dashboard interface provides users with real-time data visualization capabilities. The interface displays the object being tracked, the drone's current location, and other relevant data related to the object's movement and drone response. This feature enables users to monitor the system's performance in real-time and make adjustments as needed.

**3. Data_history_Dashboard**: This section of the dashboard interface provides users with historical data related to object detection and tracking. The interface displays data related to object movement and drone response over a specific period. This feature enables users to analyze the system's performance over time and make improvements as needed.

Overall, the dashboard interface of this project provides users with a comprehensive set of features related to drone control and real-time data visualization. The interface is designed to be user-friendly and intuitive, ensuring that users can take advantage of the full capabilities of the system.
![he dashboard interface](/videos/collecting_Data_task.gif)

## Conclusion
This project demonstrates the development of a real-time object detection and tracking system using a drone. The system provides a dashboard interface to visualize the object's movement and collect data. The system can be further improved by implementing additional features such as multiple object tracking, object classification, and video recording.
