# MediSCARA

## Summary
 MediSCARA project is a result of Hungarian collaborative development, provided by HSM Automatika as Technology Provider & Medicor as Manufacturing SME.
It consists of 2 individual robotic cells, one for high-end machine vision and non-removable laser marking handled by a Kawasaki collaborative robot; the other is devoted to accomplish enhanced robotic-based laser cutting solution similarly by a Kawasaki, 6 axis industrial robot.
#
## Background

It is dedicated for Medical Manufacturing SMEs to enhance prodution traceability and in-house production to reduce supply chain issues.

The whole project contains both robotic cells and their supplemetary state-of-the-art software components; however, each ROSE-AP component is available as a standalone component, also each cell is deployable on its own. 
 
 The major components are as follows:

 ### Industrial Cell 

 >   1. Kawasaki RS 6 axis robot
 >   2. Synrad CO2 laser source with chiller
 >   3. Tailor-made pneumatic gripper
 >   4. Machine Conrtol Unit
 >   5. Laser Control Unit
 >   6. Touchscreen HMI
 >   7. Full-coverage for radiation protection
 ### Collaborative cell

 >   1. Kawasaki dual-arm SCARA collaborative robot
 >   2. Keyence 3D Vision System with unique illumination
 >   3. Fiber laser marking system
 >   4. Label printer
 >   5. Machine Control Unit
 >   6. Touchscreen HMI
 >   7. Full-coverage for radiation protection

 ### Unix Server for data management 
 >   1. Orion Context Broker
 >   2. MondoDB
 >   3. QuantumLeap
 >   4. CrateDB
 >   5. Grafana
 >   6. RAMP real-time connection
 >   7. IoT Agent

### Embedded Softwares
>    1. MMWA - Manager WebAPP
>    2. MDPT - Automatic PDF generator
>    3. MMCU - Master Control Unit
>    4. MGKC - G-Code interpreter
>    5. MRTC - Transformation Calculator
--- 
### System Diadram
<img src="https://iili.io/ZDTpx2.md.png" alt="drawing" style="width:500px;"/>

### Grafana
![ZDzNWP.md.png](https://iili.io/ZDzNWP.md.png)

### RAMP 
![ZDIHI2.md.png](https://iili.io/ZDIHI2.md.png)

---
## ROSE-AP

The ROSE-AP components of the project are:
- Master Control Unit (**MMCU**): [here](https://github.com/ppuska/mediscara.mcu)
- PDF Generator (**MDPT**): [here]()
- Manager WebAPP (**MMWA**): [here]()
