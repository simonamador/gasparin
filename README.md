<h1 align="center"> <br> GASPARIN: Gamete Segmentation and Position Awareness Inference Network <br> </h1>

 <p align="center">
    <a href="https://github.com/simonamador">Carlos Simon Amador</a> • 
    <a href="https://github.com/AnaG18">Ana Paola Garcia</a> • 
   <a href="https://github.com/JessicaAmaralF">Jessica Amaral</a> • 
   <a href="https://www.linkedin.com/in/ana-paula-garcia-canales-55961b252/"> Ana Paula Garcia </a>
 </p>

## Purpose
Design a software as a medical device to assist medical professionals in intracytoplasmic sperm injection (ICSI) through the use of artificial intelligence models for computer vision. 

## Methodolody

The following platform is meant to assist embryologists through the use of computer vision in the following tasks:
* Sperm selection
* Sperm inmovilization
* Sperm injection

Through the use of two YOLO v8 models: one for multi-class detection and one for polygon segmentation.

For detection tasks involved in sperm selection and sperm injection, a YOLO v8 model was trained for multi-class selection. The workflow of this model can be observed in image 1.

![Detection framework](/assets/detection_framework.png)
Figure 1

For sperm inmovilization tasks, the detection model was connected to a polygon segmentation YOLO v8 model, and the polygons were employed to calculate the mid-points of sperm head and tail.

![Midpoint framework](/assets/midpoint_framework.png)
Figure 2

## models

This folder contains the jupyter files employed to train and validate the YOLO models. Training was done on both YOLO v5 and YOLO v8 models, for different parameters, and evaluated based on their Recall, Precission and F1.

## gasparin
Django application for an in vitro fertilization (IVF) visual assistance medical device.

## tests
Include codes for testing of camera, amd, and cuda.
