# CSU2 Controller

## Name
API for Control and Supply Unit 2 (CSU2) of IFG Institute for Scientific Instruments GmbH 

## Description
This project consists in the development af a python API to communicate with and control the device from IFG : CSU2.

It was first developped for MA-XRF and C-XRF devices developped by C2RMF and CNRS research unit

## Usage
typical use : 
```
import csu2controller

my_controller = csu2controller.CSU2Controller()
my_controller.connect()

resp = my_controller.query_ok()

print(resp)
```