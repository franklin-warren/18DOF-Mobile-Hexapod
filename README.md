18DOF hexapod robot. Currently under construction, expected to be finished within a month or two. All code is a work in progress. <br>
Inserted are images/videos of the construction process, including photos of assembly, videos of legs moving, as well as CAD screenshots. <br>
Currently in the main programming stage of the design. <br>
<br>
Key points:<br>
	Derived and programmed a custom inverse kinematics engine in both leg-centric and bot-centric design <br>
	Derived and implemented a cycloidal step path to reduce power draw and servo strain <br>
	Designed a 3 layer PCB stackup to handle high-amp servo draw and sensitive sensor data simultaneously <br>
	Mass-computed 870 000 point leg reachability clouds in Python to assist in step planning <br>
	Implementing closed loop control with FSR step detection, real-time clearance sensor, and IMU. <br>
	Implementing LIDAR room scanning
	Current architecture is ESP32-Pi Zero W via UART, however, there are eventual plans for ROS2 integration

<br>
Video of two legs walking:<br>
https://github.com/user-attachments/assets/c0b8d58c-5718-43e7-b491-6766b3c93bf8
<br>

<img width="1259" height="941" alt="image" src="https://github.com/user-attachments/assets/576bdf7d-288b-41cf-b133-5b3795a55f39" />
<br>
CAD and renders:<br>
<img width="651" height="419" alt="image" src="https://github.com/user-attachments/assets/922ab4d3-6269-46b6-9e45-dcd7c38aa80e" />
<img width="951" height="569" alt="image" src="https://github.com/user-attachments/assets/aae51dc9-b644-4278-a934-e6d666de5cf3" />
<img width="631" height="685" alt="image" src="https://github.com/user-attachments/assets/723152ab-94bc-41b0-940c-abcb0f56cf9f" />
<img width="1067" height="647" alt="image" src="https://github.com/user-attachments/assets/4418fb0e-0aba-446d-be55-1771705565a2" />
<img width="732" height="584" alt="image" src="https://github.com/user-attachments/assets/88982cce-01b7-40e5-87f7-7c31fa73f5e9" />
<img width="772" height="623" alt="image" src="https://github.com/user-attachments/assets/b26bd170-8009-49d0-9580-6815194d353b" />
<img width="806" height="668" alt="image" src="https://github.com/user-attachments/assets/dd06747a-d3fd-4cab-b5ef-1335ffcf60fd" />
<img width="572" height="399" alt="image" src="https://github.com/user-attachments/assets/e64a5634-e713-4fd8-8492-b44f3565f09f" />





