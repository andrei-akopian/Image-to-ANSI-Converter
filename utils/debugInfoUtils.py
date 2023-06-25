import time
import math

"""TODO
add csv export and by pixel analysis of time
"""

class DebugInfoManager:
    def __init__(self,hide):
        self.hide=hide
        self.start_time=None
        self.end_time=None
        self.run_time=None
        self.intervals=[]

    def stampStartTime(self):
        self.start_time=time.time()
        self.intervals.append(self.start_time)
        return self.start_time

    def stampEndTime(self):
        self.end_time=time.time()
        self.intervals.append(self.end_time)
        return self.end_time

    def stampInterval(self):
        self.intervals.append(time.time())
        return self.intervals[-1]

    def getInterval(self,i):
        if i+1<len(self.intervals):
            return self.intervals[i+1]-self.intervals[i]

    def getRunTime(self):
        """returns the unix time difference between .startTime() and .endTime() function calls

        if start or end time wasn't stamped returns None
        """
        if self.start_time==None or self.end_time==None:
            self.run_time=None
        else:
            self.run_time=self.end_time-self.start_time
        
        return self.run_time
    
    def printImageSize(self,image_size):
        print("Original Size:",image_size[0],image_size[1],"px")

    def printNewImageSize(self,image_size,sampleSize):
         print("ANSI Size:",math.ceil(image_size[0]/sampleSize[0]),math.ceil(image_size[1]//sampleSize[1]),"chr")

    def printRunTIme(self):
        print("Converstion Time:",round(self.getRunTime(),7),"s")
    
    def printLastInterval(self):
        #put this under an option
        if not(self.hide):
            interval=self.getInterval(len(self.intervals)-2)
            print("\033[0m %1.4fs" % interval,end="")
            return interval


