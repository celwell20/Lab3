"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
import print_task
import Closed_Loop
import encoder_elwell_mccue as enc
import motor_elwell_mccue as moe


def task_controller():
    '''!
    Task that takes encoder updates and uses the update value to calculate the next duty cycle
    '''
    while True:
        update = enc1.update()
        duty = control.run(update)
        share_duty.put(duty)
        if update >= control.getReference():
            motor1.disable()
            motor1.set_duty_cycle(0)
            control.print_data()
            

def task_motor():
    '''!
    Task that takes the calculated duty cycle and uses it to send a PWM signal to the motor
    '''
    

def task1_fun ():
    """!
    Task which puts things into a share and a queue.
    """
    counter = 0
    while True:
        share0.put (counter)
        q0.put (counter)
        counter += 1

        yield (0)


def task2_fun ():
    """!
    Task which takes things out of a queue and share to display.
    """
    while True:
        # Show everything currently in the queue and the value in the share
        print ("Share: {:}, Queue: ".format (share0.get ()), end='');
        while q0.any ():
            print ("{:} ".format (q0.get ()), end='')
        print ('')

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
    ## Object for controller
    control = control.ClosedLoop(-100, 100, 1, 0, 0)
    control.setReference(8192)
    
    print ('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
           'Press ENTER to stop and show diagnostics.')

    # Create a share and a queue to test function and diagnostic printouts
    share_duty = task_share.Share ('f', thread_protect = False, name = "Duty cycle shared variable")
    #q0 = task_share.Queue ('L', 16, thread_protect = False, overwrite = False,
                           #name = "Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    controller_cotask = cotask.Task (task_controller, name = 'Task_1', priority = 1, 
                         period = 400, profile = True, trace = False)
    motor_cotask = cotask.Task (task_motor, name = 'Task_2', priority = 2, 
                         period = 1500, profile = True, trace = False)
    cotask.task_list.append (controller_cotask)
    cotask.task_list.append (motor_cotask)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP ()
    while not vcp.any ():
        cotask.task_list.pri_sched ()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()

    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')
