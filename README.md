# Lab3
## ME 405 Lab 3 Repository

In this experienment we used cotasks to control the execution of our Finite State Machine
and subsequently the step response of our motors. This method of task scheduling is more
robust and efficient than the method used in Lab2, in which we simply ran our tasks in
order with no specific frequency or period. 

Our closed loop controller utilizes position feedback to command our test kit motors
to follow a step response and rotate a flywheel 1 rotation. Our controller utilizes proportional control of the form
*K<sub>P</sub>*(*&theta;<sub>ref</sub>* - *&theta;<sub>meas</sub>*). The figures below 
display our progression of tuning our task frequency to optimize the computational intensity
of our controller.

We found that too slow of a motor frequency led to poor controller performance, as seen in
Figure 1. The frequency at which the controller's performance became unacceptable was ___
Hz. The recommended speed at which the motor task should be run is ___ Hz. Figure 2 displays
a plot of the step response with the recommended frequency. 




![Step response with motor task frequency of XXX Hz](kpof.0001.png)
<br>
Figure 1. Step response with controller frequency of XXX Hz; *K<sub>P</sub>* = 0.0001. 

![Step response with motor task frequnecy of XXX Hz](kpof1.png)
<br>
Figure 2. Step response with controller frequency of XXX Hz; *K<sub>P</sub>* = 1.
