'''
@file           Closed_Loop.py
@brief          Closed loop control class
@details        Class implementing a closed loop controller with only a
                proportional gain or a P controller
@author         Tyler McCue
@author         Clayton Elwell
@date           February 3, 2021
'''

import array
import utime
## Tick to degrees conversion attribute
tick2deg = 1/(256*16*2/360)

class ClosedLoop:
    '''
    @brief      Class that closes loop to control the system
    @details    Uses shared variables to get an error in the system
                which the controller then eliminates
    '''

    def __init__(self, saturation_low, saturation_high, Kp, dhigh, dlow):
        '''
        @brief          Constructor for closed loop controller
        @param saturation_low   Loweset value actuatuion can be based on system
        @param saturation_high  Highest value actuatuion can be based on system
        @param Kp               Proportional gain
        @param dhigh            Dead zone upper limit
        @param dlow             Dead zone lower limit
        '''
        ## Initial time
        self.t0 = utime.ticks_ms()
        ## creates class variable for lowest acutation value
        self.saturation_low = saturation_low
        ## creates class variable for highest acutation value
        self.saturation_high = saturation_high
        ## creates class variable for proportional gain
        self.Kp = Kp
        ## creates class variable for reference value
        self.reference = 0
        ## creates class variable for actuation
        self.actuation = 0
        ## Low dead zone attribute
        self.dead_zone_low = dlow
        ## High dead zone attribute
        self.dead_zone_high = dhigh
        ## Time array attribute for plotting
        self.tArray = array.array('f',[])
        ## Position array attribute for plotting
        self.pArray = array.array('f',[])

    def run(self, feedback):
        '''
        @brief              Updates actuation value from error and gain
        @param feedback     Refers to the output of the system
        '''
        
        current_time = utime.ticks_ms() - self.t0
        
        self.tArray.append(current_time/1000)
        self.pArray.append(feedback*tick2deg)
        
        prev = self.actuation
        self.actuation += self.Kp*(self.reference - feedback)
        
        diff = prev - self.actuation
        if diff > 0:
           if self.actuation < self.dead_zone_high and self.actuation > self.dead_zone_low:
               self.actuation = self.dead_zone_low
        if diff < 0:
           if self.actuation > self.dead_zone_low and self.actuation < self.dead_zone_high:
               self.actuation = self.dead_zone_high
               
        if self.actuation > self.saturation_high:
            self.actuation = self.saturation_high
        elif self.actuation < self.saturation_low:
            self.actuation = self.saturation_low
        return self.actuation

    def setReference(self, speed):
        '''
        @brief              Updates reference value
        @param speed        Refers to the new reference value
        '''
        self.reference = speed

    def getReference(self):
        '''
        @brief              Gets reference value
        '''
        return self.reference

    def get_Kp(self):
        '''
        @brief              Gets proportional gain
        '''
        return self.Kp

    def set_Kp(self, new):
        '''
        @brief              Updates gain value value
        @param new          Refers to the new proportional gain
        '''
        self.Kp = new
        
    def print_data(self):
        '''@brief Prints the collected position and time data in two columns.

        '''
        #print('Time [sec], Position [deg]')
        for i in range(len(self.tArray)):
            print('{:},{:}'.format(self.tArray[i], self.pArray[i]))
        self.tArray = []
        self.pArray = []
        #print(self.tArray, self.pArray)
        
    def send_data(self):
        '''@brief Sends the collected position and time data in a list
           @return The list of time and position values collected

        '''
        return [self.tArray, self.pArray]
