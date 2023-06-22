import time
import math

class DebugInfoManager:
    def __init__(self):
        self.start_time=None
        self.end_time=None
        self.run_time=None

    def stampStartTime(self):
        self.start_time=time.time()
        return self.start_time

    def stampEndTime(self):
        self.end_time=time.time()
        return self.end_time

    def getRunTime(self):
        """returns the unix time difference between .startTime() and .endTime() function calls

        if start or end time wasn't stamped returns None
        """
        if start_time==None and end_time==None:
            self.run_time=end_time-start_time
        else:
            self.run_time=None
        
        return self.run_time
    
    def printImageSize(self,size):
        print("Original Size:",size[0],size[1],"px")

    def printNewImageSize(self,size,sampleSize):
         print("ANSI Size:",math.ceil(size[0]/sampleSize[0]),math.ceil(size[1]//sampleSize[1]),"chr")

    def printRunTIme(self):
        print("Converstion Time:",self.getRunTime(),"s")

