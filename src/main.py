"""!
@file main.py
    This module controls the tasks that run our closed-loop controller, motors, and encoders. In addition
    it receives inputs from a development PC via serial port, which tells the module when to run a step response
    on the motors.

@author Clayton Elwell
@author Tyler McCue
@date   February 10, 2022

"""

import gc
import pyb
import cotask
import task_share
import Closed_Loop as control
import encoder_elwell_mccue as enc
import motor_elwell_mccue as moe
import utime


def task_MCU1 ():
    """!
    Task which puts things into a share and a queue.
    """
    while True:
        update = enc2.update()
        duty = control1.run(update)
        motor1.set_duty_cycle(duty)
        yield (0)


def task_MCU2 ():
    """!
    Task which takes things out of a queue and share to display.
    """
    while True:
        update = enc1.update()
        duty = control2.run(update)
        motor2.set_duty_cycle(duty)
        yield (0)
        
# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.

if __name__ == "__main__":
    
    ## Driver object for first motor
    motor1 = moe.MotorDriver(pyb.Pin.cpu.A10, pyb.Pin.cpu.B4, pyb.Pin.cpu.B5, 3)
    
    motor1.disable()
    
    ## Driver object for second motor
    motor2 = moe.MotorDriver(pyb.Pin.cpu.C1, pyb.Pin.cpu.A0, pyb.Pin.cpu.A1, 5)
    motor2.disable()
    
    ## Driver object for first encoder
    enc1 = enc.EncoderDriver(pyb.Pin.cpu.B6, pyb.Pin.cpu.B7, 4)
    ## Driver object for second encoder
    enc2 = enc.EncoderDriver(pyb.Pin.cpu.C6, pyb.Pin.cpu.C7, 8)
    
    enc1.set_position(0)
    enc2.set_position(0)
    ## Controller object for motor 1
    control1 = control.ClosedLoop(-100, 100, .008, 0, 0)
    ## Controller object for motor 2
    control2 = control.ClosedLoop(-100, 100, .008, 0, 0)

    ## Create a share and a queue to test function and diagnostic printouts
    share_duty = task_share.Share ('f', thread_protect = False, name = "Duty Cycle")
    #q0 = task_share.Queue ('L', 16, thread_protect = False, overwrite = False, name = "Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    ## Task for motor 1 that includes the controller and motor/encoder drivers
    task1 = cotask.Task (task_MCU1, name = 'Task_Motor_1', priority = 1, 
                         period = 75, profile = True, trace = False)
    ## Task for motor 2 that includes the controller and motor/encoder drivers
    task2 = cotask.Task (task_MCU2, name = 'Task_Motor_2', priority = 1, 
                         period = 75, profile = True, trace = False)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    while True:
        ## Input received via the serial port from the development computer
        x = input()
        if x == "a":
            ## Setpoint for the motors
            ref = float(input())
            control1.setReference(ref)
            ref = float(input())
            control2.setReference(ref)
        elif x == "b":
            ## Proportional gain for the motors
            new = float(input())
            control1.set_Kp(new)
            new = float(input())
            control2.set_Kp(new)
        elif x == "c":
            new = int(input())
            motor1.enable()
            motor2.enable()
            ## Time at which the step response execution begins
            start = utime.ticks_ms()
            while (utime.ticks_diff(utime.ticks_ms(),start) < new*1000):
                cotask.task_list.pri_sched()
            motor1.disable()
            motor2.disable()
            print("start")
            for i in range(min(len(control1.tArray),len(control2.tArray))):
                print('{:},{:},{:},{:}'.format(control1.tArray[i], control1.pArray[i],control2.tArray[i], control2.pArray[i]))
            print("stop")
            
        