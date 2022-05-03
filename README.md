# MediScara project

## Project structure

- mediscara_ws: main package for the MediScara project files
  - mediscara: package for the mediscara ROS files
  - interfaces: package for the ROS interface messages
- sensor: package for the sensor raspberry pi
- fiware: FIWARE docker files
- is_ws: workspace for the eProsima Integration Service
- mysql: workspace for the MySQL docker files 

## ROS Nodes

- [ ] Robotic cell 1 HMI node
- [x] Robotic cell 2 HMI node
- [x] Node for the laser marker
- [ ] Node for the Robotic cell 1
- [x] Node for the Robotic cell 2 (collaborative)
- [ ] Node for the laser cutter

## Sensor RPi

The sensor Raspberry pi is used to measure sensor data, and send said data directly to the FIWARE Orion Context Broker

### Installation

To install the package run:
    
    pip3 install ./sensor

## Errors

- Robotic Cell 1:

- Robotic Cell 2:
  - Node went offline: 021

