'''
@file           UI.py
@brief          PC user interface task
@details        Interprets user inputs and communicates with the Nucleo to send commands
                and receive data which is subsequently plotted.
@author         Tyler McCue
@author         Clayton Elwell
@date           February 10, 2021
'''


import serial as s
import matplotlib.pyplot as plt
import time

class UI:
    '''!
    Class that establishes communication with the Nucleo and accepts user inputs to trigger a step response to run.
    Data from the step response is sent from the Nucleo to the PC via serial port and this module parses and plots that data.
    '''

    def __init__(self, com):
        '''!
        Iniates the user interface class, established serial port communication, and displays a list of commands to the user.
        @param com     The serial port to be used for communication with the Nucleo
        '''
        ## Serial port attribute
        self.comnum = com
        
        print(' ____________________________ ')
        print('|                            |')
        print('|  Welcome to the C.T. UI    |')
        print('|  Commands:                 |')
        print('|     A. Set Reference Pos.  |')
        print('|     B. Set Gain            |')
        print('|     C. Run Step Response   |')
        print('|  Enter corresponding letter|')
        print('|         to start           |')
        print('|____________________________|')
        print('\n')
        
    
    def run(self, command):
        '''!
        Writes to the Nucleo via serial port
        @param command   The data to be written to the Nucleo
        '''
        with s.Serial(str(self.comnum), 115200) as port:
            port.write((command+"\r\n").encode('utf-8'))
    
    def read(self):
        '''!
        Reads data from the Nucleo via serial port, and subsequently parses that data and plots it.
        '''
        ## Flag to say if the method should read from the serial port
        flag = True
        ## Flag to begin the process of parsing the received data
        appStrt = False
        ## X-axis list for motor 1
        x1 = [] #preallocating some lists for future storage
        ## Y-axis list for motor 1
        y1 = []
        ## X-axis list for motor 2
        x2 = []
        ## Y-axis list for motor 2
        y2 = []
        with s.Serial(str(self.comnum), 115200) as port:
            #time.sleep(5)
            while flag:
                try:
                    ## Raw data read from the serial port
                    data = port.readline().decode('utf-8')
                    if appStrt:
                        ## Data split by commas and carriage returns
                        cooked = [idx for idx in data.replace('\r\n', '').split(',')]
                            
                        x1.append(float(cooked[0])) #adding first index to x list
                        y1.append(float(cooked[1])) #adding second index to y list
                        x2.append(float(cooked[2])) #adding first index to x list
                        y2.append(float(cooked[3])) #adding second index to y list

                    if "start" in data:
                        appStrt = True
                except:
                    break
                    
            plt.plot(x1, y1, label="Motor 1")
            plt.plot(x2, y2, label="Motor 2")
            plt.xlabel('Time (Seconds)')
            plt.ylabel('Position (Degrees)')
            plt.title('Step Response Plot')
            plt.legend()
            plt.show()
            
                    
                    
if __name__ == '__main__':
    ## User interface object
    user = UI('/dev/tty.usbmodem207C337057522')
    while True:
        ## Variable to store user keyboard input
        c = 0
        
        c = input("Enter Command: ")
        #print(user.read())
        user.run(c)
        if c == "a":
            ## Reference position for motor 1
            com1 = input("Please set reference position 1: ")
            user.run(com1)
            ## Reference position for motor 2
            com2 = input("Please set reference position 2: ")
            user.run(com2)
        elif c == "b":
            ## Controller gain for motor 1
            com1 = input("Please set a controller gain for 1: ")
            user.run(com1)
            ## Controller gain for motor 2
            com2 = input("Please set a controller gain for 2: ")
            user.run(com2)
        elif c == 'c':
            ## Time duration that step response is run for
            com1 = input("Please amount of time to run step response: ")
            user.run(com1)
            user.read()
            
            
            
        
