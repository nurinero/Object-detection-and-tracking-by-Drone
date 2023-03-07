# Object Detection and Tracking by Drone
This project aims to develop a system for real-time object detection and tracking using a drone, with a dashboard to visualize the object's movement and collect data. The system employs various technologies, including Python, NumPy, Pandas, TensorFlow, OpenCV, YOLOv8, TELLO PostgreSQL, Matplotlib, Seaborn, Plotly, and Streamlit.

## Features
The following features are implemented in this project:

* `Object detection and tracking`: The system can detect and track objects in real-time using a drone. The object detection is performed using the YOLOv8 algorithm.
* `Optimized drone movement`: The drone movement is optimized in real-time using a PID control system to ensure smooth and accurate tracking of the object.
* `Object information collection`: The system collects information about the detected object and saves images to a PostgreSQL database.
* `Dashboard interface`: The system provides a real-time visualization of object movement and drone response through a dashboard interface. The dashboard is implemented using Streamlit, Matplotlib, Seaborn, and Plotly.

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
## Usage
To use this project, follow the steps below:

1.Clone the repository to your local machine.
2.Install the required technologies listed above.
3.Connect to the TELLO drone.
4.Run the main script using the command: `python main.py`.
5.Open the dashboard interface by navigating to http://localhost:7777/ in your web browser.
## Conclusion
This project demonstrates the development of a real-time object detection and tracking system using a drone. The system provides a dashboard interface to visualize the object's movement and collect data. The system can be further improved by implementing additional features such as multiple object tracking, object classification, and video recording.
