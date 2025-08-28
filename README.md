# Needle Insertion Trainer with Digital Twin

**Needle Insertion Trainer** is a low-cost trainer consisting of a needle, a dummy patient’s lower arm and their digital twins. It allows medical trainees to practice needle insertion and blood-draw techniques while receiving immediate feedback. The project is described in detail in the [presentation](/presentation/presentation.pdf).


## Content
[Images and Videos](#images-and-videos)

[Technical Decisions](#technical-decisions)

[Software Design](#software-design)

[Team](#team)

[How to run](#how-to-run)


## Images and Videos

### Set Up
![SetUpImage](/presentation/images/image_01.png)

### Needle Movement and Rotation
<img src="/presentation/videos/video_01.gif" alt="Video 1">

### Use Case: Blood Collection
<img src="/presentation/videos/video_02.gif" alt="Video 2">

## Technical Decisions

### Communication hardware and software
Motion, distance, and pressure sensors are connected to an **Arduino Nano Every**, which transmits the collected data to the **Sensor Handler Component** (implemented in Arduino) running on a workstation. This component forwards sensor data via the **Serial Communication Port** to a **Simulation Component** (implemented in Python), which reads the data from the port and integrates it into the simulation, enabling real-time interaction between the physical sensors and the virtual environment.

### Orientation, location, and pressure tracking
**BNO055 motion sensor** tracks needle orientation (pitch, yaw, roll). **VL6180X ToF sensor** measures distance to the dummy arm. **FSR (RP-S40-ST) pressure sensor** detects resistance changes on the arm.

### Digital Twin

**The SOFA Framework** was used to implement a realistic 3D visualization of the needle and the dummy lower arm. In the current setup, the needle can move along the Y-axis and rotate around any axis in the simulation window. To simulate the force applied to the arm, pressure is represented by color: under low pressure the tissue of the arm remains pink, while higher pressure gradually shifts it toward red.


## Software Design

The following UML diagrams illustrate the main software design decisions made in this project.

### Class Diagram of the Simulation Component
![Class diagram](/docs/software/class_diagram.png)

### Sequence Diagram: Needle Control
![Needle sequence diagram](/docs/software/needle_sequence_diagram.png)

### Sequence Diagram: Hand Control
![Hand sequence diagram](/docs/software/hand_sequence_diagram.png)


## Team
* [Shehab Awny](https://github.com/ShekoTito)
* [Aleksandr Vardanian](https://github.com/alex8399)
* [Jelle Hiddema](https://github.com/JelleHiddemaTUE)
* Yerin Choi
* Megan van Gerwen
* [Jori Schlangen](https://github.com/Schlangen-Jori)


## How to run

### Requirements
* Needle
* BNO055 motion sensor
* VL6180X ToF distance sensor
* FSR (RP-S40-ST) pressure sensor
* Arduino Nano Every
* Breadboard
* Wires from sensors to breadboard
* USB cable to host workstation
* Workstation (laptop/PC)

### Installation 
**1. Set up the physical components.**

Connect the motion (orientation), distance, and pressure sensors to the Arduino Nano Every and breadboard using wires, according to the schema. Connect the Arduino Nano Every to the workstation using a USB cable.

![Connection Scheme](/docs/installation/connection_scheme.png)

**2. Clone the project from GitHub.**

```bash
git clone https://github.com/alex8399/needle-insertion.git
cd needle-insertion
```

**3. Run Sensor Handler Component.**

3.1. Install the following libraries in the Arduino IDE on your workstation:
* `Adafruit BNO055 (version: 1.6.4)`
* `Adafruit BusIO (version: 1.17.2)`
* `Adafruit GFX Library (version: 1.12.1)`
* `Adafruit SSD1306 (version: 2.5.15)`
* `Adafruit Unified Sensor (version: 1.1.15)`
* `Adafruit_VL6180X (version: 1.4.4)`

3.2. Select `Arduino Nano Every` under `Tools > Board` in the Arduino IDE.

3.3. Set the serial port to `COM3` under `Tools > Port` in the Arduino IDE.

3.4. Set the baud rate to `115200` in the Arduino IDE.

3.5. Open the program `src\sensor_handler\sensor_reader\sensor_reader.ino` in the Arduino IDE and run it.

3.6. Make sure that the output appears in the Arduino IDE. <u>**However, when you run the Simulation Component that retrieves data from the serial port, close the output window in the Arduino IDE.**</u> Otherwise, an error will be thrown.

**4. Place mesh and OBJ files in the SOFA mesh directory.**

Copy the files `models\needle.obj` and `models\skin_layer.msh` into the folder `<path-to-SofaFramework>\share\sofa\mesh`.

**5. Run Simulation Component.**

5.1. Install `Sofa Framework v24.12.00` according to the [instruction](https://www.sofa-framework.org/download/). 

5.2. Install `SofaPython3` according to the [instruction](https://sofapython3.readthedocs.io/en/latest/content/Installation.html).

5.3. Install the required packages. <u>**Do not create a virtual environment.**</u>

```bash
pip install -r requirements.txt
```

5.4. Finally, run the Simulation Component.

```bash
python src/simulation/main.py
```
