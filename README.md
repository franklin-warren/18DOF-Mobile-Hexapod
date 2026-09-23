**18DOF HEXAPOD ROBOT: It's a spider bot with a suite of sensors. Manual joystick control with plans to implement autonomous walking.**
<img width="1259" height="941" alt="image" src="https://github.com/user-attachments/assets/576bdf7d-288b-41cf-b133-5b3795a55f39" />

Currently under construction, this represents progress at the end of Stardance. All code is a work in progress. <br>
Inserted are images/videos of the construction process, including photos of assembly, videos of legs moving, as well as CAD screenshots. <br>
Currently in the main programming stage of the design. <br>
<br>
**Key points:**
	<br>
	Derived and programmed a custom inverse kinematics engine in both leg-centric and bot-centric design <br>
	Derived and implemented a cycloidal step path to reduce power draw and servo strain <br>
	Designed a 3 layer PCB stackup to handle high-amp servo draw and sensitive sensor data simultaneously <br>
	Mass-computed 870 000 point leg reachability clouds in Python to assist in step planning <br>
	Implementing closed loop control with FSR step detection, real-time clearance sensor, and IMU. <br>
	Implementing LIDAR room scanning
	Current architecture is ESP32-Pi Zero W via UART, however, there are eventual plans for ROS2 integration


<br>
**Media:**
<br>
**Walk through/work in progress demo:** <br>
https://drive.google.com/file/d/1R8LIc6dlmES_6KmEAEqcxywUw9GedAyd/view?usp=drive_link
<br>
**Video of two legs walking:**<br>
https://github.com/user-attachments/assets/c0b8d58c-5718-43e7-b491-6766b3c93bf8
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

<br>
Build and samples from my engineering notebook:
<br>
<img width="635" height="670" alt="image" src="https://github.com/user-attachments/assets/a1ff342d-03ef-4997-9e3d-7e4f1d81ffa9" />
<img width="620" height="787" alt="image" src="https://github.com/user-attachments/assets/72631028-9518-440f-96d9-83da0f77e5c5" />
<img width="583" height="729" alt="image" src="https://github.com/user-attachments/assets/e34c4752-0645-4e41-b633-1219c8198fe8" />
<img width="550" height="722" alt="image" src="https://github.com/user-attachments/assets/d6bf6107-2666-4615-898f-47b7f0200dc6" />
<img width="528" height="652" alt="image" src="https://github.com/user-attachments/assets/c00294bf-c91a-4248-a500-df394b4a1f45" />
<br>
I am currently taking a linear algebra course, so I will revisit these transformation after midterms. 
<br>
<img width="570" height="774" alt="image" src="https://github.com/user-attachments/assets/b7fd8fb0-a92d-4a8e-a387-27a2d6b3445a" />
<img width="575" height="735" alt="image" src="https://github.com/user-attachments/assets/654039ca-7fdb-4eaa-aeb9-3e2d185962c5" />
<br>
Note that with some testing and condensing, I did manage to fit the hexapod onto a slimmer profile, small enough for each frame part to be one piece, printed on a standard build size (25x25cm, ish). 
<br>
<img width="583" height="708" alt="image" src="https://github.com/user-attachments/assets/f6e8e8b5-9cb0-4b7c-8123-1a165e89635d" />
<img width="545" height="708" alt="image" src="https://github.com/user-attachments/assets/b2a69725-3682-4039-b095-e1ca562f1264" />
<br>
Some changes to the electronics layout have been made, although the core components have stayed the same. 

<br>
<br>
**What works:**
<br>
	Full electromechanical assembly
	One side successfully responds to servo mode commands. 
	Noise has been reduced on IIC lines, they now work. 
	Power system works with no shorts.
	Gait math per leg has been derived, robot-centric has been derived (although refinements are in progress). 
	Cycloidal algorithm works near-flawless, no complaints. It reduces servo power by over 500mA (during startup, as opposed to a linear/instant acceleration curve).
<br>
<br>
**What is still to be done:**
<br>
	The other side PCA has to be swapped (scheduled for prior to October 1st)
	Raspberry Pi <-> ESP link must be validated. 
	Major programming and sensor integration.
	Making the robot walk to a demo-worthy standard

<br>
<br>
**Stretch Goals:**
<br>
	LiDAR, either simple point cloud or full SLAM
	Autonomous walking/navigation.
	
	
<br>
<br>
**Print settings, assembly tips, etc:**
<br>
	Print out of PETG at 4 wall loops and 30% gyroid infill. If the legs are too heavy, there will be too much torque needed, and the servos will be strained. 
	Assembly can follow the CAD for the most part. Ensure all heat sets are as close to straight as possible. 
	Some heat sets are inserted from the reverse side. They may have to be drilled out. Take a 3/32" drill bit or smaller and run it through the hole to clear any plastic,
	then thread a screw all the way through then out. This cuts a thread before assembly. DO NOT damage the brass with the drill bit. 
	All servos should be centered during assembly. The tibia requires +-110 degrees of freedom, so close to exact centering is important. Adjust trim values in code. 
	The femur-tibia bracket must be installed before installing the main tibia piece, as it must flex to fit in. 
	When soldering, test for shorts often. They will break sensitive components. 
	Be careful with batteries. Be careful with the electricity. This draws an estimated 20A. Do not allow the battery to short. 
	









