''' @file   UI.py
    @brief  PCPython module that communicates with the Nucleo via serial port.
    @details  Allows the user to set the reference position of the controller, the proportional gain of the controller, and
              run a step response on the controller.
    @author    Clayton Elwell
    @author    Tyler McCue
    @date      February 3, 2022
'''

import serial as s
import matplotlib.pyplot as plt
import time

class UI:
    '''@brief    User interface task to send various commands to a Nucleo via serial port.
       @details  Reads and writes to the Nucleo; sends triggers to cause the Nucleo to execute its own code; interprets
                 numerical data from the Nucleo and plots it.
    '''
    def __init__(self, com):
        '''@brief    Constructs a UI object
           @details  Prints the UI instructions, sets the COM port to communicate with
           @param    com Serial port for communication with the Nucleo
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
        '''@brief   Writes to the Nucleo
           @details Uses pyserial for serial communication
           @param   command Variable to be written to serial port
        '''
        with s.Serial(str(self.comnum), 115200) as port:
            port.write((command+"\r\n").encode('utf-8'))
    
    def read(self):
        '''@brief    Reads from the Nucleo via serial
           @details  Reads numerical data from the Nucleo, parses it, and appends it to lists/arrays for future plotting.
        '''
        #flag = True
        ## Absicca list
        x = [] #preallocating some lists for future storage
        ## Ordinate list
        y = []
        with s.Serial(str(self.comnum), 115200) as port:
            #time.sleep(5)
            while True:
                try:
                    ## Raw data read from serial
                    data = port.readline().decode('utf-8')
                    ## Parsed data
                    cooked = [idx for idx in data.replace('\r\n', '').split(',')]
                    
                    
                    ## Ordinate staging variable
                    xtemp = float(cooked[0]) # converting first index to float
                    ## Abscicca staging variable
                    ytemp = float(cooked[1]) # converting second index to float
                    x.append(xtemp) #adding first index to x list
                    y.append(ytemp) #adding second index to ylist
                    #print(y)
                except:
                    break
        #print('here')
            
                    
        plt.figure()
        plt.plot(x, y)
        plt.xlabel('Time, [sec]')
        plt.ylabel('Angular position [deg]')
        plt.title('1 Revolution Step Response - Position versus time with Kp = 0.05')
        plt.show()
        
        x = []
        y = []
            
                
                # cooking = [idx for idx in data.strip().split('\n')]  # splitting based on the carriage return
                # #print(cooking)
                
                # for i in range(len(cooking)-2):  # splits the commas in each list index, converts each list index into its own list
            
                # try:
                #     cooked = [idx for idx in cooking[i].split(',')]
                #     print(cooked)
                #     xtemp = float(cooked[0]) # converting first index to float
                #     ytemp = float(cooked[1]) # converting second index to float
                #     x.append(xtemp) #adding first index to x list
                #     y.append(ytemp) #adding second index to ylist
                
                # except:
                #    continue
                
                
           
                
   #             print(x)
    #            if x == 'Setting position value':
     #               flag = False
                    
                    
if __name__ == '__main__':
    
    ## User interface object
    user = UI('COM6')
    while True:
        ## Trigger attribute
        c = 0
        
        c = input("Enter Command: ")
        #print(user.read())
        user.run(c)
        if c == "a":
            ## Attribute that holds user-input reference position or controller gain.
            com = input("Please set reference position: ")
            user.run(com)
        elif c == "b":
            com = input("Please set a controller gain: ")
            user.run(com)
        elif c == 'c':
            user.read()
            #print('here')
            
            
            
        
